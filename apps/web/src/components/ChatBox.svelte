<script lang="ts">
  import { sendChat } from '../lib/api';
  import { getStoredUser } from '../lib/auth';

  interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp?: string;
  }

  let messages = $state<Message[]>([
    {
      role: 'system',
      content: 'Chào mừng đến với CCEC AI Assistant! Tôi có thể giúp bạn phân tích chiến lược khí hậu Việt Nam, trả lời câu hỏi về dữ liệu khí hậu, và hỗ trợ nghiên cứu CNKI.',
    },
  ]);
  let input = $state('');
  let loading = $state(false);
  let error = $state('');
  let conversationId = $state('');

  const user = getStoredUser();

  async function handleSend(e?: Event) {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    input = '';
    loading = true;
    error = '';

    messages = [...messages, { role: 'user', content: userMsg }];

    try {
      const res = await sendChat(userMsg, conversationId || undefined);
      conversationId = res.conversation_id;
      messages = [
        ...messages,
        { role: 'assistant', content: res.message, timestamp: new Date().toISOString() },
      ];
    } catch (e: any) {
      error = e.message || 'Lỗi kết nối AI. Vui lòng thử lại.';
    } finally {
      loading = false;
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }
</script>

<div class="flex flex-col h-screen bg-slate-50">
  <!-- Header -->
  <header class="sticky top-0 z-10 bg-white/90 backdrop-blur-xl border-b border-slate-200 px-6 py-4">
    <div class="flex items-center justify-between max-w-3xl mx-auto">
      <div class="flex items-center gap-3">
        <a href="/" class="flex items-center gap-2.5 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-500 to-teal-700 flex items-center justify-center shadow-sm">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
          </div>
          <span class="font-bold text-slate-900 text-sm">CCEC</span>
        </a>
        <span class="text-slate-300">/</span>
        <span class="font-semibold text-slate-700 text-sm">AI Chat</span>
      </div>
      {#if user}
        <div class="flex items-center gap-2 text-xs text-slate-500">
          <div class="w-6 h-6 rounded-full bg-teal-100 flex items-center justify-center">
            <svg class="w-3 h-3 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
          <span>{user.email}</span>
        </div>
      {/if}
    </div>
  </header>

  <!-- Messages -->
  <main class="flex-1 overflow-y-auto px-4 py-6 space-y-4 max-w-3xl mx-auto w-full">
    {#each messages as msg, i}
      {#if msg.role === 'user'}
        <div class="flex justify-end">
          <div class="bg-teal-600 text-white rounded-2xl rounded-br-md px-4 py-3 max-w-xs text-sm shadow-sm">
            {msg.content}
          </div>
        </div>
      {:else if msg.role === 'assistant'}
        <div class="flex justify-start">
          <div class="bg-white border border-slate-200 rounded-2xl rounded-bl-md px-4 py-3 max-w-lg text-sm shadow-sm">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-5 h-5 rounded-full bg-teal-100 flex items-center justify-center">
                <svg class="w-3 h-3 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a5 5 0 0 0-5 5v6a5 5 0 0 0 10 0V7a5 5 0 0 0-5-5z"/><path d="M12 2v5m0 0l-3-3m3 3l3-3"/></svg>
              </div>
              <span class="text-xs text-slate-400">CCEC AI Assistant</span>
            </div>
            <div class="whitespace-pre-wrap">{msg.content}</div>
          </div>
        </div>
      {:else}
        <div class="flex justify-start">
          <div class="bg-teal-50 border border-teal-100 rounded-xl px-4 py-3 text-sm text-teal-700 max-w-lg text-center mx-auto">
            {msg.content}
          </div>
        </div>
      {/if}
    {/each}

    {#if loading}
      <div class="flex justify-start">
        <div class="bg-white border border-slate-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
          <div class="flex items-center gap-2 text-sm text-slate-400">
            <div class="w-4 h-4 border-2 border-teal-600 border-t-transparent rounded-full animate-spin"></div>
            <span>AI đang trả lời...</span>
          </div>
        </div>
      </div>
    {/if}

    {#if error}
      <div class="bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 text-sm flex items-center gap-2">
        <svg class="w-4 h-4 text-red-500 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
        {error}
      </div>
    {/if}
  </main>

  <!-- Input -->
  <div class="border-t border-slate-200 bg-white px-4 py-4">
    <form onsubmit={handleSend} class="max-w-3xl mx-auto flex gap-3">
      <textarea
        bind:value={input}
        onkeydown={handleKeydown}
        placeholder="Hỏi về chiến lược khí hậu, dữ liệu Vietnam, phân tích CNKI..."
        rows="2"
        class="flex-1 resize-none px-4 py-3 rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-100 outline-none transition text-sm"
      ></textarea>
      <button
        type="submit"
        disabled={loading || !input.trim()}
        class="self-end bg-teal-600 text-white px-5 py-3 rounded-xl font-medium hover:bg-teal-700 disabled:opacity-40 transition shadow-sm"
      >
        Gửi
      </button>
    </form>
    <p class="text-xs text-slate-400 text-center mt-2">Nhấn Enter để gửi · Shift+Enter cho xuống dòng</p>
  </div>
</div>