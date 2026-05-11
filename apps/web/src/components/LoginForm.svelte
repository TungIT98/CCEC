<script lang="ts">
  import { login as apiLogin, storeUser } from '../lib/auth';

  let email = $state('');
  let password = $state('');
  let error = $state('');
  let loading = $state(false);
  let registered = $state(false);

  async function handleLogin(e: Event) {
    e.preventDefault();
    error = '';
    loading = true;
    try {
      const user = await apiLogin(email, password);
      // Store user in localStorage for page access check
      storeUser(user);
      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (err: any) {
      error = err.message || 'Đăng nhập thất bại';
    } finally {
      loading = false;
    }
  }

  async function handleRegister(e: Event) {
    e.preventDefault();
    error = '';
    loading = true;
    try {
      const res = await fetch(`${import.meta.env.PUBLIC_API_URL ?? 'http://localhost:8000'}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, full_name: email.split('@')[0] }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Đăng ký thất bại');
      }
      registered = true;
      error = 'Đăng ký thành công! Vui lòng đăng nhập.';
    } catch (err: any) {
      error = err.message || 'Đăng ký thất bại';
    } finally {
      loading = false;
    }
  }
</script>

<div class="w-full max-w-sm mx-auto">
  {#if error}
    <div class="mb-4 px-4 py-3 rounded-lg text-sm {registered ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'}">
      {error}
    </div>
  {/if}

  <form onsubmit={handleLogin} class="space-y-4">
    <div>
      <label for="email" class="block text-sm font-medium text-slate-700 mb-1">Email</label>
      <input
        id="email"
        type="email"
        bind:value={email}
        required
        placeholder="you@example.com"
        class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-100 outline-none transition"
      />
    </div>
    <div>
      <label for="password" class="block text-sm font-medium text-slate-700 mb-1">Mật khẩu</label>
      <input
        id="password"
        type="password"
        bind:value={password}
        required
        placeholder="••••••••"
        class="w-full px-4 py-2.5 rounded-lg border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-100 outline-none transition"
      />
    </div>
    <div class="flex gap-3 pt-2">
      <button
        type="submit"
        disabled={loading}
        class="flex-1 bg-teal-600 text-white py-2.5 rounded-lg font-medium hover:bg-teal-700 disabled:opacity-50 transition"
      >
        {loading ? 'Đang xử lý...' : 'Đăng nhập'}
      </button>
      <button
        type="button"
        onclick={handleRegister}
        disabled={loading}
        class="flex-1 border border-slate-200 text-slate-600 py-2.5 rounded-lg font-medium hover:bg-slate-50 disabled:opacity-50 transition"
      >
        Đăng ký
      </button>
    </div>
  </form>
  <p class="mt-4 text-xs text-slate-400 text-center">
    Chưa có tài khoản? Nhấn Đăng ký ở trên.
  </p>
</div>