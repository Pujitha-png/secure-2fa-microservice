
import base64
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

PRIVATE_KEY_PATH = "student_private.pem"
ENCRYPTED_FILE = "data/encrypted_seed.txt"  # <-- updated path
DATA_FILE = "data/seed.txt"

def decrypt_seed():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    with open(ENCRYPTED_FILE, "r") as f:
        encrypted_seed_b64 = f.read().strip()

    decoded_bytes = base64.b64decode(encrypted_seed_b64)
    decrypted_bytes = private_key.decrypt(
        decoded_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    hex_seed = decrypted_bytes.decode("utf-8")
    if len(hex_seed) != 64:
        raise ValueError("Invalid decrypted seed")

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        f.write(hex_seed)

    print("Decrypted seed saved to:", DATA_FILE)
    print("Hex seed:", hex_seed)

if __name__ == "__main__":
    decrypt_seed()
