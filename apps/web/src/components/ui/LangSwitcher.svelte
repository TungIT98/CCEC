<script lang="ts">
  import { onMount } from 'svelte';

  type Locale = 'en' | 'vi';

  const STORAGE_KEY = 'ccec-locale';
  const LANGUAGES: { code: Locale; label: string; native: string }[] = [
    { code: 'en', label: 'English', native: 'EN' },
    { code: 'vi', label: 'Vietnamese', native: 'VI' },
  ];

  let locale = $state<Locale>('en');

  onMount(() => {
    const stored = localStorage.getItem(STORAGE_KEY) as Locale | null;
    locale = stored ?? 'en';
  });

  function switchLocale(code: Locale) {
    locale = code;
    localStorage.setItem(STORAGE_KEY, code);
    // Dispatch custom event so i18n store can react
    window.dispatchEvent(new CustomEvent('ccec-locale-change', { detail: { locale: code } }));
  }

  let open = $state(false);
  let current = $derived(LANGUAGES.find((l) => l.code === locale) ?? LANGUAGES[0]);

  function toggle() { open = !open; }
  function select(code: Locale) {
    switchLocale(code);
    open = false;
  }
</script>

<div class="relative">
  <button
    type="button"
    onclick={toggle}
    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium
      text-slate-300 hover:text-white hover:bg-[#1E293B] transition-colors border border-transparent
      hover:border-[#1E293B]"
    aria-haspopup="listbox"
    aria-expanded={open}
  >
    <span class="text-xs font-mono">{current.native}</span>
    <span class="hidden sm:inline">{current.label}</span>
    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d={open ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'} />
    </svg>
  </button>

  {#if open}
    <!-- Backdrop -->
    <button
      class="fixed inset-0 z-40"
      onclick={() => { open = false; }}
      aria-label="Close language selector"
    ></button>

    <!-- Dropdown -->
    <div
      class="absolute right-0 mt-1.5 z-50 w-36 py-1 rounded-xl border border-[#1E293B]
        bg-[#0F172A] shadow-xl"
      role="listbox"
      aria-label="Select language"
    >
      {#each LANGUAGES as lang}
        <button
          type="button"
          role="option"
          aria-selected={locale === lang.code}
          onclick={() => select(lang.code)}
          class="w-full flex items-center gap-2.5 px-3 py-2 text-sm transition-colors
            {locale === lang.code
              ? 'text-[#F59E0B] bg-[#F59E0B]/5'
              : 'text-slate-300 hover:text-white hover:bg-[#1E293B]'}"
        >
          <span class="text-xs font-mono w-4">{lang.native}</span>
          <span>{lang.native === 'EN' ? 'English' : 'Tiếng Việt'}</span>
          {#if locale === lang.code}
            <svg class="ml-auto w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          {/if}
        </button>
      {/each}
    </div>
  {/if}
</div>