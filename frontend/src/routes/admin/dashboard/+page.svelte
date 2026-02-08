<script lang="ts">
  import { onMount } from 'svelte';
  import { API_BASE_URL } from '$lib/api';

  let stats = {
    total_blogs: 0,
    published_blogs: 0,
    draft_blogs: 0,
    total_admins: 0
  };
  let isLoading = true;

  onMount(async () => {
    await fetchStats();
  });

  async function fetchStats() {
    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/stats`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (res.ok) {
        stats = await res.json();
      }
    } catch (e) {
      console.error('Failed to fetch stats:', e);
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="p-8">
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-slate-800 mb-2">Dashboard</h1>
    <p class="text-slate-600">Welcome back! Here's an overview of your system.</p>
  </div>

  {#if isLoading}
    <div class="flex items-center justify-center py-20">
      <svg class="animate-spin h-8 w-8 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  {:else}
    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Total Blogs -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-slate-600 font-medium">Total Blogs</p>
            <p class="text-3xl font-bold text-slate-800 mt-2">{stats.total_blogs}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-2xl">
            📝
          </div>
        </div>
      </div>

      <!-- Published Blogs -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-slate-600 font-medium">Published</p>
            <p class="text-3xl font-bold text-green-600 mt-2">{stats.published_blogs}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center text-2xl">
            ✅
          </div>
        </div>
      </div>

      <!-- Draft Blogs -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-slate-600 font-medium">Drafts</p>
            <p class="text-3xl font-bold text-yellow-600 mt-2">{stats.draft_blogs}</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center text-2xl">
            📄
          </div>
        </div>
      </div>

      <!-- Admins -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-slate-600 font-medium">Administrators</p>
            <p class="text-3xl font-bold text-slate-800 mt-2">{stats.total_admins}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl">
            👥
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 class="text-xl font-bold text-slate-800 mb-4">Quick Actions</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <a
          href="/admin/blogs"
          class="flex items-center gap-3 p-4 border-2 border-slate-200 rounded-lg hover:border-red-600 hover:bg-red-50 transition group"
        >
          <span class="text-2xl">📝</span>
          <div>
            <p class="font-semibold text-slate-800 group-hover:text-red-600">Manage Blogs</p>
            <p class="text-sm text-slate-600">Create and edit blog posts</p>
          </div>
        </a>

        <a
          href="/admin/settings"
          class="flex items-center gap-3 p-4 border-2 border-slate-200 rounded-lg hover:border-red-600 hover:bg-red-50 transition group"
        >
          <span class="text-2xl">⚙️</span>
          <div>
            <p class="font-semibold text-slate-800 group-hover:text-red-600">Settings</p>
            <p class="text-sm text-slate-600">Configure site settings</p>
          </div>
        </a>

        <a
          href="/admin/seo"
          class="flex items-center gap-3 p-4 border-2 border-slate-200 rounded-lg hover:border-red-600 hover:bg-red-50 transition group"
        >
          <span class="text-2xl">🔍</span>
          <div>
            <p class="font-semibold text-slate-800 group-hover:text-red-600">SEO Settings</p>
            <p class="text-sm text-slate-600">Optimize for search engines</p>
          </div>
        </a>
      </div>
    </div>
  {/if}
</div>
