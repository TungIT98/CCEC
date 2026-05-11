from datetime import timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sqlfunc

from models.database import get_db
from models.carbon_credit import CarbonCredit, CarbonPrice
from models.schemas_carbon import (
    CarbonCreditResponse,
    CarbonPricesQuery,
)
from routers.auth import get_current_user

router = APIRouter(prefix="/carbon-credits", tags=["carbon-credits"])

db_session = Depends(get_db)


def _credit_response(cc: CarbonCredit) -> CarbonCreditResponse:
    return CarbonCreditResponse(
        id=cc.id,
        name=cc.name,
        standard_type=cc.standard_type,
        project_type=cc.project_type,
        vintage=cc.vintage,
        unit_price=cc.unit_price,
        currency=cc.currency,
        registry=cc.registry,
        project_url=cc.project_url,
        credit_class=cc.credit_class,
        methodology=cc.methodology,
        estimated_ERt=cc.estimated_ERt,
        verified_ERt=cc.verified_ERt,
        issued_at=cc.issued_at,
        expired_at=cc.expired_at,
        is_retired=cc.is_retired,
        country_code=cc.country_code,
        country_name=cc.country_name,
        created_at=cc.created_at,
    )


@router.get("", response_model=list[CarbonCreditResponse])
async def list_carbon_credits(
    db: AsyncSession = db_session,
    user: None = Depends(get_current_user),
    standard_type: Optional[str] = Query(None),
    vintage_min: Optional[int] = Query(None),
    vintage_max: Optional[int] = Query(None),
    project_type: Optional[str] = Query(None),
    country_code: Optional[str] = Query(None),
    unit_price_min: Optional[float] = Query(None),
    unit_price_max: Optional[float] = Query(None),
    is_retired: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List carbon credits — paginated, filterable by standard/vintage/project."""
    try:
        q = select(CarbonCredit)
        if standard_type:
            q = q.filter(CarbonCredit.standard_type == standard_type)
        if vintage_min:
            q = q.filter(CarbonCredit.vintage >= vintage_min)
        if vintage_max:
            q = q.filter(CarbonCredit.vintage <= vintage_max)
        if project_type:
            q = q.filter(CarbonCredit.project_type == project_type)
        if country_code:
            q = q.filter(CarbonCredit.country_code == country_code)
        if unit_price_min:
            q = q.filter(CarbonCredit.unit_price >= unit_price_min)
        if unit_price_max:
            q = q.filter(CarbonCredit.unit_price <= unit_price_max)
        if is_retired is not None:
            q = q.filter(CarbonCredit.is_retired == is_retired)

        count_q = select(sqlfunc.count()).select_from(CarbonCredit)
        if standard_type:
            count_q = count_q.filter(CarbonCredit.standard_type == standard_type)
        if vintage_min:
            count_q = count_q.filter(CarbonCredit.vintage >= vintage_min)
        if vintage_max:
            count_q = count_q.filter(CarbonCredit.vintage <= vintage_max)
        if project_type:
            count_q = count_q.filter(CarbonCredit.project_type == project_type)
        if country_code:
            count_q = count_q.filter(CarbonCredit.country_code == country_code)
        if unit_price_min:
            count_q = count_q.filter(CarbonCredit.unit_price >= unit_price_min)
        if unit_price_max:
            count_q = count_q.filter(CarbonCredit.unit_price <= unit_price_max)
        if is_retired is not None:
            count_q = count_q.filter(CarbonCredit.is_retired == is_retired)

        total = (await db.execute(count_q)).scalar() or 0
        offset = (page - 1) * page_size
        q = q.offset(offset).limit(page_size)
        result = await db.execute(q)
        records = result.scalars().all()

        return [_credit_response(r) for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{credit_id}", response_model=CarbonCreditResponse)
async def get_carbon_credit(
    credit_id: int,
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
):
    """Get carbon credit detail by ID."""
    try:
        result = await db.execute(select(CarbonCredit).filter(CarbonCredit.id == credit_id))
        cc = result.scalar_one_or_none()
        if not cc:
            raise HTTPException(status_code=404, detail="Carbon credit not found")
        return _credit_response(cc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Prices ─────────────────────────────────────────────────────────────────────

from models.schemas_carbon import CarbonPriceResponse


@router.get("/prices", response_model=list[CarbonPriceResponse])
async def list_carbon_prices(
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
    standard_type: Optional[str] = Query(None),
    vintage: Optional[int] = Query(None),
):
    """Get current carbon credit prices (latest per standard/vintage)."""
    try:
        q = select(CarbonPrice)
        if standard_type:
            q = q.filter(CarbonPrice.standard_type == standard_type)
        if vintage:
            q = q.filter(CarbonPrice.vintage == vintage)
        q = q.order_by(CarbonPrice.fetched_at.desc())
        result = await db.execute(q.limit(100))
        records = result.scalars().all()

        return [
            CarbonPriceResponse(
                id=r.id,
                standard_type=r.standard_type,
                vintage=r.vintage,
                price_per_tCO2e=r.price_per_tCO2e,
                currency=r.currency,
                source_url=r.source_url,
                fetched_at=r.fetched_at,
            )
            for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from models.schemas_carbon import CarbonPriceHistoryResponse


@router.get("/prices/history", response_model=list[CarbonPriceHistoryResponse])
async def carbon_prices_history(
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
    standard_type: Optional[str] = Query(None),
    vintage: Optional[int] = Query(None),
    after: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
):
    """Get historical carbon prices — filtered by standard/vintage/date."""
    try:
        from datetime import datetime

        q = select(CarbonPrice)
        if standard_type:
            q = q.filter(CarbonPrice.standard_type == standard_type)
        if vintage:
            q = q.filter(CarbonPrice.vintage == vintage)
        if after:
            try:
                after_dt = datetime.fromisoformat(after.replace("Z", "+00:00"))
                q = q.filter(CarbonPrice.fetched_at >= after_dt)
            except ValueError:
                pass
        q = q.order_by(CarbonPrice.fetched_at.asc())
        result = await db.execute(q.limit(limit))
        records = result.scalars().all()

        return [
            CarbonPriceHistoryResponse(
                id=r.id,
                standard_type=r.standard_type,
                vintage=r.vintage,
                price_per_tCO2e=r.price_per_tCO2e,
                currency=r.currency,
                source_url=r.source_url,
                fetched_at=r.fetched_at,
            )
            for r in records
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))