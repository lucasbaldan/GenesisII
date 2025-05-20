from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session

from api.database.engine import get_session_engine
from api.utils.OAuth2 import get_current_user
from api.database.models import User

T_Session = Annotated[Session, Depends(get_session_engine)]
T_Current_User = Annotated[User, Depends(get_current_user)]
T_OAuth2_Request_Form = Annotated[OAuth2PasswordRequestForm, Depends()]