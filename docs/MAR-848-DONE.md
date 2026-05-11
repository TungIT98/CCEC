# MAR-848 — DONE ✅

## Yêu cầu
- Mã nguồn mở, free, real-time trực quan CCEC toàn thế giới
- Bỏ Mapbox (Vietnam-only)
- Global coverage

## Thay đổi

### MapWidget.svelte — Complete rewrite
- **Xóa hoàn toàn**: mapbox-gl import, MAPBOX_TOKEN, MAPBOX_VALID, mapMode state, addGlobalClimateLayersMapbox()
- **Chỉ Leaflet + OpenStreetMap**: No API key, no token, free global tile server
- **Center**: [20, 0] zoom 2 — global view by default
- **22 global climate stations** (6 continents):
  - Asia: Hà Nội, TP.HCM, Đà Nẵng, Bắc Kinh, New Delhi, Tokyo, Jakarta, Bangkok, Moscow, Dubai
  - Europe: London, Paris, Berlin, Athens
  - Americas: New York, Los Angeles, São Paulo, Mexico City
  - Africa: Lagos, Cairo, Nairobi, Johannesburg
  - Oceania: Sydney, Melbourne
- **Climate zone overlays**: Tropical, Arid (Sahara/Middle East), Arid (Kalahari), Temperate (N.Am/EU), Cold/Polar
- **Vietnam outline**: CO₂ monitoring focus, teal polygon
- **Map mode badge**: "OpenStreetMap — Toàn cầu, miễn phí"

### maps.astro — Updated
- Title: "Bản đồ Climate Toàn cầu"
- Subtitle: "Leaflet · OpenStreetMap · Dữ liệu toàn cầu"
- Breadcrumb: "Bản đồ Climate"
- Legend: "Toàn cầu" (thay vì "Vietnam")

### package.json — Clean
- Removed: `mapbox-gl`, `@types/mapbox-gl`
- leaflet@^1.9.4 + @types/leaflet@^1.9.21 retained

### astro.config.mjs — Clean
- Removed mapbox-gl from optimizeDeps.exclude

## Build verification
- ✅ 8 pages in 7.89s, 0 errors
- ✅ MapWidget bundle: **8.55 kB** (vs. 1.78 MB mapbox-gl before)
- ✅ leaflet-src.js (OSM tiles): 150 kB gzipped 43 kB
- ✅ No Mapbox CSS link, no mapbox token reference

## Free global data sources (phase tiếp theo)
- Climate TRACE: emissions toàn cầu
- NOAA Climate Data Online
- NASA Open APIs
- World Bank Climate Portal