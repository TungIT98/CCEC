from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_db
from models.schemas import UserResponse, UserUpdate
from models.entities import User
from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from services.auth import get_password_hash
    if update.full_name is not None:
        current_user.full_name = update.full_name
    if update.password is not None:
        current_user.hashed_password = get_password_hash(update.password)
    await db.commit()
    await db.refresh(current_user)
    return current_user
