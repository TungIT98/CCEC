<script lang="ts">
  import { onMount } from 'svelte';

  let mapContainer: HTMLDivElement;
  let loading = $state(true);
  let error = $state('');
  let activeLayer = $state<'climate' | 'elevation' | 'flood'>('climate');

  onMount(async () => {
    const timeout = setTimeout(() => {
      if (loading) {
        loading = false;
        error = 'Bản đồ không tải được trong 15 giây. Kiểm tra kết nối internet.';
      }
    }, 15_000);

    try {
      const L = (await import('leaflet')).default;
      const m = L.map(mapContainer, { zoomControl: true }).setView([20, 0], 2);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
      }).addTo(m);
      L.control.scale({ position: 'bottomleft' }).addTo(m);
      addGlobalClimateLayers(m, L);
      clearTimeout(timeout);
      loading = false;

      (window as any).ccecRefreshMap = () => {
        m.flyTo([20, 0], 2, { duration: 1.5 });
      };
    } catch (e: any) {
      clearTimeout(timeout);
      error = 'Không thể khởi tạo bản đồ: ' + e.message;
      loading = false;
    }
  });

  function addGlobalClimateLayers(m: any, L: any) {
    // 22 global climate stations across 6 continents
    const globalStations = [
      // Asia
      { name: 'Hà Nội', lat: 21.0285, lng: 105.8542, temp: 28, risk: 'flood', region: 'Asia' },
      { name: 'TP. Hồ Chí Minh', lat: 10.8231, lng: 106.6297, temp: 30, risk: 'flood', region: 'Asia' },
      { name: 'Bắc Kinh', lat: 39.9042, lng: 116.4074, temp: 14, risk: 'low', region: 'Asia' },
      { name: 'New Delhi', lat: 28.6139, lng: 77.2090, temp: 33, risk: 'heat', region: 'Asia' },
      { name: 'Tokyo', lat: 35.6762, lng: 139.6503, temp: 20, risk: 'low', region: 'Asia' },
      { name: 'Jakarta', lat: -6.2088, lng: 106.8456, temp: 31, risk: 'flood', region: 'Asia' },
      { name: 'Bangkok', lat: 13.7563, lng: 100.5018, temp: 32, risk: 'flood', region: 'Asia' },
      { name: 'Đà Nẵng', lat: 16.0544, lng: 108.2024, temp: 27, risk: 'flood', region: 'Asia' },
      { name: 'Moscow', lat: 55.7558, lng: 37.6173, temp: -4, risk: 'cold', region: 'Asia' },
      { name: 'Dubai', lat: 25.2048, lng: 55.2708, temp: 38, risk: 'heat', region: 'Asia' },
      // Europe
      { name: 'London', lat: 51.5074, lng: -0.1278, temp: 12, risk: 'low', region: 'Europe' },
      { name: 'Paris', lat: 48.8566, lng: 2.3522, temp: 14, risk: 'low', region: 'Europe' },
      { name: 'Berlin', lat: 52.5200, lng: 13.4050, temp: 11, risk: 'low', region: 'Europe' },
      { name: 'Athens', lat: 37.9838, lng: 23.7275, temp: 23, risk: 'heat', region: 'Europe' },
      // Americas
      { name: 'New York', lat: 40.7128, lng: -74.0060, temp: 16, risk: 'low', region: 'Americas' },
      { name: 'Los Angeles', lat: 34.0522, lng: -118.2437, temp: 22, risk: 'heat', region: 'Americas' },
      { name: 'São Paulo', lat: -23.5505, lng: -46.6333, temp: 24, risk: 'flood', region: 'Americas' },
      { name: 'Mexico City', lat: 19.4326, lng: -99.1332, temp: 19, risk: 'low', region: 'Americas' },
      // Africa
      { name: 'Lagos', lat: 6.5244, lng: 3.3792, temp: 29, risk: 'flood', region: 'Africa' },
      { name: 'Cairo', lat: 30.0444, lng: 31.2357, temp: 28, risk: 'heat', region: 'Africa' },
      { name: 'Nairobi', lat: -1.2921, lng: 36.8219, temp: 21, risk: 'low', region: 'Africa' },
      { name: 'Johannesburg', lat: -26.2041, lng: 28.0473, temp: 18, risk: 'low', region: 'Africa' },
      // Oceania
      { name: 'Sydney', lat: -33.8688, lng: 151.2093, temp: 21, risk: 'low', region: 'Oceania' },
      { name: 'Melbourne', lat: -37.8136, lng: 144.9631, temp: 17, risk: 'low', region: 'Oceania' },
    ];

    // Regional climate zone overlays
    const climateZones = [
      { bounds: [[-23.5, -180], [23.5, 180]], label: 'Tropical Zone — Hot & Humid', color: '#ef4444', opacity: 0.10 },
      { bounds: [[15, -20], [45, 60]], label: 'Arid — Sahara & Middle East', color: '#f97316', opacity: 0.15 },
      { bounds: [[-35, 15], [-15, 50]], label: 'Arid — Kalahari & Namibia', color: '#f97316', opacity: 0.13 },
      { bounds: [[35, -125], [70, -60]], label: 'Temperate — North America', color: '#14b8a6', opacity: 0.10 },
      { bounds: [[35, -15], [70, 40]], label: 'Temperate — Europe', color: '#14b8a6', opacity: 0.10 },
      { bounds: [[60, -180], [90, 180]], label: 'Cold/Polar — Arctic', color: '#60a5fa', opacity: 0.12 },
      { bounds: [[-90, -180], [-60, 180]], label: 'Cold/Polar — Antarctic', color: '#60a5fa', opacity: 0.12 },
    ];

    climateZones.forEach(z => {
      L.rectangle(z.bounds as [[number, number], [number, number]], {
        color: z.color, weight: 0.5, dashArray: '2 3',
        fillColor: z.color, fillOpacity: z.opacity,
      }).bindPopup(`<b>${z.label}</b>`).addTo(m);
    });

    globalStations.forEach(s => {
      const color = s.risk === 'flood' ? '#ef4444' : s.risk === 'heat' ? '#f97316' : s.risk === 'cold' ? '#60a5fa' : '#14b8a6';
      const icon = L.divIcon({
        html: `<div style="background:${color};width:10px;height:10px;border-radius:50%;border:2px solid white;box-shadow:0 0 4px rgba(0,0,0,0.4)"></div>`,
        iconSize: [10, 10], iconAnchor: [5, 5],
      });
      L.marker([s.lat, s.lng], { icon })
        .bindPopup(`<b>${s.name}</b><br/>Nhiệt độ: ${s.temp}°C<br/>Khu vực: ${s.region}<br/>Rủi ro: ${s.risk}`)
        .addTo(m);
    });

    // Vietnam outline — CO₂ monitoring focus
    const vnCoords: [number, number][] = [
      [23.35, 102.14], [23.12, 106.6], [21.72, 108.47],
      [20.42, 107.18], [18.45, 106.63], [16.06, 106.03],
      [15.26, 108.83], [13.4, 109.36], [11.62, 108.97],
      [10.93, 106.57], [9.85, 105.8], [9.43, 104.34],
      [10.98, 103.5], [12.38, 102.99], [14.7, 102.29],
      [16.2, 102.14], [18.46, 102.14], [22.21, 102.14],
      [23.35, 102.14],
    ];
    L.polygon(vnCoords, { color: '#14b8a6', weight: 1.5, fillColor: '#14b8a6', fillOpacity: 0.15 })
      .bindPopup('<b>Việt Nam</b><br/>Trọng điểm giám sát CO₂').addTo(m);
  }

  function setLayer(name: 'climate' | 'elevation' | 'flood') {
    activeLayer = name;
  }
