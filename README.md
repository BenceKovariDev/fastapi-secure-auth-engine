# FastAPI Secure Authentication Engine with RBAC (Step 5 Enhanced)

A high-performance, production-ready enterprise user authentication microservice built with **FastAPI**, featuring secure cryptographic password hashing, **SQLite** persistence, stateless **JWT (JSON Web Tokens)**, and **Role-Based Access Control (RBAC)**.

This repository represents **Step 5 out of my 1000-lesson masterclass engineering journey**, heavily refactored to support enterprise-grade security structures like granular user privileges and route protection. Developed entirely within a localized mobile Linux environment (Userland) using Python 3.14.

## 🚀 Enhanced Features

- **Asynchronous API Endpoints**: Powered by FastAPI and Uvicorn for blazing-fast I/O operations.
- **Role-Based Access Control (RBAC)**: Supports explicit role isolation (`user` vs. `admin`) out of the box.
- **Granular Route Protection**: Implements a strict dependency injection layer to intercept requests and enforce permission boundaries (`GET /admin/dashboard`).
- **Secure Password Hashing**: Implements one-way cryptographic salting and hashing utilizing the `bcrypt` algorithm via `passlib`.
- **Stateless JWT Authentication**: Generates short-lived, cryptographically signed access tokens embedded with secure role claims.

## 🛠️ Tech Stack

- **Language**: Python 3.14
- **Framework**: FastAPI
- **Security**: PyJWT, Passlib [bcrypt], OAuth2
- **Database**: SQLite3

## 🛣️ API Architecture & RBAC Flow

- `GET /` - Root status health check.
- `POST /register` - Accepts `email`, `password`, and optional `role` (stores safely in SQLite).
- `POST /login` - Validates credentials, injects user privileges into claims, and returns a bearer JWT.
- `GET /admin/dashboard` - **Vulnerable/Protected** endpoint requiring valid admin JWT token verification. Throws `403 Forbidden` for standard users.

---
*Maintained with 💻 as part of a 1000-project backend engineering sprint.*
