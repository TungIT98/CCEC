<script lang="ts">
  interface Tab {
    id: string;
    label: string;
    disabled?: boolean;
  }

  interface Props {
    tabs: Tab[];
    defaultTab?: string;
    class?: string;
    onchange?: (tabId: string) => void;
    children?: import('svelte').Snippet;
  }

  let {
    tabs,
    defaultTab = $bindable(tabs[0]?.id ?? ''),
    class: className = '',
    onchange,
    children,
  }: Props = $props();

  let activeTab = $state(defaultTab);

  function select(id: string) {
    activeTab = id;
    defaultTab = id;
    onchange?.(id);
  }
</script>

<div class="flex flex-col {className}">
  <!-- Tab list -->
  <div
    class="flex border-b border-[#1E293B]"
    role="tablist"
    aria-label="Tabs"
  >
    {#each tabs as tab}
      <button
        role="tab"
        aria-selected={activeTab === tab.id}
        aria-disabled={tab.disabled}
        disabled={tab.disabled}
        onclick={() => select(tab.id)}
        class="px-4 py-2.5 text-sm font-medium transition-colors relative
          {activeTab === tab.id
            ? 'text-[#F59E0B]'
            : 'text-slate-400 hover:text-slate-200'}
          {tab.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}"
      >
        {tab.label}
        {#if activeTab === tab.id}
          <span class="absolute bottom-0 left-0 right-0 h-0.5 bg-[#F59E0B] rounded-full"></span>
        {/if}
      </button>
    {/each}
  </div>

  <!-- Tab panels -->
  {#each tabs as tab}
    <div
      role="tabpanel"
      aria-labelledby={tab.id}
      hidden={activeTab !== tab.id}
      class="pt-4"
    >
      {#if activeTab === tab.id && children}
        {@render children()}
      {/if}
    </div>
  {/each}
</div>