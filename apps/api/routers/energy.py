from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sqlfunc

from models.database import get_db
from models.renewable_energy import RenewableEnergy
from models.schemas_energy import (
    RenewableEnergyResponse,
    CapacityResponse,
    CapacityByEnergyType,
    TrendsResponse,
    CountryEnergyDetail,
)
from routers.auth import get_current_user

router = APIRouter(prefix="/energy", tags=["renewable-energy"])

db_session = Depends(get_db)


@router.get("/renewable", response_model=list[RenewableEnergyResponse])
async def list_renewable_energy(
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
    country_code: Optional[str] = Query(None),
    energy_type: Optional[str] = Query(None),
    year_min: Optional[int] = Query(None),
    year_max: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
):
    """Get renewable energy data — filtered by country/energy type."""
    try:
        q = select(RenewableEnergy)
        if country_code:
            q = q.filter(RenewableEnergy.country_code == country_code)
        if energy_type:
            q = q.filter(RenewableEnergy.energy_type == energy_type)
        if year_min:
            q = q.filter(RenewableEnergy.installed_year >= year_min)
        if year_max:
            q = q.filter(RenewableEnergy.installed_year <= year_max)

        total = (await db.execute(select(sqlfunc.count()).select_from(RenewableEnergy))).scalar() or 0
        offset = (page - 1) * page_size
        q = q.offset(offset).limit(page_size)
        result = await db.execute(q)
        records = result.scalars().all()

        return [
            RenewableEnergyResponse(
                id=r.id,
                country_name=r.country_name,
                country_code=r.country_code,
                energy_type=r.energy_type,
                capacity_mw=r.capacity_mw,
                generation_gwh=r.generation_gwh,
                installed_year=r.installed_year,
                source=r.source,
                fetched_at=r.fetched_at,
            )
            for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capacity", response_model=CapacityResponse)
async def list_energy_capacity(
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
):
    """Get global renewable energy capacity — grouped by energy type."""
    try:
        # All records
        result = await db.execute(select(RenewableEnergy).limit(500))
        records = result.scalars().all()

        # Aggregate by energy type
        agg_result = await db.execute(
            select(
                RenewableEnergy.energy_type,
                sqlfunc.count(RenewableEnergy.id).label("count_records"),
                sqlfunc.sum(RenewableEnergy.capacity_mw).label("total_capacity_mw"),
            )
            .group_by(RenewableEnergy.energy_type)
        )
        agg = agg_result.all()

        by_energy = [
            CapacityByEnergyType(
                energy_type=str(r.energy_type),
                total_capacity_mw=float(r.total_capacity_mw or 0),
                count_records=int(r.count_records),
            )
            for r in agg
        ]

        return CapacityResponse(
            records=[
                RenewableEnergyResponse(
                    id=r.id,
                    country_name=r.country_name,
                    country_code=r.country_code,
                    energy_type=r.energy_type,
                    capacity_mw=r.capacity_mw,
                    generation_gwh=r.generation_gwh,
                    installed_year=r.installed_year,
                    source=r.source,
                    fetched_at=r.fetched_at,
                )
                for r in records
            ],
            by_energy_type=by_energy,
            total_count=len(records),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends", response_model=list[TrendsResponse])
async def list_energy_trends(
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
    country_code: Optional[str] = Query(None),
    energy_type: Optional[str] = Query(None),
):
    """Get renewable energy generation trends — yearly aggregation."""
    try:
        q = select(RenewableEnergy)
        if country_code:
            q = q.filter(RenewableEnergy.country_code == country_code)
        if energy_type:
            q = q.filter(RenewableEnergy.energy_type == energy_type)

        agg_result = await db.execute(
            select(
                RenewableEnergy.country_code,
                RenewableEnergy.country_name,
                RenewableEnergy.energy_type,
                RenewableEnergy.installed_year.label("year"),
                sqlfunc.sum(RenewableEnergy.generation_gwh).label("yearly_generation_gwh"),
            )
            .group_by(
                RenewableEnergy.country_code,
                RenewableEnergy.country_name,
                RenewableEnergy.energy_type,
                RenewableEnergy.installed_year.label("year"),
            )
            .order_by(RenewableEnergy.country_code, RenewableEnergy.energy_type)
        )
        agg = agg_result.all()

        return [
            TrendsResponse(
                country_code=str(r.country_code),
                country_name=str(r.country_name),
                energy_type=str(r.energy_type),
                yearly_generation_gwh=float(r.yearly_generation_gwh or 0),
                year=int(r.year),
            )
            for r in agg
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/country/{code}", response_model=CountryEnergyDetail)
async def get_country_energy(
    code: str,
    db: AsyncSession = db_session,
    _: None = Depends(get_current_user),
):
    """Get renewable energy detail for a specific country (ISO 3166-1 code)."""
    try:
        result = await db.execute(
            select(RenewableEnergy)
            .filter(RenewableEnergy.country_code == code.upper())
        )
        records = result.scalars().all()

        if not records:
            raise HTTPException(status_code=404, detail=f"Country {code.upper()} not found")

        country_name = records[0].country_name

        agg_result = await db.execute(
            select(
                RenewableEnergy.energy_type,
                sqlfunc.sum(RenewableEnergy.capacity_mw).label("total_capacity_mw"),
            )
            .filter(RenewableEnergy.country_code == code.upper())
            .group_by(RenewableEnergy.energy_type)
        )
        agg = agg_result.all()
        by_energy_type = {str(r.energy_type): float(r.total_capacity_mw or 0) for r in agg}

        total_capacity = sum(r.capacity_mw for r in records)

        return CountryEnergyDetail(
            country_code=str(code.upper()),
            country_name=str(country_name),
            records=[
                RenewableEnergyResponse(
                    id=r.id,
                    country_name=r.country_name,
                    country_code=r.country_code,
                    energy_type=r.energy_type,
                    capacity_mw=r.capacity_mw,
                    generation_gwh=r.generation_gwh,
                    installed_year=r.installed_year,
                    source=r.source,
                    fetched_at=r.fetched_at,
                )
                for r in records
            ],
            total_capacity_mw=float(total_capacity),
            by_energy_type=by_energy_type,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))