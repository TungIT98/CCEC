<section id="team" class="py-24 px-6 bg-[#111827]">
  <div class="max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <p class="text-[#0EA5E9] text-sm font-semibold uppercase tracking-widest mb-3">Team</p>
      <h2 class="text-4xl md:text-5xl font-bold text-[#F1F5F9] mb-4">Built by Researchers & Engineers</h2>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
      {#each [
        { name: 'Nguyen Van A', role: 'CEO & Co-founder', bio: 'Former climate researcher at MIT, 10+ years in energy analytics.', initials: 'NVA' },
        { name: 'Tran Thi B', role: 'CTO & Co-founder', bio: 'Ex-Google infrastructure engineer, crypto enthusiast since 2015.', initials: 'TTB' },
        { name: 'Le Van C', role: 'Lead AI Engineer', bio: 'PhD in ML from Stanford, specializing in time-series forecasting.', initials: 'LVC' },
        { name: 'Pham Thi D', role: 'Product Designer', bio: 'Former Figma designer, passionate about data visualization.', initials: 'PTD' },
      ] as member}
        <div class="bg-[#1E293B] rounded-2xl p-6 border border-[#334155] text-center hover:border-[#F59E0B]/50 transition-colors">
          <div class="w-16 h-16 rounded-full bg-[#334155] mx-auto mb-4 flex items-center justify-center text-xl font-bold text-[#F59E0B]">
            {member.initials}
          </div>
          <h3 class="text-[#F1F5F9] font-semibold mb-1">{member.name}</h3>
          <p class="text-[#F59E0B] text-xs font-medium mb-2">{member.role}</p>
          <p class="text-[#94A3B8] text-xs">{member.bio}</p>
        </div>
      {/each}
    </div>
  </div>
</section>
