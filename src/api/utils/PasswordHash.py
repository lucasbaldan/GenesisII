from datetime import datetime
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """
    Hash a password using the recommended hashing algorithm.
    """
    return pwd_context.hash(password)

def verify_password(password: str, senha_hash: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(password, senha_hash)