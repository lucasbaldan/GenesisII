from zoneinfo import ZoneInfo
from jwt import encode
from datetime import datetime, timedelta
from api.shared.schemas import SubJWT

import os
from dotenv import load_dotenv

load_dotenv()

jwtSecret = os.getenv("JWT_SECRET")
jwtAlgorithm = os.getenv("JWT_ALGORITHM")
jwtExpireMins = os.getenv("JWT_EXP_MINUTES")

def create_jwt_token(data: SubJWT) -> str:
    """
    Create a JWT token.

    """ 
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=int(jwtExpireMins))

    return encode({
        "exp": expire,
        "sub": data
    }, 
    jwtSecret, 
    algorithm=jwtAlgorithm)