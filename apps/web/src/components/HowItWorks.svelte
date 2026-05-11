<section class="py-24 px-6 bg-[#111827]">
  <div class="max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <p class="text-[#0EA5E9] text-sm font-semibold uppercase tracking-widest mb-3">How It Works</p>
      <h2 class="text-4xl md:text-5xl font-bold text-[#F1F5F9] mb-4">Three Steps to Climate Intelligence</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {#each [
        { step: '01', title: 'Connect Your Rigs', desc: 'Install our lightweight agent on your mining hardware. Automatic discovery and setup in under 5 minutes.', icon: '🔗' },
        { step: '02', title: 'Analyze & Model', desc: 'Our AI ingests real-time telemetry, weather data, and market feeds to build operational models.', icon: '🧠' },
        { step: '03', title: 'Act on Insights', desc: 'Receive actionable recommendations for energy arbitrage, cooling optimization, and risk mitigation.', icon: '⚡' },
      ] as item, i}
        <div class="relative">
          {#if i < 2}
            <div class="hidden md:block absolute top-10 right-0 translate-x-1/2 z-10">
              <svg width="60" height="24" viewBox="0 0 60 24" fill="none">
                <path d="M0 12 H50 M42 4 L52 12 L42 20" stroke="#334155" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </div>
          {/if}
          <div class="bg-[#1E293B] rounded-2xl p-8 border border-[#334155] text-center">
            <div class="text-5xl mb-4">{item.icon}</div>
            <div class="inline-block px-3 py-1 rounded-full bg-[#0EA5E9]/20 text-[#0EA5E9] text-xs font-bold mb-4">{item.step}</div>
            <h3 class="text-xl font-semibold text-[#F1F5F9] mb-3">{item.title}</h3>
            <p class="text-[#94A3B8] text-sm">{item.desc}</p>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>
