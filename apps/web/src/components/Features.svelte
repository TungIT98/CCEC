<section id="features" class="py-24 px-6 bg-[#0B0F1A]">
  <div class="max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <p class="text-[#F59E0B] text-sm font-semibold uppercase tracking-widest mb-3">Features</p>
      <h2 class="text-4xl md:text-5xl font-bold text-[#F1F5F9] mb-4">Built for Climate Intelligence</h2>
      <p class="text-[#94A3B8] max-w-2xl mx-auto">
        End-to-end platform for monitoring, analyzing, and optimizing crypto operations under climate constraints.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {#each [
        { icon: '📡', title: 'Real-time Monitoring', desc: 'Live dashboard tracking rig health, energy consumption, and climate metrics across your entire fleet.' },
        { icon: '🤖', title: 'AI Analytics', desc: 'Machine learning models trained on historical data to detect anomalies and predict failures before they happen.' },
        { icon: '🌡️', title: 'Climate Models', desc: 'Integration with regional weather data and climate projections to model operational risk scenarios.' },
        { icon: '🔮', title: 'Forecasting', desc: '7-day energy cost and profitability forecasts based on weather patterns and market conditions.' },
        { icon: '🗺️', title: 'Interactive Maps', desc: 'Geographic visualization of your mining operations with climate risk overlays and efficiency heatmaps.' },
        { icon: '📊', title: 'Open Data', desc: 'Public API and datasets for community research on crypto mining and climate impact.' },
      ] as feature}
        <div class="bg-[#1E293B] rounded-2xl p-6 border border-[#334155] hover:border-[#F59E0B]/50 transition-colors group">
          <div class="text-4xl mb-4">{feature.icon}</div>
          <h3 class="text-xl font-semibold text-[#F1F5F9] mb-2">{feature.title}</h3>
          <p class="text-[#94A3B8] text-sm leading-relaxed">{feature.desc}</p>
        </div>
      {/each}
    </div>
  </div>
</section>
