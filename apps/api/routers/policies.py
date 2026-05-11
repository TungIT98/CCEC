from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sqlfunc

from models.database import get_db
from models.carbon_credit import Policy, NdcTracking
from models.schemas_carbon import (
    PolicyResponse,
    NdcTrackingResponse,
)
from routers.auth import get_current_user

router = APIRouter(prefix="/policies", tags=["climate-policies"])

db_session = Depends(get_db)


@router.get("", response_model=list[PolicyResponse])
async def list_policies(
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
    country_code: Optional[str] = Query(None),
    policy_type: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List climate policies — paginated, filterable by country/type/sector."""
    try:
        q = select(Policy)
        if country_code:
            q = q.filter(Policy.country_code == country_code)
        if policy_type:
            q = q.filter(Policy.policy_type == policy_type)
        if sector:
            q = q.filter(Policy.sector == sector)

        total = (await db.execute(select(sqlfunc.count()).select_from(Policy))).scalar() or 0
        offset = (page - 1) * page_size
        q = q.offset(offset).limit(page_size)
        result = await db.execute(q)
        records = result.scalars().all()

        return [
            PolicyResponse(
                country_name=str(r.country_name),
                country_code=str(r.country_code),
                policy_name=str(r.policy_name),
                policy_type=str(r.policy_type),
                instrument_type=r.instrument_type,
                sector=r.sector,
                coverage=r.coverage,
                economy_wide=r.economy_wide,
                carbon_pricing_existence=r.carbon_pricing_existence,
                pricing_existence_notes=r.pricing_existence_notes,
                carbon_price_min_tCO2e=r.carbon_price_min_tCO2e,
                carbon_price_max_tCO2e=r.carbon_price_max_tCO2e,
                currency=str(r.currency or "USD"),
                link_source=r.link_source,
                fetched_at=r.fetched_at,
                id=r.id,
            )
            for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ndc", response_model=list[NdcTrackingResponse])
async def list_ndc(
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
):
    """Get NDC (Nationally Determined Contribution) tracking list."""
    try:
        result = await db.execute(select(NdcTracking).limit(200))
        records = result.scalars().all()

        return [
            NdcTrackingResponse(
                country_name=str(r.country_name),
                country_code=str(r.country_code),
                submission_type=r.submission_type,
                status=str(r.status),
                latest_submission_date=r.latest_submission_date,
                link_NDC=r.link_NDC,
                fetch_link=r.fetch_link,
                fetched_at=r.fetched_at,
                id=r.id,
            )
            for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/country/{code}", response_model=list[PolicyResponse])
async def get_country_policies(
    code: str,
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
):
    """Get climate policies for a specific country (ISO 3166-1 code)."""
    try:
        result = await db.execute(
            select(Policy).filter(Policy.country_code == code.upper())
        )
        records = result.scalars().all()

        if not records:
            raise HTTPException(status_code=404, detail=f"Country {code.upper()} not found")

        return [
            PolicyResponse(
                country_name=str(r.country_name),
                country_code=str(r.country_code),
                policy_name=str(r.policy_name),
                policy_type=str(r.policy_type),
                instrument_type=r.instrument_type,
                sector=r.sector,
                coverage=r.coverage,
                economy_wide=r.economy_wide,
                carbon_pricing_existence=r.carbon_pricing_existence,
                pricing_existence_notes=r.pricing_existence_notes,
                carbon_price_min_tCO2e=r.carbon_price_min_tCO2e,
                carbon_price_max_tCO2e=r.carbon_price_max_tCO2e,
                currency=str(r.currency or "USD"),
                link_source=r.link_source,
                fetched_at=r.fetched_at,
                id=r.id,
            )
            for r in records
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{policy_id}", response_model=PolicyResponse)
async def get_policy(
    policy_id: int,
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
):
    """Get climate policy detail by ID."""
    try:
        result = await db.execute(select(Policy).filter(Policy.id == policy_id))
        p = result.scalar_one_or_none()

        if not p:
            raise HTTPException(status_code=404, detail="Policy not found")

        return PolicyResponse(
            country_name=str(p.country_name),
            country_code=str(p.country_code),
            policy_name=str(p.policy_name),
            policy_type=str(p.policy_type),
            instrument_type=p.instrument_type,
            sector=p.sector,
            coverage=p.coverage,
            economy_wide=p.economy_wide,
            carbon_pricing_existence=p.carbon_pricing_existence,
            pricing_existence_notes=p.pricing_existence_notes,
            carbon_price_min_tCO2e=p.carbon_price_min_tCO2e,
            carbon_price_max_tCO2e=p.carbon_price_max_tCO2e,
            currency=str(p.currency or "USD"),
            link_source=p.link_source,
            fetched_at=p.fetched_at,
            id=p.id,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))