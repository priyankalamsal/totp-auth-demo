# TOTP Auth Microservice

I built a complete authentication microservice that combines RSA encryption, TOTP-based 2FA, secure API endpoints, Docker containerization, and an automated cron system. The service decrypts an encrypted seed using my RSA private key, generates time-based one-time passwords, verifies them with tolerance, and logs fresh 2FA codes every minute.  

Everything runs inside a container with persistent storage, so the seed and cron logs survive restarts. I also implemented a status endpoint, proper error handling, and followed all security rules required in the task.  

The project includes my full working API, cron job, multi-stage Docker build, and commit proof generation. This repository represents the final working solution for the entire assignment.
