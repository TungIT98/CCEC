<script lang="ts">
  // Auth-gated wrapper — redirects to / if not logged in
  import { isAuthenticated } from '../lib/auth';

  interface Props {
    children?: any;
  }

  const { children }: Props = $props();

  if (typeof window !== 'undefined' && !isAuthenticated()) {
    window.location.href = '/';
  }
</script>

{#if typeof window === 'undefined' || isAuthenticated()}
  {@render children?.()}
{/if}