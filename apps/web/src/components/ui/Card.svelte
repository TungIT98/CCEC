<script lang="ts">
  interface Props {
    class?: string;
    hover?: boolean;
  }
  let { class: className = '', hover = true }: Props = $props();
</script>

<div
  class="bg-[#1E293B] rounded-2xl border border-[#334155] p-6 transition-all duration-300
    {hover ? 'hover:border-[#00E5A0]/50 hover:shadow-[0_0_30px_rgba(0,229,160,0.1)]' : ''}
    {className}"
>
  <slot />
</div>