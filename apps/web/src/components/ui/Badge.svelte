<script lang="ts">
  interface Props {
    color?: 'green' | 'blue' | 'purple' | 'yellow' | 'red';
    class?: string;
  }
  let { color = 'green', class: className = '' }: Props = $props();

  const colors = {
    green: 'bg-[#F59E0B]/10 text-[#F59E0B] border-[#F59E0B]/30',
    blue: 'bg-[#0EA5E9]/10 text-[#0EA5E9] border-[#0EA5E9]/30',
    purple: 'bg-[#A855F7]/10 text-[#A855F7] border-[#A855F7]/30',
    yellow: 'bg-[#F59E0B]/10 text-[#F59E0B] border-[#F59E0B]/30',
    red: 'bg-[#EF4444]/10 text-[#EF4444] border-[#EF4444]/30',
  };
</script>

<span
  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border
    {colors[color]}
    {className}"
>
  <slot />
</span>