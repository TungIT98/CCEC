<script lang="ts">
  import { onMount } from 'svelte';

  const API_BASE = import.meta.env.PUBLIC_API_URL ?? 'http://localhost:8000';

  let messages = $state([
    {
      role: 'assistant',
      content: 'Chào bạn! Tôi là AI trợ lý khí hậu của CCEC. Tôi có thể giúp bạn phân tích dữ liệu phát thải, dự báo xu hướng hoặc tìm hiểu về chiến lược carbon. Bạn cần hỗ trợ gì?',
    },
  ]);
  let input = $state('');
  let loading = $state(false);
  let chatEl = $state<HTMLDivElement | null>(null);

  $effect(() => {
    if (chatEl) chatEl.scrollTop = chatEl.scrollHeight;
  });

  function authHeaders(): Record<string, string> {
    try {
      const raw = localStorage.getItem('ccec_tokens');
      if (raw) {
        const tokens = JSON.parse(raw);
        return { Authorization: `Bearer ${tokens.access_token}` };
      }
    } catch {}
    return {};
  }

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    messages = [...messages, { role: 'user', content: text }];
    input = '';
    loading = true;
    try {
      const res = await fetch(`${API_BASE}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...authHeaders(),
        },
        body: JSON.stringify({ message: text }),
      });
      if (!res.ok) {
        const errText = await res.text().catch(() => '');
        const errMsg = errText ? `Lỗi (${res.status}): ${errText.slice(0, 100)}` : `Lỗi kết nối (${res.status}). Vui lòng đăng nhập.`;
        messages = [...messages, { role: 'assistant', content: errMsg }];
        return;
      }
      const data = await res.json();
      // API returns { message, conversation_id, sources[] }
      const reply = data.message ?? data.reply ?? 'Xin lỗi, tôi chưa hiểu. Vui lòng thử lại.';
      messages = [...messages, { role: 'assistant', content: reply }];
    } catch {
      messages = [...messages, { role: 'assistant', content: 'Đã xảy ra lỗi kết nối. Vui lòng thử lại.' }];
    } finally {
      loading = false;
    }
  }

  function handleKey(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  }
</script>

<div class="fixed bottom-6 right-6 z-50 w-80 max-w-[calc(100vw-3rem)]">
  <!-- Toggle button -->
  <button
    class="w-14 h-14 bg-[#00E5A0] rounded-full shadow-[0_0_30px_rgba(0,229,160,0.4)] flex items-center justify-center hover:scale-110 transition-transform ml-auto block"
    onclick={() => { const panel = document.getElementById('ccec-chat-panel'); if (panel) panel.classList.toggle('hidden'); }}
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-[#0B0F1A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
    </svg>
  </button>

  <!-- Chat panel -->
  <div id="ccec-chat-panel" class="hidden mt-3 bg-[#111827] rounded-2xl border border-[#334155] shadow-2xl overflow-hidden">
    <div class="bg-[#1E293B] px-4 py-3 flex items-center justify-between border-b border-[#334155]">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 bg-[#00E5A0] rounded-full animate-pulse"></div>
        <span class="text-sm font-semibold text-[#F1F5F9]">CCEC AI Assistant</span>
      </div>
      <button
        onclick={() => { const panel = document.getElementById('ccec-chat-panel'); if (panel) panel.classList.add('hidden'); }}
        class="text-[#94A3B8] hover:text-white"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Messages -->
    <div bind:this={chatEl} class="h-72 overflow-y-auto p-4 space-y-4">
      {#each messages as msg}
        <div class="flex {msg.role === 'user' ? 'justify-end' : 'justify-start'}">
          <div class="max-w-[85%] px-4 py-2.5 rounded-xl text-sm leading-relaxed
            {msg.role === 'user'
              ? 'bg-[#00E5A0] text-[#0B0F1A] rounded-br-md'
              : 'bg-[#1E293B] text-[#F1F5F9] border border-[#334155] rounded-bl-md'}">
            {msg.content}
          </div>
        </div>
      {/each}
      {#if loading}
        <div class="flex justify-start">
          <div class="bg-[#1E293B] border border-[#334155] rounded-xl rounded-bl-md px-4 py-3">
            <div class="flex gap-1.5">
              <span class="w-2 h-2 bg-[#00E5A0] rounded-full animate-bounce" style="animation-delay:0ms"></span>
              <span class="w-2 h-2 bg-[#00E5A0] rounded-full animate-bounce" style="animation-delay:150ms"></span>
              <span class="w-2 h-2 bg-[#00E5A0] rounded-full animate-bounce" style="animation-delay:300ms"></span>
            </div>
          </div>
        </div>
      {/if}
    </div>

    <!-- Input -->
    <div class="p-3 border-t border-[#334155] flex gap-2">
      <textarea
        bind:value={input}
        onkeydown={handleKey}
        placeholder="Ask about emissions data..."
        rows="1"
        class="flex-1 px-3 py-2 bg-[#1E293B] border border-[#334155] rounded-lg text-sm text-[#F1F5F9] placeholder-[#94A3B8] resize-none focus:outline-none focus:border-[#00E5A0]"
      ></textarea>
      <button
        onclick={send}
        disabled={loading || !input.trim()}
        class="px-3 py-2 bg-[#00E5A0] text-[#0B0F1A] rounded-lg text-sm font-semibold hover:bg-[#00C485] disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex-shrink-0"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
        </svg>
      </button>
    </div>
  </div>
</div>