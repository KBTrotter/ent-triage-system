from fastapi import APIRouter, HTTPException, Depends
from app.auth.schemas import Token
from app.core.security import (verify_password, create_access_token, hash_password)
from app.auth.schemas import LoginRequest, UserResponse
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])

# Mock users
fake_users = {
    "admin": {
        "userID": 1,
        "username": "admin",
        "password": hash_password("adminpass"),  # hashed password
        "role": "admin",
        "last_login": None
    },
    "user": {
        "userID": 2,
        "username": "user",
        "password": hash_password("userpass"),
        "role": "user",
        "last_login": None
    },
}

# Login route
@router.post("/login", response_model=Token)
def login(payload: LoginRequest):
    user = fake_users.get(payload.username)

    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(str(user["userID"]))
    
    return Token(access_token=access_token)

# Current user info route
@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    for user in fake_users.values():
        if str(user["userID"]) == current_user["userID"]:
            return {
                "userID": user["userID"],
                "username": user["username"],
                "role": user["role"],
                "first_initial": user["username"][0].upper()
            }
    raise HTTPException(status_code=404, detail="User not found")