</script>

<div class="relative w-full h-full">
  {#if error}
    <div class="absolute top-2 left-2 right-2 z-10 bg-red-50 border border-red-300 text-red-700 text-xs p-3 rounded shadow-sm font-medium flex items-center gap-2">
      <svg class="w-4 h-4 text-red-500 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      {error}
    </div>
  {/if}

  <div class="absolute top-2 left-2 z-10 bg-white/90 border border-slate-200 text-slate-600 text-xs px-2.5 py-1.5 rounded-lg shadow-sm flex items-center gap-1.5">
    <svg class="w-3.5 h-3.5 text-amber-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
    OpenStreetMap — Toàn cầu, miễn phí
  </div>

  <div class="absolute top-2 right-2 z-10 flex gap-1.5">
    <button
      onclick={() => setLayer('climate')}
      class="px-2.5 py-1 text-xs rounded-full font-medium transition-colors flex items-center gap-1 {activeLayer === 'climate' ? 'bg-amber-600 text-white' : 'bg-white/90 text-slate-600 hover:bg-white border border-slate-200 shadow-sm'}"
    >
      <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a5 5 0 0 0-5 5v6a5 5 0 0 0 10 0V7a5 5 0 0 0-5-5z"/><path d="M12 2v5m0 0l-3-3m3 3l3-3"/></svg>
      Khí hậu
    </button>
    <button
      onclick={() => setLayer('flood')}
      class="px-2.5 py-1 text-xs rounded-full font-medium transition-colors flex items-center gap-1 {activeLayer === 'flood' ? 'bg-red-500 text-white' : 'bg-white/90 text-slate-600 hover:bg-white border border-slate-200 shadow-sm'}"
    >
      <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
      Ngập lụt
    </button>
    <button
      onclick={() => setLayer('elevation')}
      class="px-2.5 py-1 text-xs rounded-full font-medium transition-colors flex items-center gap-1 {activeLayer === 'elevation' ? 'bg-slate-700 text-white' : 'bg-white/90 text-slate-600 hover:bg-white border border-slate-200 shadow-sm'}"
    >
      <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 20 21 20 12 4 12 20"/></svg>
      Địa hình
    </button>
  </div>

  <div bind:this={mapContainer} class="w-full h-full min-h-64"></div>
  {#if loading}
    <div class="absolute inset-0 flex items-center justify-center bg-slate-100">
      <div class="text-center">
        <div class="w-8 h-8 border-2 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <span class="text-slate-500 text-sm">Đang tải bản đồ...</span>
      </div>
    </div>
  {/if}
</div>