<script lang="ts">
  interface Props {
    src?: string;
    alt?: string;
    name?: string; // fallback initials
    size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
    class?: string;
  }

  let { src, alt = '', name = '', size = 'md', class: className = '' }: Props = $props();

  const sizes = {
    xs: 'w-6 h-6 text-xs',
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base',
    xl: 'w-16 h-16 text-lg',
  };

  const scale = {
    xs: 'w-6 h-6',
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  };

  function initials(n: string) {
    return n
      .split(' ')
      .slice(0, 2)
      .map((w) => w[0] ?? '')
      .join('')
      .toUpperCase();
  }

  let imgError = $state(false);
</script>

<span
  class="inline-flex items-center justify-center rounded-full bg-[#1E40AF] text-white font-semibold
    overflow-hidden flex-shrink-0 {sizes[size]} {className}"
  title={alt || name}
>
  {#if src && !imgError}
    <img
      {src}
      {alt}
      class="w-full h-full object-cover"
      onerror={() => { imgError = true; }}
    />
  {:else}
    <span>{initials(alt || name)}</span>
  {/if}
</span>