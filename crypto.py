# crypto.py
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os

# Both server and client must use SAME key
# This is our shared secret key
KEY = b'\x01' * 32      # 32 bytes (we will improve this later)
cipher = ChaCha20Poly1305(KEY)

def encrypt(data: bytes) -> bytes:
    nonce = os.urandom(12)          # random 12 bytes every time
    encrypted = cipher.encrypt(nonce, data, None)
    return nonce + encrypted        # send nonce with data

def decrypt(data: bytes) -> bytes:
    nonce = data[:12]               # first 12 bytes is nonce
    encrypted = data[12:]           # rest is encrypted data
    return cipher.decrypt(nonce, encrypted, None)