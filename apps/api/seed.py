"""Seed data for carbon credits, energy, and climate policies."""

import asyncio
from datetime import datetime as DT, timezone
import random

from models.database import async_session_maker, init_db
from models.carbon_credit import CarbonCredit, CarbonPrice, RenewableEnergy, Policy, NdcTracking


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)

CC_DATA = [
    {"name": "Gorongo-North REDD+", "std": "VER", "type": "AR-34", "v": 2022,
     "price": 14.20, "reg": "Verra", "cc": "VCS-VER", "et": 850000.0, "vt": 836000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Gorongo-North REDD+", "std": "VER", "type": "AR-34", "v": 2023,
     "price": 15.10, "reg": "Verra", "cc": "VCS-VER", "et": 850000.0, "vt": 836000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Gorou-North REDD+", "std": "VER", "type": "AR-34", "v": 2024,
     "price": 16.80, "reg": "Verra", "cc": "VCS-VER", "et": 850000.0, "vt": 836000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Gorou-North REDD+", "std": "VER", "type": "AR-34", "v": 2025,
     "price": 18.20, "reg": "Verra", "cc": "VCS-VER", "et": 850000.0, "vt": 836000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Biali-North REFDC+", "std": "VER", "type": "AR-27", "v": 2022,
     "price": 13.50, "reg": "Verra", "cc": "CCB-Plus-Gold-VER", "et": 420000.0, "vt": 410000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Biali-North REFDC+", "std": "VER", "type": "AR-27", "v": 2023,
     "price": 14.00, "reg": "Verra", "cc": "CCB-Plus-Gold-VER", "et": 420000.0, "vt": 410000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Cambodge-North REFDC+", "std": "GOLD", "type": "AR-34", "v": 2022,
     "price": 18.50, "reg": "Gold Standard", "cc": "GS-VER", "et": 700000.0, "vt": 690000.0,
     "country_code": "KHM", "country_name": "Cambodia"},
    {"name": "Cambodge-North REFDC+", "std": "GOLD", "type": "AR-34", "v": 2023,
     "price": 19.20, "reg": "Gold Standard", "cc": "GS-VER", "et": 700000.0, "vt": 690000.0,
     "country_code": "KHM", "country_name": "Cambodia"},
    {"name": "Biali2 REFDC+", "std": "VER", "type": "AR-27", "v": 2023,
     "price": 14.50, "reg": "Verra", "cc": "VCS-VER", "et": 400000.0, "vt": 390000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Gorou2 REFDC+", "std": "VER", "type": "AR-34", "v": 2023,
     "price": 14.80, "reg": "Gold Standard", "cc": "GS-VER", "et": 900000.0, "vt": 880000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Gorou REFDC+", "std": "VER", "type": "AR-34", "v": 2024,
     "price": 16.00, "reg": "Gold Standard", "cc": "GS-VER", "et": 900000.0, "vt": 880000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Gorou3 REFDC+", "std": "GOLD", "type": "AR-34", "v": 2025,
     "price": 19.50, "reg": "Gold Standard", "cc": "GS-VER", "et": 950000.0, "vt": 930000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
    {"name": "Gorou4 REFDC+", "std": "GOLD", "type": "AR-34", "v": 2025,
     "price": 19.80, "reg": "Gold Standard", "cc": "GS-VER", "et": 950000.0, "vt": 930000.0,
     "country_code": "KHM", "country_name": "Cambodia"},
    {"name": "Gorou5 REFDC+", "std": "VER", "type": "AR-34", "v": 2025,
     "price": 17.00, "reg": "Verra", "cc": "VCS-VER", "et": 870000.0, "vt": 850000.0,
     "country_code": "VNM", "country_name": "Vietnam"},
]

ENERGY_DATA = [
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "solar",
     "cap": 18500.0, "gen": 27000.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "wind",
     "cap": 12500.0, "gen": 38000.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "hydro",
     "cap": 4500.0, "gen": 42000.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "biomass",
     "cap": 450.0, "gen": 2100.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "solar",
     "cap": 20700.0, "gen": 30000.0, "yr": 2024, "src": "IRENA"},
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "wind",
     "cap": 14500.0, "gen": 44000.0, "yr": 2024, "src": "IRENA"},
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "hydro",
     "cap": 4800.0, "gen": 45000.0, "yr": 2024, "src": "IRENA"},
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "solar",
     "cap": 22900.0, "gen": 33000.0, "yr": 2025, "src": "IRENA"},
    {"country_name": "Vietnam", "country_code": "VNM", "energy_type": "wind",
     "cap": 16000.0, "gen": 49000.0, "yr": 2025, "src": "IRENA"},
    {"country_name": "India", "country_code": "IND", "energy_type": "solar",
     "cap": 62000.0, "gen": 88000.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "India", "country_code": "IND", "energy_type": "wind",
     "cap": 43000.0, "gen": 80000.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "India", "country_code": "IND", "energy_type": "hydro",
     "cap": 47000.0, "gen": 158000.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "India", "country_code": "IND", "energy_type": "solar",
     "cap": 72000.0, "gen": 105000.0, "yr": 2024, "src": "IRENA"},
    {"country_name": "India", "country_code": "IND", "energy_type": "wind",
     "cap": 47000.0, "gen": 92000.0, "yr": 2024, "src": "IRENA"},
    {"country_name": "Thailand", "country_code": "THA", "energy_type": "solar",
     "cap": 6800.0, "gen": 9800.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "Thailand", "country_code": "THA", "energy_type": "wind",
     "cap": 1870.0, "gen": 3800.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "Thailand", "country_code": "THA", "energy_type": "hydro",
     "cap": 3200.0, "gen": 8200.0, "yr": 2023, "src": "IRENA"},
    {"country_name": "Thailand", "country_code": "THA", "energy_type": "solar",
     "cap": 7800.0, "gen": 11000.0, "yr": 2024, "src": "IRENA"},
    {"country_name": "Singapore", "country_code": "SGP", "energy_type": "solar",
     "cap": 2200.0, "gen": 3100.0, "yr": 2023, "src": "GEM"},
    {"country_name": "Singapore", "country_code": "SGP", "energy_type": "solar",
     "cap": 2800.0, "gen": 4000.0, "yr": 2024, "src": "GEM"},
]

