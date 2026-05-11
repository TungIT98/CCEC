from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_db
from models.schemas import UserResponse, UserUpdate, UserSettingsResponse, UserSettingsCreate
from models.entities import User, UserSettings
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


@router.get("/settings", response_model=UserSettingsResponse)
async def get_settings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.get(UserSettings, current_user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
    return result


@router.put("/settings", response_model=UserSettingsResponse)
async def update_settings(
    settings_update: UserSettingsCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.get(UserSettings, current_user.id)
    if not result:
        result = UserSettings(user_id=current_user.id)
        db.add(result)
    for field, value in settings_update.model_dump(exclude_unset=True, exclude={"user_id"}).items():
        if value is not None:
            setattr(result, field, value)
    await db.commit()
    await db.refresh(result)
    return result
