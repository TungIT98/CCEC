<script lang="ts">
  interface Column<T> {
    key: keyof T | string;
    label: string;
    sortable?: boolean;
    render?: (value: unknown, row: T) => import('svelte').Snippet;
    width?: string;
    align?: 'left' | 'center' | 'right';
  }

  interface Props<T extends Record<string, unknown> = Record<string, unknown>> {
    columns: Column<T>[];
    data: T[];
    /** Row key extractor (default: first string key) */
    rowKey?: keyof T;
    emptyMessage?: string;
    loading?: boolean;
    class?: string;
    onRowClick?: (row: T) => void;
  }

  let {
    columns,
    data,
    rowKey,
    emptyMessage = 'No data available',
    loading = false,
    class: className = '',
    onRowClick,
  }: Props = $props();

  type T = typeof data[number];

  let sortKey = $state<string | null>(null);
  let sortDir = $state<'asc' | 'desc'>('asc');

  function handleSort(col: Column<T>) {
    if (!col.sortable) return;
    const k = String(col.key);
    if (sortKey === k) {
      sortDir = sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey = k;
      sortDir = 'asc';
    }
  }

  const sorted = $derived((() => {
    if (!sortKey) return data;
    return [...data].sort((a, b) => {
      const av = (a as Record<string, unknown>)[sortKey!];
      const bv = (b as Record<string, unknown>)[sortKey!];
      const cmp = String(av ?? '').localeCompare(String(bv ?? ''), undefined, { numeric: true });
      return sortDir === 'asc' ? cmp : -cmp;
    });
  })());

  function getRowKey(row: T, index: number): string {
    if (rowKey) return String((row as Record<string, unknown>)[String(rowKey)] ?? index);
    return String(index);
  }

  function getVal(row: T, key: string): unknown {
    return (row as Record<string, unknown>)[key];
  }

  const alignClass = { left: 'text-left', center: 'text-center', right: 'text-right' };
</script>

<div class="overflow-x-auto rounded-xl border border-[#1E293B] {className}">
  <table class="ccec-table">
    <thead>
      <tr>
        {#each columns as col}
          <th
            style={col.width ? `width: ${col.width}` : undefined}
            class="text-xs font-semibold text-slate-400 uppercase tracking-wider
              {col.sortable ? 'cursor-pointer select-none hover:text-slate-200' : ''}
              {alignClass[col.align ?? 'left']}"
            onclick={() => handleSort(col)}
          >
            <span class="inline-flex items-center gap-1.5">
              {col.label}
              {#if col.sortable && sortKey === String(col.key)}
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {#if sortDir === 'asc'}
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  {:else}
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  {/if}
                </svg>
              {/if}
            </span>
          </th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#if loading}
        <tr>
          <td colspan={columns.length} class="text-center py-10 text-slate-500 text-sm">
            Loading...
          </td>
        </tr>
      {:else if sorted.length === 0}
        <tr>
          <td colspan={columns.length} class="text-center py-10 text-slate-500 text-sm">
            {emptyMessage}
          </td>
        </tr>
      {:else}
        {#each sorted as row (getRowKey(row, sorted.indexOf(row)))}
          <tr
            class="border-b border-[#1E293B]/50 last:border-0
              {onRowClick ? 'cursor-pointer hover:bg-[#0F172A]/60' : ''}"
            onclick={() => onRowClick?.(row)}
          >
            {#each columns as col}
              {@const val = getVal(row, String(col.key))}
              <td class="text-sm text-slate-200 {alignClass[col.align ?? 'left']}">
                {#if col.render}
                  {@render col.render(val, row)}
                {:else}
                  {val ?? '—'}
                {/if}
              </td>
            {/each}
          </tr>
        {/each}
      {/if}
    </tbody>
  </table>
</div>