# TOTP Auth Microservice

A secure **PKI + TOTP-based authentication microservice** built with **FastAPI**, **Docker**, and **Cron**.  
This project demonstrates RSA cryptography, encrypted seed handling, TOTP generation, and containerized deployment.

---

## Features
- RSA (PKI) based encrypted seed decryption
- Time-based One-Time Password (TOTP) generation & verification
- REST APIs using FastAPI
- Cron job to generate and log 2FA codes every minute
- Dockerized with persistent volumes
- Production-ready structure

---

## Tech Stack
- **Backend:** Python, FastAPI
- **Security:** RSA (OAEP, PSS), PyOTP
- **DevOps:** Docker, Docker Compose, Cron
- **Tools:** Git, GitHub

---

## API Endpoints
- `POST /decrypt-seed` – Decrypt and store encrypted seed
- `GET /generate-2fa` – Generate current TOTP code
- `POST /verify-2fa` – Verify a TOTP code

---

## Run Locally

```bash
docker-compose up --build
```

Service runs on:
```
http://localhost:8080
```

---

## Author
**Priyanka Lamsal**  
GitHub: https://github.com/priyankalamsal
