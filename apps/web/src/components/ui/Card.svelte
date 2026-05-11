<script lang="ts">
  interface Props {
    class?: string;
    hover?: boolean;
  }
  let { class: className = '', hover = true }: Props = $props();
</script>

<div
  class="bg-[#1E293B] rounded-2xl border border-[#334155] p-6 transition-all duration-300
    {hover ? 'hover:border-[#F59E0B]/50 hover:shadow-[0_0_30px_rgba(245,229,11,0.1)]' : ''}
    {className}"
>
  <slot />
</div>