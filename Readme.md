# Secure 2FA Microservice

## Overview
This project is a secure Two-Factor Authentication (2FA) microservice that generates and validates Time-Based One-Time Passwords (TOTP) for user authentication. The microservice works with an instructor-provided API to handle encrypted seeds, making it suitable for secure submission and verification in an academic environment.

---

## Project Steps

1. Created the project folder `secure-2fa-microservice` to organize all files and resources.  
2. Set up the Python environment and installed required packages.  
3. Generated `student_private.pem` and `student_public.pem` to handle commit signing.  
4. Added the instructor's public key `instructor_public.pem` for seed encryption.  
5. Requested an encrypted seed from the instructor API.  
6. Stored the received seed in `data/encrypted_seed.txt`.  
7. Implemented functionality to generate TOTP codes from the secret key.  
8. Built validation for user-provided TOTP codes.  
9. Developed API endpoints to generate and validate TOTP codes.  
10. Created `submission.py` to prepare all required submission outputs.  
11. Signed the final Git commit hash using the student private key.  
12. Encrypted the commit signature using the instructor's public key.  
13. Verified all outputs, including commit signature, public key, and encrypted seed.  
14. Added Docker support with a Dockerfile and optional docker-compose.yml.  
15. Documented the project, including steps, features, and submission process.

---

## Author
**Pujita Kotha**
GitHub: [https://github.com/Pujitha-png](https://github.com/Pujitha-png)

---

This microservice is designed to be secure, easy to use, and ready for deployment or submission. All scripts, keys, and instructions required for operation and verification are included in the project.
