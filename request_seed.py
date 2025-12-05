
import os
import json
import requests

# -------------------- CHANGE ONLY THESE --------------------
STUDENT_ID = "23MH1A1228"
GITHUB_REPO_URL = "https://github.com/Pujitha-png/secure-2fa-microservice.git"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"
STUDENT_PUBLIC_KEY_PATH = "student_public.pem"
# -------------------------------------------------------------

def request_seed():
    # Ensure data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Read your public key
    with open(STUDENT_PUBLIC_KEY_PATH, "r") as f:
        public_key = f.read().strip()

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        result = response.json()

        if "encrypted_seed" not in result:
            print("Error from API:", result)
            return

        encrypted_seed = result["encrypted_seed"]

        # Save inside data/encrypted_seed.txt
        with open("data/encrypted_seed.txt", "w") as f:
            f.write(encrypted_seed)

        print("Encrypted seed saved to data/encrypted_seed.txt")

    except Exception as e:
        print("Request failed:", e)


if __name__ == "__main__":
    request_seed()
