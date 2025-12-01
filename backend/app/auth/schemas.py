from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    userID: int
    username: str
    role: str
    first_initial: str
    