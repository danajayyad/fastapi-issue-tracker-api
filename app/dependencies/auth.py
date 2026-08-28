# An instance of OAuth2PasswordBearer class
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.logger import logger 
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from jose import JWTError , jwt
from ..models.user import Users 
from app.database.database import db_dependency
from ..core.config import settings


oath2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
token_dependency = Annotated[str, Depends(oath2_bearer)]



# for protected endpoint (after login)
# Behind the scenes inside FastAPI framework:
# token = await oauth2_bearer.__call__(request)
async def get_current_user(token: token_dependency, db : db_dependency):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credintials', headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        role : str = payload.get('role')
        
        if username is None or user_id is None or role is None:
            logger.warning('JWT payload missing required claims: sub, id, or role')
            raise credentials_exception
        
    except JWTError as e:
        logger.warning(f"JWT decoding failed: {e}")
        raise credentials_exception
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        logger.warning(f'User with ID {user_id} from valid token not found in DB')
        raise credentials_exception
    return user

user_dependency = Annotated[Users, Depends(get_current_user)]