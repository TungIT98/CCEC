<script lang="ts">
  import { onMount } from 'svelte';

  type Theme = 'dark' | 'light' | 'system';

  const STORAGE_KEY = 'ccec-theme';

  let theme = $state<Theme>('dark');

  onMount(() => {
    const stored = localStorage.getItem(STORAGE_KEY) as Theme | null;
    theme = stored ?? 'dark';
    applyTheme(theme);
  });

  function applyTheme(t: Theme) {
    const root = document.documentElement;
    if (t === 'dark' || (t === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }

  function cycle() {
    const next: Record<Theme, Theme> = { dark: 'light', light: 'system', system: 'dark' };
    theme = next[theme];
    localStorage.setItem(STORAGE_KEY, theme);
    applyTheme(theme);
  }

  const icons: Record<Theme, string> = {
    dark: 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z',
    light: 'M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z',
    system: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
  };
</script>

<button
  type="button"
  onclick={cycle}
  title="Toggle theme: {theme}"
  class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-[#1E293B] transition-colors"
  aria-label="Toggle theme"
>
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d={icons[theme]} />
  </svg>
</button>