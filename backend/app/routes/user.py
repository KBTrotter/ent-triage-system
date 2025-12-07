"""Routes for managing user accounts.

This module defines CRUD endpoints for users.  Only administrators are
allowed to list, create, update or delete users.  Regular users may
retrieve their own user record via the `/auth/me` endpoint defined in
the authentication routes.  The endpoints in this module rely on the
current user being provided by the authentication dependency; if the
current user is not an administrator a 403 error is raised.
"""

from __future__ import annotations

from typing import List

import uuid  # for converting string IDs to UUID objects

from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from app.core.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.models import (
    User,
    UserPublic,
    UserCreate,
    UserUpdate,
    UsersList,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=UsersList)
def list_users(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UsersList:
    """Return a paginated list of users.

    Only administrators may access this endpoint.  The ``limit`` and
    ``offset`` parameters control pagination.  The response includes
    both the list of users and a count of the total number returned.
    """
    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    statement = select(User).offset(offset).limit(limit)
    results = db.exec(statement).all()
    return UsersList(data=[UserPublic.model_validate(u) for u in results], count=len(results))


@router.get("/{user_id}", response_model=UserPublic)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserPublic:
    """Retrieve a single user by ID.

    Only administrators may access this endpoint.
    """
    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    try:
        user_uuid = uuid.UUID(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="user_id must be a valid UUID")
    user = db.get(User, user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserPublic.model_validate(user)


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserPublic:
    """Create a new user record.

    Only administrators may create users.  This endpoint does not set
    passwords for the new user; password management is deferred to
    another workflow (e.g., invite emails).  Duplicate emails are
    rejected with a 409 error.
    """
    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    # Check for existing email
    existing = db.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    new_user = User(
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        role=payload.role.lower(),
        passwordHash="",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserPublic.model_validate(new_user)


@router.put("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserPublic:
    """Update an existing user record.

    Only administrators may update users.  Fields that are ``None`` in
    the request payload are ignored.  Attempting to update a
    non‑existent user returns a 404.
    """
    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    try:
        user_uuid = uuid.UUID(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="user_id must be a valid UUID")
    user = db.get(User, user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    update_data = payload.model_dump(exclude_unset=True)
    if update_data.get("role"):
        update_data["role"] = update_data["role"].lower()
    for field, value in update_data.items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserPublic.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a user record.

    Only administrators may delete users.  Attempting to delete a
    non‑existent user returns a 404.
    """
    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    try:
        user_uuid = uuid.UUID(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="user_id must be a valid UUID")
    user = db.get(User, user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db.delete(user)
    db.commit()
    return None
