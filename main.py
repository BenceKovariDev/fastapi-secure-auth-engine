from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
import sqlite3

app = FastAPI(
    title="Enterprise User Auth API v1.0",
    description="Step 5 of 1000: Secure FastAPI Authentication Engine with JWT & Bcrypt"
)

# --- BIZTONSÁGI BEÁLLÍTÁSOK ---
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FIGYELEM: Éles környezetben ezt környezeti változóból (ENV) kell beolvasni!
SECRET_KEY = "szuper_titkos_kiber_pajzs_kulcs_ami_brutalis_hosszu"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # A token 30 perc után lejár

# --- ADATBÁZIS INICIALIZÁLÁSA ---
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- ADATMODELLEK (Pydantic) ---
class UserAuth(BaseModel):
    email: EmailStr
    password: str

# --- SEGÉDFÜGGVÉNYEK ---
def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- API VÉGPONTOK (ENDPOINTS) ---

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "milestone": "5 out of 1000",
        "engine": "FastAPI + JWT Auth Core"
    }

# 1. REGISZTRÁCIÓ (POST /register)
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserAuth):
    hashed_pwd = get_password_hash(user.password)
    
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, hashed_password) VALUES (?, ?)", (user.email, hashed_pwd))
        conn.commit()
        conn.close()
        return {"message": "User registered successfully", "email": user.email}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

# 2. BEJELENTKEZÉS ÉS TOKEN GENERÁLÁS (POST /login)
@app.post("/login")
def login_user(user: UserAuth):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE email = ?", (user.email,))
    result = cursor.fetchone()
    conn.close()
    
    # Felhasználó ellenőrzése és a hashelt jelszó összehasonlítása
    if not result or not verify_password(user.password, result[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Ha minden stimmel, generálunk egy JWT tokent
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in_minutes": ACCESS_TOKEN_EXPIRE_MINUTES
    }
