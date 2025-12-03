from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.core.security import (verify_password, create_access_token, create_refresh_token, verify_refresh_token, hash_refresh_token)
from app.auth.schemas import LoginRequest, UserResponse, Token
from app.auth.dependencies import get_current_user
from app.models import (User, RefreshToken)
from app.core.dependencies import get_db
from sqlmodel import Session, select
from app.core.config import settings
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

REFRESH_COOKIE_NAME = "refresh_token"

# # Mock users
# fake_users = {
#     "admin": {
#         "userID": 1,
#         "username": "admin",
#         "password": hash_password("adminpass"),  # hashed password
#         "role": "admin",
#         "last_login": None
#     },
#     "user": {
#         "userID": 2,
#         "username": "user",
#         "password": hash_password("userpass"),
#         "role": "user",
#         "last_login": None
#     },
# }

# Login route
@router.post("/login", response_model=Token)
def login(response: Response, data: LoginRequest, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == data.email)).first()

    if not user or not verify_password(data.password, user.passwordHash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.userID), "role": user.role})
    refresh_token = create_refresh_token()
    # refresh_token = create_refresh_token({"sub": str(user.userID)})
    refresh_token_hash = hash_refresh_token(refresh_token)
    rt = RefreshToken(
        token = refresh_token_hash,
        user_id = user.userID,
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked = False
    )
    db.add(rt)
    db.commit()
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="none"
    )
    
    return Token(access_token=access_token)


@router.post("/refresh", response_model=Token)
def refresh(response: Response, request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    stored_token = db.exec(
        select(RefreshToken).where(
            RefreshToken.revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        )
    ).all()

     # Verify provided token against all stored tokens
    matched_token = None
    for rt in stored_token:
        if verify_refresh_token(refresh_token, rt.token):
            matched_token = rt
            break

    if not matched_token:
        raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

    user = db.exec(select(User).where(User.userID == matched_token.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token({"sub": str(user.userID), "role": user.role})
    new_refresh_token = create_refresh_token()
    new_refresh_token_hash = hash_refresh_token(new_refresh_token)

    # Store new token
    new_rt = RefreshToken(
        token=new_refresh_token_hash,
        user_id=user.userID,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    )
    with db.begin():
        stored_token.revoked = True
        db.add(new_rt)

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=new_refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="none"
    )

    return Token(access_token=new_access_token)

@router.post("/logout")
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if refresh_token:
        stored_token = db.exec(
            select(RefreshToken).where(RefreshToken.token == hash_refresh_token(refresh_token))
        ).first()
        if stored_token:
            stored_token.revoked = True
            db.commit()

    response.delete_cookie(REFRESH_COOKIE_NAME)
    return {"detail": "Logged out successfully"}

# Current user info route
@router.get("/me", response_model=UserResponse)
def get_current_user_info(user = Depends(get_current_user)):
    return UserResponse(
        userID=str(user.userID),
        email=user.email,
        role=user.role,
        firstName=user.firstName,
        lastName=user.lastName,
        first_initial=user.firstName[0].upper()
    )



