from fastapi import APIRouter, HTTPException
from models.users import User
from jwt_manager import create_token


users_router = APIRouter()

# Function to do user login.
@users_router.post('/login', tags=['auth'], status_code=200)
def login(user: User):
    if user.email == 'admin@email.com' and user.password == 'password':
        token: str = create_token(user.model_dump())        # Create a token.
        return {'token': token}
    raise HTTPException(status_code=401, detail='Invalid email or password')