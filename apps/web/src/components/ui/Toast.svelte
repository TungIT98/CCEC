<script lang="ts">
  // Centralised toast store — shared across the app
  import { writable } from 'svelte/store';

  export type ToastKind = 'success' | 'error' | 'warning' | 'info';

  export interface ToastItem {
    id: string;
    kind: ToastKind;
    title: string;
    message?: string;
    duration?: number; // ms, default 4000
  }

  export const toasts = writable<ToastItem[]>([]);

  export function showToast(opts: Omit<ToastItem, 'id'>) {
    const id = Math.random().toString(36).slice(2);
    toasts.update((t) => [...t, { ...opts, id }]);
    setTimeout(() => dismissToast(id), opts.duration ?? 4000);
  }

  export function dismissToast(id: string) {
    toasts.update((t) => t.filter((x) => x.id !== id));
  }

  const icons: Record<ToastKind, string> = {
    success: 'M5 13l4 4L19 7',
    error: 'M6 18L18 6M6 6l12 12',
    warning: 'M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z',
    info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
  };

  const colors: Record<ToastKind, { border: string; icon: string; title: string }> = {
    success: { border: '#F59E0B', icon: '#F59E0B', title: 'text-[#F59E0B]' },
    error:   { border: '#EF4444', icon: '#EF4444', title: 'text-[#EF4444]' },
    warning: { border: '#F59E0B', icon: '#F59E0B', title: 'text-[#F59E0B]' },
    info:    { border: '#6366F1', icon: '#6366F1', title: 'text-[#6366F1]' },
  };
</script>

<script lang="ts" module>
  // re-export for convenience
  export { showToast, dismissToast } from './Toast.svelte';
</script>

<div
  class="fixed bottom-5 right-5 z-[100] flex flex-col gap-3 pointer-events-none"
  aria-live="polite"
  aria-atomic="false"
>
  {#each $toasts as toast (toast.id)}
    {@const c = colors[toast.kind]}
    <div
      class="pointer-events-auto flex items-start gap-3 max-w-sm w-full p-4 rounded-xl border shadow-xl
        bg-[#0F172A] text-slate-100"
      style="border-color: {c.border};"
      role="alert"
    >
      <!-- Icon -->
      <span class="flex-shrink-0 mt-0.5">
        <svg class="w-5 h-5" style="color: {c.icon}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={icons[toast.kind]} />
        </svg>
      </span>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <p class="text-sm font-semibold {c.title}">{toast.title}</p>
        {#if toast.message}
          <p class="mt-0.5 text-xs text-slate-400">{toast.message}</p>
        {/if}
      </div>

      <!-- Dismiss -->
      <button
        onclick={() => dismissToast(toast.id)}
        class="flex-shrink-0 text-slate-500 hover:text-slate-300 transition-colors"
        aria-label="Dismiss"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  {/each}
</div>