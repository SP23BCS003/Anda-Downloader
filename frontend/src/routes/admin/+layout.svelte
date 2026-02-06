<script lang="ts">
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';

  let currentPage = 'dashboard';
  let username = '';
  let isMobileMenuOpen = false;
  let isCheckingAuth = true;
  let isAuthenticated = false;

  $: isLoginPage = $page.url.pathname === '/admin/login';

  onMount(() => {
    // Skip auth check on login page
    if (isLoginPage) {
      isCheckingAuth = false;
      return;
    }

    // Check auth
    const token = browser ? localStorage.getItem('admin_token') : null;
    if (!token) {
      goto('/admin/login');
      return;
    }
    username = localStorage.getItem('admin_username') || 'Admin';
    isAuthenticated = true;
    isCheckingAuth = false;
  });

  function logout() {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_username');
    goto('/admin/login');
  }

  const menuItems = [
    { name: 'Dashboard', icon: '📊', href: '/admin/dashboard' },
    { name: 'Blogs', icon: '📝', href: '/admin/blogs' },
    { name: 'Settings', icon: '⚙️', href: '/admin/settings' },
    { name: 'SEO', icon: '🔍', href: '/admin/seo' }
  ];
</script>

<!-- Login page gets rendered directly without sidebar -->
{#if isLoginPage}
  <slot />
{:else if isCheckingAuth}
  <!-- Loading state while checking auth -->
  <div class="min-h-screen bg-slate-900 flex items-center justify-center">
    <div class="text-center">
      <div class="w-12 h-12 bg-red-600 rounded-xl flex items-center justify-center text-white font-bold text-2xl mx-auto mb-4 animate-pulse">
        A
      </div>
      <p class="text-slate-400">Checking authentication...</p>
    </div>
  </div>
{:else if isAuthenticated}
  <!-- Authenticated admin layout -->
  <div class="min-h-screen bg-slate-50 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-900 text-white flex flex-col hidden md:flex">
      <!-- Logo -->
      <div class="p-6 border-b border-slate-800">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-red-600 rounded-lg flex items-center justify-center font-bold text-xl">
            A
          </div>
          <div>
            <h1 class="font-bold text-lg">Admin Panel</h1>
            <p class="text-xs text-slate-400">Downloader</p>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 p-4 space-y-2">
        {#each menuItems as item}
          <a
            href={item.href}
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-slate-800 transition"
          >
            <span class="text-xl">{item.icon}</span>
            <span>{item.name}</span>
          </a>
        {/each}
      </nav>

      <!-- User Info -->
      <div class="p-4 border-t border-slate-800">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center text-sm font-bold">
              {username.charAt(0).toUpperCase()}
            </div>
            <div class="text-sm">
              <p class="font-medium">{username}</p>
              <p class="text-xs text-slate-400">Administrator</p>
            </div>
          </div>
          <button
            on:click={logout}
            class="text-slate-400 hover:text-white transition"
            title="Logout"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <!-- Top Bar (Mobile) -->
      <header class="bg-white border-b border-slate-200 p-4 md:hidden flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center text-white font-bold">
            A
          </div>
          <span class="font-bold">Admin Panel</span>
        </div>
        <button
          on:click={() => isMobileMenuOpen = !isMobileMenuOpen}
          class="p-2 hover:bg-slate-100 rounded-lg"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </header>

      <!-- Mobile Menu -->
      {#if isMobileMenuOpen}
        <div class="md:hidden bg-white border-b border-slate-200 p-4 space-y-2">
          {#each menuItems as item}
            <a
              href={item.href}
              class="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-slate-100 transition"
              on:click={() => isMobileMenuOpen = false}
            >
              <span>{item.icon}</span>
              <span>{item.name}</span>
            </a>
          {/each}
          <button
            on:click={logout}
            class="flex items-center gap-3 px-4 py-2 w-full text-left text-red-600 hover:bg-red-50 rounded-lg transition"
          >
            <span>🚪</span>
            <span>Logout</span>
          </button>
        </div>
      {/if}

      <!-- Page Content -->
      <main class="flex-1 overflow-auto">
        <slot />
      </main>
    </div>
  </div>
{/if}
