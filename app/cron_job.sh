#!/usr/bin/env bash

PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"
export PATH
echo "PATH=$PATH" >> /cron/debug_path.txt

set -euo pipefail
UTC_DATE() { date -u +"%Y-%m-%d %H:%M:%S"; }

SEED_FILE="/data/seed.txt"
OUT="/cron/last_code.txt"

if [ ! -f "$SEED_FILE" ]; then
  echo "$(UTC_DATE) - ERROR: seed file not found" >&2
  exit 1
fi

seed_hex=$(tr -d '[:space:]' < "$SEED_FILE")

if ! [[ "$seed_hex" =~ ^[0-9a-fA-F]{64}$ ]]; then
  echo "$(UTC_DATE) - ERROR: invalid seed format" >&2
  exit 1
fi

code=$(/usr/local/bin/python3 - <<PY
import base64, pyotp

seed_hex = "$seed_hex"
seed_bytes = bytes.fromhex(seed_hex)
base32 = base64.b32encode(seed_bytes).decode()
t = pyotp.TOTP(base32, digits=6, interval=30)
print(t.now())
PY
)

echo "$(UTC_DATE) - 2FA Code: $code" > "$OUT"

