from jwt import encode, decode
from datetime import datetime, timedelta, timezone

import os
from dotenv import load_dotenv

load_dotenv()

jwtSecret = os.getenv("JWT_SECRET")
jwtAlgorithm = os.getenv("JWT_ALGORITHM")
jwtExpireMins = os.getenv("JWT_EXP_MINUTES")

def create_jwt_token(data: int):
    """
    Create a JWT token.

    """ 
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=int(jwtExpireMins))

    jwt = encode({
        "exp": expire,
        "sub": str(data),
    }, 
    jwtSecret, 
    algorithm=jwtAlgorithm)

    return {
        "access_token": jwt,
        "token_type": "bearer",
        "expires": expire 
    }

def decode_jwt_token(token: str) -> int:
    """
    Decode a JWT token.

    """
    payload = decode(
            token, 
            jwtSecret, 
            algorithms=[jwtAlgorithm]
        )
    return int(payload.get("sub"))