<script lang="ts">
  interface Props {
    /** JSON-serialisable data to export */
    data: unknown[];
    /** Optional filename without extension */
    filename?: string;
    /** CSV column headers (uses data[0] keys if omitted) */
    columns?: { key: string; label: string }[];
    /** Export label */
    label?: string;
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md';
    class?: string;
    disabled?: boolean;
    icon?: boolean; // show icon only
  }

  let {
    data,
    filename = 'export',
    columns,
    label = 'Export',
    variant = 'secondary',
    size = 'sm',
    class: className = '',
    disabled = false,
    icon = false,
  }: Props = $props();

  let exporting = $state(false);

  async function exportCSV() {
    if (disabled || exporting) return;
    exporting = true;
    try {
      // Build headers
      const headers = columns ?? Object.keys((data[0] ?? {}) as Record<string, unknown>).map((k) => ({ key: k, label: k }));

      const rows = data.map((row) =>
        headers
          .map((h) => {
            const v = (row as Record<string, unknown>)[h.key];
            const str = v == null ? '' : String(v);
            // Escape CSV special chars
            return str.includes(',') || str.includes('"') || str.includes('\n')
              ? `"${str.replace(/"/g, '""')}"`
              : str;
          })
          .join(',')
      );

      const csv = [headers.map((h) => h.label).join(','), ...rows].join('\n');
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${filename}-${new Date().toISOString().slice(0, 10)}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } finally {
      exporting = false;
    }
  }
</script>

<button
  type="button"
  onclick={exportCSV}
  disabled={disabled || exporting}
  class="inline-flex items-center gap-2 rounded-lg font-medium transition-all duration-150
    focus:outline-none focus:ring-[#F59E0B]/40
    {variant === 'primary' ? 'bg-[#F59E0B] text-[#0B0F1A] hover:bg-[#FBBF24]' : ''}
    {variant === 'secondary' ? 'border border-[#1E293B] text-slate-300 hover:border-[#F59E0B] hover:text-[#F59E0B]' : ''}
    {variant === 'ghost' ? 'text-slate-400 hover:text-white' : ''}
    {size === 'sm' ? 'px-3 py-1.5 text-xs' : 'px-4 py-2 text-sm'}
    {disabled || exporting ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
    {className}"
  title={icon ? label : undefined}
>
  {#if exporting}
    <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a10 10 0 00-10 10h2z" />
    </svg>
  {:else}
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  {/if}
  {#if !icon}<span>{exporting ? 'Exporting…' : label}</span>{/if}
</button>