POLICY_DATA = [
    {"country_name": "Vietnam", "country_code": "VNM",
     "policy_name": "Power Fixed Price", "policy_type": "ETS",
     "instrument": "Cap-and-trade", "sector": "Energy",
     "coverage": "Power sector", "ew": "Yes",
     "cp": "Yes", "cp_min": 1.0, "cp_max": 5.0, "cur": "USD",
     "link": "https://carbonpricingdashboard.worldbank.org"},
    {"country_name": "Vietnam", "country_code": "VNM",
     "policy_name": "EVN Fixed ETS Price", "policy_type": "ETS",
     "instrument": "Cap-and-trade", "sector": "Energy",
     "coverage": "Power sector", "ew": "Yes",
     "cp": "Yes", "cp_min": 2.0, "cp_max": 8.0, "cur": "USD",
     "link": "https://carbonpricingdashboard.worldbank.org"},
    {"country_name": "Vietnam", "country_code": "VNM",
     "policy_name": "NDC on renewable", "policy_type": "Feed-in Tariff",
     "instrument": "FiT", "sector": "Energy",
     "coverage": "Solar, Wind", "ew": "Yes",
     "cp": "No", "cp_min": None, "cp_max": None, "cur": "VND",
     "link": "https://unfccc.int"},
    {"country_name": "Vietnam", "country_code": "VNM",
     "policy_name": "Net-Zero by 2050", "policy_type": "Strategy",
     "instrument": "Strategy", "sector": "Cross-sector",
     "coverage": "Economy-wide", "ew": "Yes",
     "cp": "Under", "cp_min": 5.0, "cp_max": 15.0, "cur": "USD",
     "link": "https://unfccc.int"},
    {"country_name": "Thailand", "country_code": "THA",
     "policy_name": "TGO ETS Fixed Price", "policy_type": "ETS",
     "instrument": "Cap-and-trade", "sector": "Energy",
     "coverage": "Power sector", "ew": "Yes",
     "cp": "Yes", "cp_min": 2.5, "cp_max": 10.0, "cur": "USD",
     "link": "https://carbonpricingdashboard.worldbank.org"},
    {"country_name": "Thailand", "country_code": "THA",
     "policy_name": "S下一ET Fixed Price", "policy_type": "ETS",
     "instrument": "Cap-and-trade", "sector": "Energy",
     "coverage": "Power sector", "ew": "Yes",
     "cp": "Yes", "cp_min": 2.5, "cp_max": 10.0, "cur": "USD",
     "link": "https://carbonpricingdashboard.worldbank.org"},
    {"country_name": "India", "country_code": "IND",
     "policy_name": "PAT-Schem-e ETS", "policy_type": "ETS",
     "instrument": "Cap-and-trade", "sector": "Energy",
     "coverage": "Energy-intensive", "ew": "No",
     "cp": "Yes", "cp_min": 1.0, "cp_max": 15.0, "cur": "USD",
     "link": "https://carbonpricingdashboard.worldbank.org"},
    {"country_name": "Germany", "country_code": "DEU",
     "policy_name": "EU-ETS Allowance", "policy_type": "ETS",
     "instrument": "Cap-and-trade", "sector": "Cross-sector",
     "coverage": "Economy-wide", "ew": "Yes",
     "cp": "Yes", "cp_min": 25.0, "cp_max": 90.0, "cur": "EUR",
     "link": "https://ec.europa.eu"},
    {"country_name": "United Kingdom", "country_code": "GBR",
     "policy_name": "UK-ETS Allowance", "policy_type": "ETS",
     "instrument": "Cap-and-trade", "sector": "Cross-sector",
     "coverage": "Economy-wide", "ew": "Yes",
     "cp": "Yes", "cp_min": 30.0, "cp_max": 95.0, "cur": "GBP",
     "link": "https://uk-ets.adm.eu"},
]

