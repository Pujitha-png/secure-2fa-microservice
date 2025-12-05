#!/usr/bin/env python3
import os
from datetime import datetime
import pyotp
import base64

SEED_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

try:
    hex_seed = open(SEED_FILE).read().strip()
except FileNotFoundError:
    hex_seed = None

if hex_seed:
    # Convert hex seed to bytes, then to base32
    seed_bytes = bytes.fromhex(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')

    totp = pyotp.TOTP(seed_base32)
    code = totp.now()

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"({timestamp}) 2FA Code: {code}\n")
