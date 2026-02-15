<script lang="ts">
  import { onMount } from 'svelte';
  import { API_BASE_URL } from '$lib/api';

  let pages = [
    'home',
    'youtube-downloader',
    'youtube-to-mp3',
    'tiktok-downloader',
    'instagram-downloader',
    'facebook-downloader',
    'twitter-downloader',
    'pinterest-downloader',
    'soundcloud-downloader',
    'vimeo-downloader',
    'dailymotion-downloader',
    'twitch-downloader',
    'threads-downloader',
    'capcut-downloader',
    'contact',
    'privacy',
    'terms'
  ];
  let currentPage = 'home';
  let seoData: Record<string, any> = {};
  let isLoading = true;
  let isSaving = false;
  let saveMessage = '';

  let title = '';
  let description = '';
  let keywords = '';
  let ogImage = '';

onMount(async () => {
    await fetchSEO();
  });

  async function fetchSEO() {
    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/seo`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        seoData = await res.json();
        loadPageData(currentPage);
      }
    } catch (e) {
      console.error('Failed to fetch SEO:', e);
    } finally {
      isLoading = false;
    }
  }

  function loadPageData(page: string) {
    currentPage = page;
    const data = seoData[page] || {};
    title = data.title || '';
    description = data.description || '';
    keywords = data.keywords || '';
    ogImage = data.og_image || '';
  }

  async function saveSEO() {
    isSaving = true;
    saveMessage = '';

    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/seo/${currentPage}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          page: currentPage,
          title,
          description,
          keywords,
          og_image: ogImage
        })
      });

      if (res.ok) {
        saveMessage = 'SEO settings saved successfully! ✓';
        setTimeout(() => saveMessage = '', 3000);
        await fetchSEO();
      } else {
        throw new Error('Failed to save SEO settings');
      }
    } catch (e: any) {
      saveMessage = `Error: ${e.message}`;
    } finally {
      isSaving = false;
    }
  }
</script>

<div class="p-8">
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-slate-800 mb-2">SEO Settings</h1>
    <p class="text-slate-600">Optimize your pages for search engines</p>
  </div>

  {#if isLoading}
    <div class="flex items-center justify-center py-20">
      <svg class="animate-spin h-8 w-8 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  {:else}
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Page Selector -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 h-fit">
        <h3 class="font-semibold text-slate-800 mb-3">Pages</h3>
        <div class="space-y-1 max-h-[600px] overflow-y-auto">
          <!-- Main Pages -->
          <p class="text-xs font-medium text-slate-500 uppercase tracking-wide px-2 py-1">Main</p>
          {#each ['home', 'contact', 'privacy', 'terms'] as page}
            <button
              on:click={() => loadPageData(page)}
              class="w-full text-left px-3 py-2 rounded-lg transition text-sm {currentPage === page ? 'bg-red-600 text-white' : 'bg-slate-50 text-slate-700 hover:bg-slate-100'}"
            >
              {page === 'home' ? '🏠 Home' : 
               page === 'contact' ? '📧 Contact' :
               page === 'privacy' ? '🔒 Privacy Policy' :
               '📄 Terms of Service'}
            </button>
          {/each}

          <!-- Video Downloaders -->
          <p class="text-xs font-medium text-slate-500 uppercase tracking-wide px-2 py-1 mt-3">Video Downloaders</p>
          {#each ['youtube-downloader', 'youtube-to-mp3', 'tiktok-downloader', 'instagram-downloader', 'facebook-downloader', 'twitter-downloader', 'pinterest-downloader', 'vimeo-downloader', 'dailymotion-downloader', 'twitch-downloader', 'threads-downloader', 'capcut-downloader'] as page}
            <button
              on:click={() => loadPageData(page)}
              class="w-full text-left px-3 py-2 rounded-lg transition text-sm {currentPage === page ? 'bg-red-600 text-white' : 'bg-slate-50 text-slate-700 hover:bg-slate-100'}"
            >
              {page === 'youtube-downloader' ? '▶️ YouTube' :
               page === 'youtube-to-mp3' ? '🎵 YouTube to MP3' :
               page === 'tiktok-downloader' ? '🎬 TikTok' :
               page === 'instagram-downloader' ? '📷 Instagram' :
               page === 'facebook-downloader' ? '👍 Facebook' :
               page === 'twitter-downloader' ? '🐦 Twitter' :
               page === 'pinterest-downloader' ? '📌 Pinterest' :
               page === 'vimeo-downloader' ? '🎥 Vimeo' :
               page === 'dailymotion-downloader' ? '📺 Dailymotion' :
               page === 'twitch-downloader' ? '🎮 Twitch' :
               page === 'threads-downloader' ? '🧵 Threads' :
               '✂️ CapCut'}
            </button>
          {/each}

          <!-- Audio Downloader -->
          <p class="text-xs font-medium text-slate-500 uppercase tracking-wide px-2 py-1 mt-3">Audio</p>
          <button
            on:click={() => loadPageData('soundcloud-downloader')}
            class="w-full text-left px-3 py-2 rounded-lg transition text-sm {currentPage === 'soundcloud-downloader' ? 'bg-red-600 text-white' : 'bg-slate-50 text-slate-700 hover:bg-slate-100'}"
          >
            🎧 SoundCloud
          </button>
        </div>
      </div>

      <!-- SEO Form -->
      <div class="lg:col-span-3 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 class="text-xl font-bold text-slate-800 mb-6 capitalize flex items-center gap-2">
          {#if currentPage === 'home'}
            🏠 Home
          {:else if currentPage.includes('downloader')}
            {currentPage.replace('-downloader', '').replace('-', ' ')}
          {:else if currentPage.includes('mp3')}
            🎵 YouTube to MP3
          {:else}
            {currentPage}
          {/if}
          Page SEO
        </h2>
        
        <div class="space-y-6">
          <div>
            <label for="meta-title" class="block text-sm font-medium text-slate-700 mb-2">Meta Title</label>
            <input
              id="meta-title"
              type="text"
              bind:value={title}
              placeholder="Page title for search engines"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
            />
            <p class="text-xs text-slate-500 mt-1">Optimal length: 50-60 characters</p>
          </div>

          <div>
            <label for="meta-desc" class="block text-sm font-medium text-slate-700 mb-2">Meta Description</label>
            <textarea
              id="meta-desc"
              bind:value={description}
              rows="3"
              placeholder="Page description for search engines"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none resize-none"
            ></textarea>
            <p class="text-xs text-slate-500 mt-1">Optimal length: 150-160 characters</p>
          </div>

          <div>
            <label for="meta-keywords" class="block text-sm font-medium text-slate-700 mb-2">Keywords</label>
            <input
              id="meta-keywords"
              type="text"
              bind:value={keywords}
              placeholder="keyword1, keyword2, keyword3"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
            />
            <p class="text-xs text-slate-500 mt-1">Comma-separated keywords</p>
          </div>

          <div>
            <label for="og-image" class="block text-sm font-medium text-slate-700 mb-2">Open Graph Image URL</label>
            <input
              id="og-image"
              type="text"
              bind:value={ogImage}
              placeholder="https://example.com/image.jpg"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
            />
            <p class="text-xs text-slate-500 mt-1">Recommended: 1200x630px</p>
          </div>

          {#if saveMessage}
            <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
              {saveMessage}
            </div>
          {/if}

          <div class="pt-4 border-t border-slate-200">
            <button
              on:click={saveSEO}
              disabled={isSaving}
              class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition disabled:opacity-70"
            >
              {isSaving ? 'Saving...' : 'Save SEO Settings'}
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>
