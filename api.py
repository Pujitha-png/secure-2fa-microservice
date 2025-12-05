
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pyotp
import time

app = FastAPI()

# ----------------------------
# Paths
# ----------------------------
DATA_FOLDER = Path("data")
SEED_FILE = DATA_FOLDER / "seed.txt"
PRIVATE_KEY_FILE = Path("student_private.pem")  # stays in project root

# ----------------------------
# Models
# ----------------------------
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str

# ----------------------------
# Endpoint 1: /decrypt-seed
# ----------------------------
@app.post("/decrypt-seed")
def decrypt_seed(request: DecryptSeedRequest):
    if not request.encrypted_seed:
        raise HTTPException(status_code=400, detail="Encrypted seed missing")

    if not PRIVATE_KEY_FILE.exists():
        raise HTTPException(status_code=400, detail=f"Private key not found at {PRIVATE_KEY_FILE}")

    # Decode Base64
    try:
        encrypted_bytes = base64.b64decode(request.encrypted_seed)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Base64 decode failed: {str(e)}")

    # Load private key
    try:
        private_key = serialization.load_pem_private_key(
            PRIVATE_KEY_FILE.read_bytes(),
            password=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load private key: {str(e)}")

    # Decrypt
    try:
        decrypted_seed = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"RSA decryption failed: {str(e)}")

    # Convert to hex
    hex_seed = decrypted_seed.hex()
    if len(hex_seed) != 64:
        raise HTTPException(status_code=400, detail=f"Decrypted seed invalid length: {len(hex_seed)} hex chars")

    # Save to file
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    SEED_FILE.write_text(hex_seed)

    return {"status": "ok", "message": "Seed decrypted successfully", "decrypted_seed": hex_seed}

# ----------------------------
# Endpoint 2: /generate-2fa
# ----------------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = SEED_FILE.read_text().strip()
    # Convert hex to Base32 for pyotp
    seed_bytes = bytes.fromhex(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')

    totp = pyotp.TOTP(seed_base32)
    code = totp.now()
    valid_for = 30 - (int(time.time()) % 30)

    return {"code": code, "valid_for": valid_for}

# ----------------------------
# Endpoint 3: /verify-2fa
# ----------------------------
@app.post("/verify-2fa")
def verify_2fa(request: Verify2FARequest):
    if not request.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = SEED_FILE.read_text().strip()
    # Convert hex to Base32 for pyotp
    seed_bytes = bytes.fromhex(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')

    totp = pyotp.TOTP(seed_base32)
    is_valid = totp.verify(request.code, valid_window=1)

    return {"valid": is_valid}
