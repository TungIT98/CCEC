<script lang="ts">
  interface Props {
    type?: 'text' | 'email' | 'password' | 'number' | 'url' | 'search';
    value?: string;
    placeholder?: string;
    label?: string;
    error?: string;
    help?: string;
    disabled?: boolean;
    required?: boolean;
    id?: string;
    name?: string;
    class?: string;
    oninput?: (val: string) => void;
  }

  let {
    type = 'text',
    value = $bindable(''),
    placeholder = '',
    label = '',
    error = '',
    help = '',
    disabled = false,
    required = false,
    id = '',
    name = '',
    class: className = '',
    oninput,
  }: Props = $props();

  const inputId = id || `input-${Math.random().toString(36).slice(2)}`;
</script>

<div class="flex flex-col gap-1 {className}">
  {#if label}
    <label for={inputId} class="text-sm font-medium text-slate-700">
      {label}{#if required}<span class="text-red-500 ml-1">*</span>{/if}
    </label>
  {/if}

  <input
    {type}
    id={inputId}
    {name}
    {placeholder}
    {disabled}
    {required}
    bind:value
    oninput={(e) => oninput?.((e.target as HTMLInputElement).value)}
    class="
      ccec-input
      w-full px-3.5 py-2.5 rounded-xl border text-sm transition-all
      {error
        ? 'border-red-400 bg-red-50 focus:border-red-500 focus:ring-2 focus:ring-red-200'
        : 'border-slate-300 bg-white focus:border-[#F59E0B] focus:ring-2 focus:ring-[#F59E0B]/20'}
      {disabled ? 'opacity-60 cursor-not-allowed bg-slate-50' : ''}
      placeholder:text-slate-400 outline-none
    "
    aria-invalid={!!error}
    aria-describedby={error ? `${inputId}-error` : help ? `${inputId}-help` : undefined}
  />

  {#if error}
    <p id="{inputId}-error" class="text-xs text-red-600 flex items-center gap-1">
      <svg class="w-3.5 h-3.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      {error}
    </p>
  {:else if help}
    <p id="{inputId}-help" class="text-xs text-slate-400">{help}</p>
  {/if}
</div>