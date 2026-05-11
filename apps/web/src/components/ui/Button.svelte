<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    href?: string;
    class?: string;
  }

  let { variant = 'primary', size = 'md', href, class: className = '', ...rest }: Props = $props();
</script>

{#if href}
  <a
    {href}
    class="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200
      {variant === 'primary' ? 'bg-[#00E5A0] text-[#0B0F1A] hover:bg-[#00C485] shadow-[0_0_20px_rgba(0,229,160,0.3)] hover:shadow-[0_0_30px_rgba(0,229,160,0.5)]' : ''}
      {variant === 'secondary' ? 'border border-[#334155] bg-transparent text-slate-100 hover:border-[#00E5A0] hover:text-[#00E5A0]' : ''}
      {variant === 'ghost' ? 'text-slate-400 hover:text-white' : ''}
      {size === 'sm' ? 'px-4 py-2 text-sm' : ''}
      {size === 'md' ? 'px-6 py-3 text-base' : ''}
      {size === 'lg' ? 'px-8 py-4 text-lg' : ''}
      {className}"
    {...rest}
  >
    <slot />
  </a>
{:else}
  <button
    class="inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200
      {variant === 'primary' ? 'bg-[#00E5A0] text-[#0B0F1A] hover:bg-[#00C485] shadow-[0_0_20px_rgba(0,229,160,0.3)] hover:shadow-[0_0_30px_rgba(0,229,160,0.5)]' : ''}
      {variant === 'secondary' ? 'border border-[#334155] bg-transparent text-slate-100 hover:border-[#00E5A0] hover:text-[#00E5A0]' : ''}
      {variant === 'ghost' ? 'text-slate-400 hover:text-white' : ''}
      {size === 'sm' ? 'px-4 py-2 text-sm' : ''}
      {size === 'md' ? 'px-6 py-3 text-base' : ''}
      {size === 'lg' ? 'px-8 py-4 text-lg' : ''}
      {className}"
    {...rest}
  >
    <slot />
  </button>
{/if}