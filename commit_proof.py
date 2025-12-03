import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)

# ======== CONFIG ========
COMMIT_HASH = "760e2fcce8b9948645238a685ccf98bd6d7001f0"
STUDENT_PRIVATE_KEY_PATH = "student_private.pem"
INSTRUCTOR_PUBLIC_KEY_PATH = "instructor_public.pem"
# ========================

# 1. Load student private key
with open(STUDENT_PRIVATE_KEY_PATH, "rb") as f:
    private_key = load_pem_private_key(f.read(), password=None)

# 2. Load instructor public key
with open(INSTRUCTOR_PUBLIC_KEY_PATH, "rb") as f:
    instructor_pub = load_pem_public_key(f.read())

# 3. Sign commit hash using RSA-PSS-SHA256 (ASCII encoding)
signature = private_key.sign(
    COMMIT_HASH.encode("utf-8"),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    ),
    hashes.SHA256(),
)

# 4. Encrypt signature using instructor public key (RSA-OAEP-SHA256)
encrypted_signature = instructor_pub.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# 5. Base64 encode for submission
encrypted_signature_b64 = base64.b64encode(encrypted_signature).decode("utf-8")

print("\n========== SUBMISSION OUTPUT ==========\n")
print("Commit Hash:")
print(COMMIT_HASH)
print("\nEncrypted Signature (Base64, single line):")
print(encrypted_signature_b64)
print("\n========================================\n")
