from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os

# ---CREATE KEY -------------------------------
key = os.urandom(32)        # random 32 byte secret key
cipher = ChaCha20Poly1305(key)

# ---ENCRIPTION--------------------------------
message = b"Hello ! How are You?"
nonce = os.urandom(12)
encrypted = cipher.encrypt(nonce, message, None)

print("Original : ", message)
print("Encription :", encrypted)

# ---DECRIPT -----------------------------------
decrypted = cipher.decrypt(nonce, encrypted, None)
print("Decripted : ", decrypted)
 