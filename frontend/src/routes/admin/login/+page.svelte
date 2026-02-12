<script lang="ts">
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';
  import { API_BASE_URL } from '$lib/api';

  let username = '';
  let password = '';
  let error = '';
  let isLoading = false;

  onMount(() => {
    // Check if already logged in
    const token = browser ? localStorage.getItem('admin_token') : null;
    if (token) {
      goto('/admin/dashboard');
    }
  });

  async function handleLogin() {
    username = username.trim();
    
    if (!username || !password) {
      error = 'Please enter both username and password';
      return;
    }

    isLoading = true;
    error = '';

    try {
      const res = await fetch(`${API_BASE_URL}/admin/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Login failed');
      }

      const data = await res.json();
      localStorage.setItem('admin_token', data.access_token);
      localStorage.setItem('admin_username', data.username);
      
      goto('/admin/dashboard');
    } catch (e: any) {
      error = e.message || 'Failed to login';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
  <div class="w-full max-w-md">
    <!-- Logo & Title -->
    <div class="text-center mb-8">
      <div class="w-16 h-16 bg-red-600 rounded-2xl flex items-center justify-center text-white font-bold text-2xl mx-auto mb-4 shadow-lg shadow-red-600/50">
        A
      </div>
      <h1 class="text-3xl font-bold text-white mb-2">Admin Panel</h1>
      <p class="text-slate-400">Sign in to manage your downloader</p>
    </div>

    <!-- Login Card -->
    <div class="bg-white rounded-2xl shadow-2xl p-8">
      <form on:submit|preventDefault={handleLogin}>
        <div class="space-y-6">
          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium text-slate-700 mb-2">
              Username
            </label>
            <input
              id="username"
              type="text"
              bind:value={username}
              class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none transition"
              placeholder="Enter your username"
              disabled={isLoading}
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-slate-700 mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              bind:value={password}
              class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none transition"
              placeholder="Enter your password"
              disabled={isLoading}
            />
          </div>

          <!-- Error Message -->
          {#if error}
            <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
              ⚠️ {error}
            </div>
          {/if}

          <!-- Submit Button -->
          <button
            type="submit"
            disabled={isLoading}
            class="w-full bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-6 rounded-lg transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {#if isLoading}
              <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            {:else}
              Sign In
            {/if}
          </button>
        </div>
      </form>

      <!-- Help Text -->

    </div>

    <!-- Back to Site -->
    <div class="mt-6 text-center">
      <a href="/" class="text-slate-400 hover:text-white transition text-sm">
        ← Back to downloader
      </a>
    </div>
  </div>
</div>

<style>
  :global(body) {
    overflow-x: hidden;
  }
</style>
