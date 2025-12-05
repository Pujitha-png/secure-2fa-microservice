
import pyotp
import base64

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    seed_bytes = bytes.fromhex(hex_seed)
    seed_base32 = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(seed_base32)
    return totp.verify(code, valid_window=valid_window)

if __name__ == "__main__":
    with open("./data/seed.txt", "r") as f:
        hex_seed = f.read().strip()

    code_to_verify = input("Enter the 6-digit TOTP code: ").strip()
    is_valid = verify_totp_code(hex_seed, code_to_verify)
    print("Is the code valid?", is_valid)
