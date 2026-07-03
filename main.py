from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
import jwt
import sqlite3

app = FastAPI(
    title="Enterprise User Auth API v1.5",
    description="Step 5 (Enhanced): FastAPI Auth Engine with Role-Based Access Control (RBAC)"
)

# --- BIZTONSÁGI BEÁLLÍTÁSOK ---
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "szuper_titkos_kiber_pajzs_kulcs_ami_brutalis_hosszu"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Ez a segédlet automatikusan kiolvassa a "Authorization: Bearer <TOKEN>" fejlécet a kérésekből
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- ADATBÁZIS INICIALIZÁLÁSA (Új role oszloppal) ---
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- ADATMODELLEK (Pydantic) ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"  # Alapértelmezett szerepkör, de megadható 'admin' is

class UserLogin(BaseModel):
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
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- TOKEN DEKÓDOLÓ ÉS JOGOSULTSÁG ELLENŐRZŐ DEPENDENCY ---
def get_current_user_role(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")
        return {"email": email, "role": role}
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

# --- API VÉGPONTOK (ENDPOINTS) ---

@app.get("/")
def read_root():
    return {"status": "Online", "engine": "FastAPI + RBAC Auth Core v1.5"}

# 1. REGISZTRÁCIÓ (Már menti a szerepkört is)
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    if user.role not in ["user", "admin"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role type. Use 'user' or 'admin'.")
        
    hashed_pwd = get_password_hash(user.password)
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, hashed_password, role) VALUES (?, ?, ?)", (user.email, hashed_pwd, user.role))
        conn.commit()
        conn.close()
        return {"message": "User registered successfully", "email": user.email, "role": user.role}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

# 2. BEJELENTKEZÉS (A tokenbe most már beégetjük a felhasználó jogkörét is!)
@app.post("/login")
def login_user(user: UserLogin):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password, role FROM users WHERE email = ?", (user.email,))
    result = cursor.fetchone()
    conn.close()
    
    if not result or not verify_password(user.password, result[0]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    user_role = result[1]
    # A szerepkört (role) beletesszük a JWT token "belsejébe"
    access_token = create_access_token(data={"sub": user.email, "role": user_role})
    return {"access_token": access_token, "token_type": "bearer"}

# 3. 🔐 VÉDETT ADMIN VÉGPONT (Csak admin joggal enged be!)
@app.get("/admin/dashboard")
def get_admin_dashboard(current_user: dict = Depends(get_current_user_role)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not have admin privileges."
        )
    return {
        "message": f"Welcome to the Secure Admin Dashboard, {current_user['email']}!",
        "secret_server_data": "Brutálisan titkos vállalati információk elérhetőek."
    }
