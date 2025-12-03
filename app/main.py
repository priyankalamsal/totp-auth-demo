from datetime import datetime

from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os
from app.crypto_utils import load_private_key, decrypt_seed, generate_totp_code, verify_totp_code

# File where decrypted seed will be stored
SEED_PATH = Path(os.getenv("SEED_PATH", "data/seed.txt"))
PRIVATE_KEY_PATH = Path(os.getenv("PRIVATE_KEY_PATH", "student_private.pem"))

app = FastAPI()

class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

# Load private key once
try:
    PRIVATE_KEY = load_private_key(PRIVATE_KEY_PATH)
except Exception:
    PRIVATE_KEY = None


@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(req: DecryptRequest):
    if PRIVATE_KEY is None:
        raise HTTPException(status_code=500, detail="Private key not loaded")

    try:
        seed_hex = decrypt_seed(req.encrypted_seed, PRIVATE_KEY)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {e}")

    # ensure directory exists
    SEED_PATH.parent.mkdir(parents=True, exist_ok=True)

    # save seed
    SEED_PATH.write_text(seed_hex)

    return {"status": "ok"}


@app.get("/generate-2fa")
async def generate_2fa():
    if not SEED_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not available yet")

    seed_hex = SEED_PATH.read_text().strip()

    try:
        code = generate_totp_code(seed_hex)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate code")

    import time
    valid_for = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
async def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not SEED_PATH.exists():
        raise HTTPException(status_code=500, detail="Seed not available yet")

    seed_hex = SEED_PATH.read_text().strip()

    try:
        valid = verify_totp_code(seed_hex, req.code, valid_window=1)
    except Exception:
        raise HTTPException(status_code=500, detail="Verification failed")

    return {"valid": valid}
from fastapi import status

@app.get("/status")
def system_status():
    return {
        "api": "running",
        "cron_last_run": read_last_run(),
        "current_time_utc": datetime.utcnow().isoformat()
    }

def read_last_run():
    try:
        with open("/cron/last_code.txt", "r") as f:
            return f.readline().strip()
    except Exception:
        return "no data"

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("app/templates/index.html")

