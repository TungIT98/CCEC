<script lang="ts">
  import { onMount } from 'svelte';

  interface Props {
    open?: boolean;
    title?: string;
    description?: string;
    size?: 'sm' | 'md' | 'lg' | 'xl';
    onclose?: () => void;
    children?: import('svelte').Snippet;
    footer?: import('svelte').Snippet;
  }

  let {
    open = $bindable(false),
    title = '',
    description = '',
    size = 'md',
    onclose,
    children,
    footer,
  }: Props = $props();

  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
  };

  function close() {
    open = false;
    onclose?.();
  }

  function handleKey(e: KeyboardEvent) {
    if (e.key === 'Escape') close();
  }

  let dialog: HTMLDialogElement;

  $effect(() => {
    if (!dialog) return;
    if (open) {
      dialog.showModal();
    } else {
      dialog.close();
    }
  });

  onMount(() => {
    dialog.addEventListener('close', () => {
      open = false;
      onclose?.();
    });
    dialog.addEventListener('click', (e) => {
      if (e.target === dialog) close();
    });
  });
</script>

<dialog
  bind:this={dialog}
  onkeydown={handleKey}
  class="backdrop-brightness-50 backdrop-blur-sm border border-[#1E293B] p-0 rounded-2xl w-full
    bg-[#0B0F1A] text-slate-100 shadow-2xl {sizes[size]}"
>
  <div class="flex flex-col">
    <!-- Header -->
    <div class="flex items-start justify-between p-6 pb-4 border-b border-[#1E293B]">
      <div>
        {#if title}
          <h2 class="text-lg font-semibold text-white">{title}</h2>
        {/if}
        {#if description}
          <p class="mt-1 text-sm text-slate-400">{description}</p>
        {/if}
      </div>
      <button
        onclick={close}
        class="ml-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-[#1E293B] transition-colors"
        aria-label="Close"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Body -->
    <div class="p-6">
      {#if children}
        {@render children()}
      {/if}
    </div>

    <!-- Footer -->
    {#if footer}
      <div class="px-6 py-4 border-t border-[#1E293B] flex justify-end gap-3">
        {@render footer()}
      </div>
    {/if}
  </div>
</dialog>