"""
Public demo endpoints — no auth required.
Used by landing page to display sample data without login.
"""
import random
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Query

router = APIRouter(prefix="/emissions", tags=["emissions"])


# Vietnam provinces with coordinates
PROVINCES = [
    {"name": "Hà Nội", "code": "HN", "lat": 21.0285, "lng": 105.8542, "pop_m": 8.3},
    {"name": "Hồ Chí Minh", "code": "HCM", "lat": 10.8231, "lng": 106.6297, "pop_m": 9.0},
    {"name": "Đà Nẵng", "code": "DN", "lat": 16.0544, "lng": 108.2022, "pop_m": 1.2},
    {"name": "Hải Phòng", "code": "HP", "lat": 20.8651, "lng": 106.6851, "pop_m": 2.0},
    {"name": "Cần Thơ", "code": "CT", "lat": 10.0452, "lng": 105.7469, "pop_m": 1.2},
    {"name": "Quảng Ninh", "code": "QN", "lat": 21.0137, "lng": 107.0455, "pop_m": 1.3},
    {"name": "Bình Dương", "code": "BD", "lat": 11.1674, "lng": 106.6542, "pop_m": 2.4},
    {"name": "Thanh Hóa", "code": "TH", "lat": 19.7543, "lng": 105.4522, "pop_m": 3.4},
    {"name": "Nghệ An", "code": "NA", "lat": 18.6745, "lng": 105.6987, "pop_m": 3.3},
    {"name": "Bà Rịa Vũng Tàu", "code": "VT", "lat": 10.4806, "lng": 107.0823, "pop_m": 1.1},
]

SECTORS = ["Năng lượng", "Giao thông", "Công nghiệp", "Nông nghiệp", "Chất thải"]

YEARS = [2019, 2020, 2021, 2022, 2023, 2024]


@router.get("")
async def get_emissions_summary(
    year: int = Query(2024, ge=2019, le=2024, description="Năm báo cáo"),
):
    """Public emissions summary for Vietnam by province and sector."""
    provinces = []
    total = 0

    for prov in PROVINCES:
        prov_total = 0
        sectors = []
        for sector in SECTORS:
            # Simulated emissions in kt CO2
            base = round(100 + prov["pop_m"] * 50 + random.uniform(-20, 20), 1)
            if sector == "Năng lượng":
                base *= 2.5
            elif sector == "Giao thông":
                base *= 1.8
            elif sector == "Công nghiệp":
                base *= 1.5
            base = round(base, 1)
            sectors.append({"name": sector, "emissions_kt": base})
            prov_total += base

        prov_total = round(prov_total, 1)
        total += prov_total

        provinces.append({
            "name": prov["name"],
            "code": prov["code"],
            "lat": prov["lat"],
            "lng": prov["lng"],
            "emissions_kt": prov_total,
            "per_capita_t": round(prov_total * 1000 / (prov["pop_m"] * 1_000_000), 3),
            "sectors": sectors,
        })

    return {
        "year": year,
        "total_emissions_kt": round(total, 1),
        "unit": "kt CO2",
        "source": "CCEC Demo Data v0.1",
        "provinces": sorted(provinces, key=lambda p: p["emissions_kt"], reverse=True),
    }


@router.get("/trends")
async def get_emission_trends(
    country: str = Query("VNM", description="ISO country code"),
    years: int = Query(6, ge=2, le=20, description="Number of years"),
):
    """Time-series emission trends (2019–2024)."""
    result = []
    for i, yr in enumerate(YEARS[-years:]):
        # Simulate a gradual increase with some variation
        base_total = 300_000  # kt CO2 for Vietnam
        annual_growth = 0.04  # ~4% per year
        emissions = round(base_total * (1 + annual_growth) ** i + random.uniform(-5000, 5000), 0)
        result.append({
            "year": yr,
            "total_emissions_kt": int(emissions),
            "change_pct": round(emissions / (base_total * (1 + annual_growth) ** max(i - 1, 0)) * 100 - 100, 2) if i > 0 else 0,
            "main_sector": SECTORS[i % len(SECTORS)],
        })
    return {"country": country, "trends": result}


@router.get("/carbon-credits")
async def get_carbon_credits(
    lat: float = Query(21.0285, description="Latitude"),
    lng: float = Query(105.8542, description="Longitude"),
):
    """Sample carbon credit registry (public demo)."""
    return {
        "credits": [
            {
                "id": "CCEC-2024-001",
                "project": "Rừng Đắk Lắk REDD+",
                "location": "Đắk Lắk, Vietnam",
                "lat": 12.7,
                "lng": 108.0,
                "credits_issued": 125_000,
                "credits_sold": 87_500,
                "price_usd": 18.5,
                "status": "active",
                "verification": "Verra VCS",
            },
            {
                "id": "CCEC-2024-002",
                "project": "Năng lượng mặt trời Bình Thuận",
                "location": "Bình Thuận, Vietnam",
                "lat": 10.9,
                "lng": 108.1,
                "credits_issued": 45_000,
                "credits_sold": 22_000,
                "price_usd": 12.0,
                "status": "active",
                "verification": "Gold Standard",
            },
            {
                "id": "CCEC-2024-003",
                "project": "Wind Farm Quảng Trị",
                "location": "Quảng Trị, Vietnam",
                "lat": 16.7,
                "lng": 107.1,
                "credits_issued": 80_000,
                "credits_sold": 35_000,
                "price_usd": 15.0,
                "status": "active",
                "verification": "Verra VCS",
            },
        ],
        "total_registered": 250_000,
        "total_sold": 144_500,
        "market_price_usd": 15.2,
    }