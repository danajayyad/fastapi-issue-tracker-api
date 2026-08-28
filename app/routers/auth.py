from fastapi import APIRouter, HTTPException
from starlette import status
from app.core.security import create_access_token, hash_password, verify_password
from ..models.user import Users
from ..schemas.user import CreateUserRequest, LoginRequest, TokenResponse
from app.database.database import db_dependency



router = APIRouter(prefix='/auth', tags=['auth'])


# sign up
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        username = create_user_request.username,
        role= create_user_request.role,
        hashed_password = hash_password(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    
    

# login 
@router.post("/login", response_model=TokenResponse)
async def login(db: db_dependency, credintials: LoginRequest):
    user = db.query(Users).filter(Users.username == credintials.username).first()
    if not user or not verify_password(credintials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    token_data = {'sub' : user.username, 'id' : user.id, 'role': user.role}
    token = create_access_token(token_data)
    return {'access_token' : token , 'token_type' : 'bearer'}
