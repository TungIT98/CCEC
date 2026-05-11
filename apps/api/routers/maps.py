from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response

from routers.auth import get_current_user

router = APIRouter(prefix="/maps", tags=["maps"])


@router.get("/tiles/{z}/{x}/{y}", response_class=Response)
async def get_tile(
    z: int,
    x: int,
    y: int,
    _current_user=Depends(get_current_user),
):
    """Proxy tile requests to Mapbox (or return placeholder PNG)."""
    from core.config import settings

    token = settings.MAPBOX_ACCESS_TOKEN
    if not token:
        # Return a minimal transparent 1x1 PNG
        return Response(bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
                              0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52,
                              0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
                              0x08, 0x06, 0x00, 0x00, 0x00, 0x1f, 0x15, 0xc4,
                              0x00, 0x00, 0x00, 0x0a, 0x49, 0x44, 0x41, 0x54,
                              0x78, 0x9c, 0x63, 0x00, 0x01, 0x00, 0x00, 0x05,
                              0x00, 0x01, 0x0d, 0x0a, 0x2d, 0xb4, 0x00, 0x00,
                              0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42,
                              0x60, 0x82]),
                         media_type="image/png")

    import httpx
    tile_url = f"https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token={token}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(tile_url)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Tile fetch failed")
        return Response(content=resp.content, media_type="image/png")