NDC_DATA = [
    {"country_name": "Vietnam", "country_code": "VNM",
     "sub_type": "Second", "status": "Submitted",
     "ndc_link": "https://unfccc.int/vietnam-ndc",
     "fetch_link": "https://unfccc.int/vnm-ndc"},
    {"country_name": "Vietnam", "country_code": "VNM",
     "sub_type": "Third", "status": "Submitted",
     "ndc_link": "https://unfccc.int/vietnam-ndc",
     "fetch_link": "https://unfccc.int/vnm-ndc3"},
    {"country_name": "Thailand", "country_code": "THA",
     "sub_type": "Second", "status": "Submitted",
     "ndc_link": "https://unfccc.int/thailand-ndc",
     "fetch_link": "https://unfccc.int/tha-ndc"},
    {"country_name": "India", "country_code": "IND",
     "sub_type": "Third", "status": "Submitted",
     "ndc_link": "https://unfccc.int/india-ndc",
     "fetch_link": "https://unfccc.int/ind-ndc"},
    {"country_name": "Singapore", "country_code": "SGP",
     "sub_type": "First", "status": "Under Review",
     "ndc_link": "https://unfccc.int/sgp-ndc",
     "fetch_link": "https://unfccc.int/sgp-ndc"},
    {"country_name": "Cambodia", "country_code": "KHM",
     "sub_type": "Second", "status": "Submitted",
     "ndc_link": "https://unfccc.int/khm-ndc",
     "fetch_link": "https://unfccc.int/khm-ndc"},
    {"country_name": "Germany", "country_code": "DEU",
     "sub_type": "Third", "status": "Submitted",
     "ndc_link": "https://unfccc.int/deu-ndc",
     "fetch_link": "https://ec.europa.eu"},
    {"country_name": "United Kingdom", "country_code": "GBR",
     "sub_type": "Third", "status": "Pending",
     "ndc_link": "https://unfccc.int/gbr-ndc",
     "fetch_link": "https://unfccc.int/gbr-ndc"},
]


async def seed_all():
    from datetime import datetime as DT

    await init_db()

    async with async_session_maker() as db:
        try:
            from sqlalchemy import select, func

            result = await db.execute(select(func.count()).select_from(CarbonCredit))
            if (result.scalar() or 0) > 0:
                print("[seed] Already seeded — skip.")
                return

            for d in CC_DATA:
                cc = CarbonCredit(
                    name=d["name"], standard_type=d["std"],
                    project_type=d["type"], vintage=d["v"],
                    unit_price=d["price"], currency="USD",
                    registry=d["reg"], credit_class=d["cc"],
                    estimated_ERt=d["et"], verified_ERt=d["vt"],
                    issued_at=DT(d["v"], 1, 1, tzinfo=timezone.utc),
                    expired_at=DT(d["v"] + 7, 1, 1, tzinfo=timezone.utc),
                    is_retired=False,
                    country_code=d["country_code"], country_name=d["country_name"],
                    created_at=NOW,
                )
                db.add(cc)

            result = await db.execute(select(CarbonPrice).limit(1))
            if result.scalar_one_or_none() is None:
                for m in range(2022, 2026):
                    for std in ["VER", "GOLD"]:
                        cp = CarbonPrice(
                            standard_type=std, vintage=m,
                            price_per_tCO2e=round(10 + (m - 2022) * 2 + random.uniform(-0.5, 2.5), 2),
                            currency="USD",
                            source_url="https://registry.verra.org",
                            fetched_at=DT(m, 6, 1, tzinfo=timezone.utc),
                        )
                        db.add(cp)

            for d in ENERGY_DATA:
                re = RenewableEnergy(
                    country_name=d["country_name"], country_code=d["country_code"],
                    energy_type=d["energy_type"],
                    capacity_mw=d["cap"], generation_gwh=d["gen"],
                    installed_year=d["yr"], source=d["src"],
                    fetched_at=NOW,
                )
                db.add(re)

            for d in POLICY_DATA:
                p = Policy(
                    country_name=d["country_name"], country_code=d["country_code"],
                    policy_name=d["policy_name"], policy_type=d["policy_type"],
                    instrument_type=d["instrument"], sector=d["sector"],
                    coverage=d["coverage"], economy_wide=d["ew"],
                    carbon_pricing_existence=d["cp"],
                    carbon_price_min_tCO2e=d.get("cp_min"),
                    carbon_price_max_tCO2e=d.get("cp_max"),
                    currency=d["cur"], link_source=d["link"],
                    fetched_at=DT(2025, 6, 1, tzinfo=timezone.utc),
                )
                db.add(p)

            for d in NDC_DATA:
                n = NdcTracking(
                    country_name=d["country_name"], country_code=d["country_code"],
                    submission_type=d["sub_type"], status=d["status"],
                    latest_submission_date=DT(2023, 10, 1, tzinfo=timezone.utc),
                    link_NDC=d["ndc_link"], fetch_link=d["fetch_link"],
                    fetched_at=DT(2025, 6, 1, tzinfo=timezone.utc),
                )
                db.add(n)

            await db.commit()
            print("[seed] Done.")
        except Exception as e:
            await db.rollback()
            print(f"[seed] Error: {e}")


if __name__ == "__main__":
    asyncio.run(seed_all())