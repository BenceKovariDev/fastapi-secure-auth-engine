# FastAPI Secure Authentication Engine (Step 5 of 1000)

A high-performance, production-ready enterprise user authentication microservice built with **FastAPI**, featuring secure cryptographic password hashing, **SQLite** persistence, and stateless **JWT (JSON Web Tokens)** session management[cite: 1].

This repository represents **Step 5 out of my 1000-lesson masterclass engineering journey**, focusing on clean architecture, strict data validation, and modern backend security best practices[cite: 1]. Developed entirely within a localized mobile Linux environment (Userland) using Python 3.14[cite: 1].

## 🚀 Features

- **Asynchronous API Endpoints**: Powered by FastAPI and Uvicorn for blazing-fast I/O operations[cite: 1].
- **Secure Password Hashing**: Implements one-way cryptographic salting and hashing utilizing the `bcrypt` algorithm via `passlib`[cite: 1].
- **Stateless JWT Authentication**: Generates short-lived, cryptographically signed access tokens for downstream endpoint protection[cite: 1].
- **Strict Payload Validation**: Leverages `Pydantic` schemas (including strict `EmailStr` rules) to sanitise inputs at the gateway layer[cite: 1].
- **Lightweight DB Persistence**: Integrates a clean, decoupled SQLite relational database configuration[cite: 1].

## 🛠️ Tech Stack

- **Language**: Python 3.14[cite: 1]
- **Framework**: FastAPI[cite: 1]
- **ASGI Server**: Uvicorn[cite: 1]
- **Data Validation**: Pydantic v2 (with email-validator)[cite: 1]
- **Security**: PyJWT, Passlib [bcrypt][cite: 1]
- **Database**: SQLite3[cite: 1]

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/BenceKovariDev/fastapi-secure-auth-engine.git](https://github.com/BenceKovariDev/fastapi-secure-auth-engine.git)
   cd fastapi-secure-auth-engine
   ```[cite: 1]

2. **Create and activate a virtual environment (PEP 668 Compliant):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```[cite: 1]

3. **Install the required dependencies:**
   ```bash
   pip install fastapi uvicorn "passlib[bcrypt]" pyjwt python-multipart email-validator
   ```[cite: 1]

4. **Launch the Uvicorn development server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```[cite: 1]

5. **Access the Interactive API Documentation (Swagger UI):**
   Open your browser and navigate to: `http://127.0.0.1:8000/docs`[cite: 1]

## 🛣️ API Architecture

- `GET /` - Root status health check[cite: 1].
- `POST /register` - Registers a new user, hashes the password, and stores data in SQLite[cite: 1].
- `POST /login` - Validates credentials and issues a cryptographically signed bearer JWT token[cite: 1].

---
*Maintained with 💻 as part of a 1000-project backend engineering sprint.*[cite: 1]
