# /app/routers/login.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

router = APIRouter(tags=["login"])

# In-memory "database" of users (replace with your actual user database)
fake_users_db = {
    "test_user": {
        "username": "test_user",
        "hashed_password": "$2b$12$KIX8F1Wc2wPFh8r9JtWnjeQwgE./vOVnD0nUHRjdS71/teWDH9Q5K",  # hash for 'dlpeye'
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key_here"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    user = fake_users_db.get(username)
    return user

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Optionally, add a logout endpoint if using cookies/sessions
@router.post("/logout")
def logout():
    # In a token-based system, logout is typically handled on the client side by discarding the token.
    return {"message": "Logout successful"}
