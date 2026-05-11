<script lang="ts">
  const navLinks = [
    { label: 'Features', href: '#features' },
    { label: 'Roadmap', href: '#roadmap' },
    { label: 'Team', href: '#team' },
    { label: 'Contact', href: '#contact' },
  ];
</script>

<nav class="fixed top-0 w-full z-50 bg-[#0B0F1A]/90 backdrop-blur-md border-b border-[#334155]">
  <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
    <!-- Logo -->
    <a href="/" class="flex items-center gap-2">
      <div class="w-8 h-8 rounded-lg bg-[#00E5A0] flex items-center justify-center">
        <span class="text-[#0B0F1A] font-bold text-sm">C</span>
      </div>
      <span class="font-semibold text-lg text-[#F1F5F9]">CCEC</span>
    </a>

    <!-- Desktop nav -->
    <div class="hidden md:flex items-center gap-8">
      {#each navLinks as link}
        <a href={link.href} class="text-[#94A3B8] hover:text-[#00E5A0] transition-colors text-sm font-medium">
          {link.label}
        </a>
      {/each}
    </div>

    <!-- CTA -->
    <div class="flex items-center gap-3">
      <a href="#pricing" class="hidden sm:block text-sm text-[#94A3B8] hover:text-[#00E5A0] transition-colors">
        Pricing
      </a>
      <a
        href="#"
        class="px-4 py-2 bg-[#00E5A0] text-[#0B0F1A] rounded-lg text-sm font-semibold hover:bg-[#00C485] transition-colors"
      >
        Get Started
      </a>
    </div>
  </div>
</nav>
