import pyotp
import base64
import time

def generate_totp_code(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(seed_base32)
    return totp.now()

if __name__ == "__main__":
    with open("./data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    period = 30
    remaining = period - (int(time.time()) % period)

    print("Generated TOTP:", code)
    print("Valid for (seconds):", remaining)
