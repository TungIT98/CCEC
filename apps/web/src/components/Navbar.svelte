<script lang="ts">
  const navLinks = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Emissions', href: '/emissions' },
    { label: 'ESG', href: '/esg' },
    { label: 'Carbon Credits', href: '/carbon-credits' },
    { label: 'Energy', href: '/energy' },
    { label: 'Policies', href: '/policies' },
    { label: 'Forecast', href: '/forecast' },
  ];
</script>

<nav class="fixed top-0 w-full z-50 bg-[#0B0F1A]/90 backdrop-blur-md border-b border-[#334155]">
  <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
    <!-- Logo -->
    <a href="/" class="flex items-center gap-2">
      <div class="w-8 h-8 rounded-lg bg-[#F59E0B] flex items-center justify-center">
        <span class="text-[#0B0F1A] font-bold text-sm">C</span>
      </div>
      <span class="font-semibold text-lg text-[#F1F5F9]">CCEC</span>
    </a>

    <!-- Desktop nav -->
    <div class="hidden md:flex items-center gap-8">
      {#each navLinks as link}
        <a href={link.href} class="text-[#94A3B8] hover:text-[#F59E0B] transition-colors text-sm font-medium">
          {link.label}
        </a>
      {/each}
    </div>

    <!-- CTA -->
    <div class="flex items-center gap-3">
      <a href="#pricing" class="hidden sm:block text-sm text-[#94A3B8] hover:text-[#F59E0B] transition-colors">
        Pricing
      </a>
      <a
        href="#"
        class="px-4 py-2 bg-[#F59E0B] text-[#0B0F1A] rounded-lg text-sm font-semibold hover:bg-[#FBBF24] transition-colors"
      >
        Get Started
      </a>
    </div>
  </div>
</nav>
