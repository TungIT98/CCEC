<script lang="ts">
  interface Props {
    checked?: boolean;
    label?: string;
    description?: string;
    disabled?: boolean;
    size?: 'sm' | 'md';
    onchange?: (checked: boolean) => void;
  }

  let {
    checked = false,
    label = '',
    description = '',
    disabled = false,
    size = 'md',
    onchange,
  }: Props = $props();

  function toggle() {
    if (disabled) return;
    const next = !checked;
    checked = next;
    onchange?.(next);
  }
</script>

<label class="flex items-center gap-3 cursor-pointer select-none {disabled ? 'opacity-50 cursor-not-allowed' : ''}">
  <button
    type="button"
    role="switch"
    aria-checked={checked}
    {disabled}
    onclick={toggle}
    class="
      relative rounded-full transition-all duration-200 flex-shrink-0
      {size === 'sm' ? 'w-9 h-5' : 'w-11 h-6'}
      {checked
        ? 'bg-[#F59E0B]'
        : 'bg-slate-300'}
      focus:outline-none focus:ring-2 focus:ring-[#F59E0B] focus:ring-offset-2
    "
  >
    <span
      class="
        absolute top-0.5 bg-white rounded-full shadow-sm transition-transform duration-200
        {size === 'sm' ? 'w-4 h-4' : 'w-5 h-5'}
        {checked ? (size === 'sm' ? 'translate-x-4' : 'translate-x-5') : 'translate-x-0.5'}
        top-0.5
      "
    ></span>
  </button>

  <span class="flex flex-col">
    {#if label}
      <span class="text-sm font-medium text-slate-700">{label}</span>
    {/if}
    {#if description}
      <span class="text-xs text-slate-500">{description}</span>
    {/if}
  </span>
</label>