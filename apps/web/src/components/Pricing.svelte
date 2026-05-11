<section id="pricing" class="py-24 px-6 bg-[#111827]">
  <div class="max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <p class="text-[#A855F7] text-sm font-semibold uppercase tracking-widest mb-3">Pricing</p>
      <h2 class="text-4xl md:text-5xl font-bold text-[#F1F5F9] mb-4">Plans for Every Scale</h2>
      <p class="text-[#94A3B8]">Start free, scale as you grow.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
      {#each [
        {
          tier: 'Free', price: '$0', period: '/month', color: '#94A3B8',
          features: ['5 rigs monitored', 'Real-time dashboard', '7-day data history', 'Community support'],
          cta: 'Start Free',
          highlight: false,
        },
        {
          tier: 'Pro', price: '$49', period: '/month', color: '#00E5A0',
          features: ['50 rigs monitored', 'AI analytics', '90-day data history', 'Email alerts', 'API access'],
          cta: 'Start Pro Trial',
          highlight: true,
        },
        {
          tier: 'Enterprise', price: 'Custom', period: '', color: '#0EA5E9',
          features: ['Unlimited rigs', 'Custom climate models', 'Dedicated support', 'SLA guarantee', 'On-premise option'],
          cta: 'Contact Sales',
          highlight: false,
        },
      ] as plan}
        <div class="rounded-2xl p-8 border {(plan.highlight ? 'bg-[#00E5A0]/5 border-[#00E5A0]/50' : 'bg-[#1E293B] border-[#334155]')}">
          <div class="text-sm font-semibold mb-2" style="color: {plan.color}">{plan.tier}</div>
          <div class="flex items-baseline gap-1 mb-1">
            <span class="text-4xl font-bold text-[#F1F5F9]">{plan.price}</span>
            {#if plan.period}
              <span class="text-[#94A3B8] text-sm">{plan.period}</span>
            {/if}
          </div>
          <ul class="mt-6 space-y-3 mb-8">
            {#each plan.features as feature}
              <li class="flex items-center gap-2 text-sm text-[#94A3B8]">
                <span style="color: {plan.color}">✓</span> {feature}
              </li>
            {/each}
          </ul>
          <a
            href="#"
            class="block text-center py-3 rounded-xl text-sm font-semibold transition-colors {(plan.highlight ? 'bg-[#00E5A0] text-[#0B0F1A] hover:bg-[#00C485]' : 'border border-[#334155] text-[#F1F5F9] hover:border-[#334155]/80')}"
          >
            {plan.cta}
          </a>
        </div>
      {/each}
    </div>
  </div>
</section>
