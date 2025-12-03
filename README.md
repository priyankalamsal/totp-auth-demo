# PKI + TOTP Authentication Microservice  
Secure RSA-based Seed Decryption + TOTP 2FA + Cron Logging (Dockerized)

This project implements a fully secure, containerized microservice that demonstrates enterprise-grade authentication practices using:

- **RSA 4096-bit cryptography (OAEP + PSS)**
- **TOTP-based 2FA (SHA-1, 30s window, 6 digits)**
- **FastAPI REST API**
- **Cron job automation inside Docker**
- **Persistent volumes for seed + logs**
- **Multi-stage Docker build**

This microservice securely decrypts a seed sent by the instructor, stores it, generates TOTP codes, verifies codes, and logs them every minute.

---

# 🚀 Features

### 🔐 **Cryptography**
- RSA-4096 keys with exponent 65537  
- RSA/OAEP-SHA256 seed decryption  
- RSA-PSS-SHA256 commit signature  
- Instructor public key encryption (RSA-OAEP-SHA256)

### 🔑 **2FA / TOTP**
- SHA-1 algorithm  
- 30s time period  
- 6-digit codes  
- Hex seed converted → Base32 correctly  
- ±1 time window tolerance

### 🐳 **Docker Microservice**
- Multi-stage build (builder → runtime)  
- Cron daemon runs inside the container  
- Automatic TOTP logging every minute  
- UTC timezone everywhere  
- Persistent volumes:
  - `/data` → decrypted seed  
  - `/cron` → last TOTP code output  

---

# 📡 API Endpoints

## `POST /decrypt-seed`
Decrypts encrypted seed using RSA-OAEP and stores at `/data/seed.txt`.

**Body:**
```json
{
  "encrypted_seed": "BASE64_STRING"
}
