from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from models.database import get_db
from models.schemas import TeamMemberResponse, TeamMemberCreate
from models.entities import User, TeamMember
from routers.auth import get_current_user

router = APIRouter(prefix="/team", tags=["team"])


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Admin-only guard — extend role check when role field is added to User."""
    # Currently no role field; all authenticated users can create team members.
    # Restrict this endpoint in production by adding a role column to User.
    return current_user


@router.get("", response_model=List[TeamMemberResponse])
async def list_team_members(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TeamMember).order_by(TeamMember.created_at.desc()))
    return result.scalars().all()


@router.post("", response_model=TeamMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_team_member(
    member: TeamMemberCreate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    # Check for duplicate email
    existing = await db.execute(
        select(TeamMember).where(TeamMember.email == member.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already a team member")

    db_member = TeamMember(user_id=current_user.id, **member.model_dump())
    db.add(db_member)
    await db.commit()
    await db.refresh(db_member)
    return db_member