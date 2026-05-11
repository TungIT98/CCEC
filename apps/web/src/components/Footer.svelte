<footer id="contact" class="py-20 px-6 bg-[#0B0F1A] border-t border-[#334155]">
  <div class="max-w-7xl mx-auto">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
      <div>
        <div class="flex items-center gap-2 mb-4">
          <div class="w-8 h-8 rounded-lg bg-[#00E5A0] flex items-center justify-center">
            <span class="text-[#0B0F1A] font-bold text-sm">C</span>
          </div>
          <span class="font-semibold text-lg text-[#F1F5F9]">CCEC</span>
        </div>
        <p class="text-[#94A3B8] text-sm">AI-powered climate intelligence for crypto mining operations.</p>
      </div>

      <div>
        <h4 class="text-[#F1F5F9] font-semibold text-sm mb-4">Product</h4>
        <ul class="space-y-2">
          {#each ['Features', 'Pricing', 'Roadmap', 'Documentation'] as link}
            <li><a href="#" class="text-[#94A3B8] text-sm hover:text-[#00E5A0] transition-colors">{link}</a></li>
          {/each}
        </ul>
      </div>

      <div>
        <h4 class="text-[#F1F5F9] font-semibold text-sm mb-4">Company</h4>
        <ul class="space-y-2">
          {#each ['About', 'Team', 'Blog', 'Careers'] as link}
            <li><a href="#" class="text-[#94A3B8] text-sm hover:text-[#00E5A0] transition-colors">{link}</a></li>
          {/each}
        </ul>
      </div>

      <div>
        <h4 class="text-[#F1F5F9] font-semibold text-sm mb-4">Stay Updated</h4>
        <p class="text-[#94A3B8] text-sm mb-3">Subscribe to our newsletter.</p>
        <form class="flex gap-2" onsubmit={(e) => e.preventDefault()}>
          <input
            type="email"
            placeholder="you@example.com"
            class="flex-1 px-3 py-2 bg-[#1E293B] border border-[#334155] rounded-lg text-[#F1F5F9] text-sm placeholder-[#94A3B8] focus:outline-none focus:border-[#00E5A0]"
          />
          <button type="submit" class="px-4 py-2 bg-[#00E5A0] text-[#0B0F1A] rounded-lg text-sm font-semibold hover:bg-[#00C485] transition-colors">
            →
          </button>
        </form>
      </div>
    </div>

    <div class="pt-8 border-t border-[#334155] flex flex-col sm:flex-row items-center justify-between gap-4">
      <p class="text-[#94A3B8] text-xs">© 2026 CCEC Climate Platform. All rights reserved.</p>
      <div class="flex gap-4">
        {#each ['Twitter', 'GitHub', 'Discord', 'LinkedIn'] as social}
          <a href="#" class="text-[#94A3B8] hover:text-[#00E5A0] transition-colors text-xs">{social}</a>
        {/each}
      </div>
    </div>
  </div>
</footer>
