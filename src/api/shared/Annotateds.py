from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncEngine

from src.api.database.engine import get_session_engine
from src.api.utils.OAuth2 import get_current_user
from src.api.database.models import User

T_Session = Annotated[AsyncEngine, Depends(get_session_engine)]
T_Current_User = Annotated[User, Depends(get_current_user)]
T_OAuth2_Request_Form = Annotated[OAuth2PasswordRequestForm, Depends()]