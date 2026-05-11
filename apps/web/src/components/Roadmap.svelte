<section id="roadmap" class="py-24 px-6 bg-[#0B0F1A]">
  <div class="max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <p class="text-[#F59E0B] text-sm font-semibold uppercase tracking-widest mb-3">Roadmap</p>
      <h2 class="text-4xl md:text-5xl font-bold text-[#F1F5F9] mb-4">What's Coming</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {#each [
        {
          quarter: 'Q2 2026', color: '#F59E0B',
          items: ['Core platform launch', 'Real-time rig monitoring', 'OpenWeatherMap integration', 'Free tier'],
        },
        {
          quarter: 'Q3 2026', color: '#0EA5E9',
          items: ['AI anomaly detection', 'Multi-region support', 'Ethereum hashrate integration', 'Pro tier launch'],
        },
        {
          quarter: 'Q4 2026', color: '#A855F7',
          items: ['Predictive energy arbitrage', 'Custom climate models API', 'Enterprise tier', 'Mobile app'],
        },
      ] as column}
        <div class="bg-[#1E293B] rounded-2xl p-6 border border-[#334155]">
          <div class="inline-block px-3 py-1 rounded-full text-xs font-bold mb-4" style="background-color: {column.color}20; color: {column.color}">
            {column.quarter}
          </div>
          <ul class="space-y-3">
            {#each column.items as item}
              <li class="flex items-start gap-2 text-sm text-[#94A3B8]">
                <span style="color: {column.color}">→</span> {item}
              </li>
            {/each}
          </ul>
        </div>
      {/each}
    </div>
  </div>
</section>
