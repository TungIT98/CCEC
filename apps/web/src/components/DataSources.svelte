<section class="py-20 px-6 bg-[#0B0F1A]">
  <div class="max-w-7xl mx-auto text-center">
    <p class="text-[#94A3B8] text-sm font-medium uppercase tracking-widest mb-10">Trusted Data Sources</p>
    <div class="flex flex-wrap items-center justify-center gap-10 md:gap-16 opacity-60">
      {#each ['🌍 OpenWeatherMap', '🌐 NASA POWER', '📡 NOAA', '💨 Electricity Maps', '⛏️ CoinMetrics', '📈 CoinGecko'] as source}
        <span class="text-[#F1F5F9] text-lg font-medium">{source}</span>
      {/each}
    </div>
  </div>
</section>
