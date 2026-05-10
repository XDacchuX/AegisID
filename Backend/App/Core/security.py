import hashlib
import json
from cryptography.fernet import Fernet
from app.core.config import settings

fernet = Fernet(settings.FERNET_KEY.encode())

def hash_descriptor(descriptor: list) -> str:
    """SHA-256 hash of face descriptor for blockchain"""
    return hashlib.sha256(json.dumps(descriptor).encode()).hexdigest()

def encrypt_data(data: bytes) -> bytes:
    """AES encryption for w3up storage"""
    return fernet.encrypt(data)

def decrypt_data(token: bytes) -> bytes:
    """Decrypt data from w3up"""
    return fernet.decrypt(token)
