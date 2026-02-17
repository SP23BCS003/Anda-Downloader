<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { translations, t } from '$lib/i18n';
  import { API_BASE_URL } from '$lib/api';

  export let title = 'Free Online <span class="text-red-600">Video Downloader</span>';
  export let subtitle = 'Download videos from YouTube, Facebook, Instagram, TikTok and more.';

  let url = '';
  let isLoading = false;
  let error = '';
  let showPasteSuccess = false;

  const dispatch = createEventDispatcher();

  $: trans = $translations;

  async function pasteFromClipboard() {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        url = text;
        showPasteSuccess = true;
        setTimeout(() => showPasteSuccess = false, 2000);
        // Auto-fetch if it looks like a URL
        if (text.match(/^https?:\/\//)) {
          setTimeout(() => fetchInfo(), 300);
        }
      }
    } catch (err) {
      console.error('Failed to read clipboard:', err);
      error = t(trans, 'errors.clipboardFailed');
      setTimeout(() => error = '', 3000);
    }
  }

  async function fetchInfo() {
    if (!url) return;
    isLoading = true;
    error = '';
    dispatch('loading', true);
    
    try {
      const res = await fetch(`${API_BASE_URL}/info`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });

      if (!res.ok) {
          const text = await res.text();
          throw new Error(text || res.statusText);
      }
      const data = await res.json();
      dispatch('data', data);
    } catch (e: any) {
      error = e.message || 'Failed to fetch video info';
    } finally {
      isLoading = false;
      dispatch('loading', false);
    }
  }
</script>

<div class="pt-20 md:pt-28 pb-8 md:pb-10 px-4 bg-white">
    <div class="max-w-4xl mx-auto text-center">
      <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold mb-3 md:mb-4 tracking-tight text-slate-800">
        {@html t(trans, 'hero.title')}
      </h1>
      <p class="text-sm sm:text-base text-gray-500 mb-6 md:mb-8 max-w-2xl mx-auto px-4">
        {t(trans, 'hero.subtitle')}
      </p>

      <!-- Input Area -->
      <div class="bg-white p-1.5 rounded-full shadow-lg border border-gray-200 max-w-2xl mx-auto">
        <!-- Desktop Layout -->
        <div class="hidden sm:flex gap-2 items-center">
          <input 
            bind:value={url}
            placeholder={t(trans, 'hero.placeholder')}
            class="flex-1 pl-6 py-3 rounded-full bg-transparent text-gray-700 placeholder-gray-400 focus:outline-none text-base md:text-lg"
            on:keydown={(e) => e.key === 'Enter' && fetchInfo()}
          />
          <button
            on:click={pasteFromClipboard}
            class="px-4 py-3 bg-red-100 hover:bg-red-200 text-red-700 rounded-2xl transition-all flex flex-col items-center justify-center gap-0.5 group min-w-[80px]"
            title={t(trans, 'hero.pasteButton')}
          >
            <div class="relative">
              <svg class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              {#if showPasteSuccess}
                <span class="absolute -top-1 -right-1 flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
              {/if}
            </div>
            <span class="text-[10px] font-bold uppercase tracking-wider">Paste</span>
          </button>
          <button 
            on:click={fetchInfo}
            disabled={isLoading}
            class="px-6 md:px-8 py-3 bg-red-600 hover:bg-red-700 text-white rounded-full font-semibold text-base md:text-lg transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2 min-w-[120px] md:min-w-[140px] justify-center"
          >
            {#if isLoading}
              <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            {:else}
              {t(trans, 'hero.downloadButton')}
            {/if}
          </button>
        </div>

        <!-- Mobile Layout -->
        <div class="sm:hidden flex flex-col gap-3 p-1">
          <!-- Row 1: Input + Paste -->
          <div class="flex gap-2">
            <input 
              bind:value={url}
              placeholder={t(trans, 'hero.placeholderMobile')}
              class="flex-1 min-w-0 px-4 py-2.5 rounded-full bg-gray-50 border border-gray-200 text-gray-700 placeholder-gray-400 focus:outline-none focus:border-red-300 focus:ring-2 focus:ring-red-100 text-sm"
              on:keydown={(e) => e.key === 'Enter' && fetchInfo()}
            />
            <button
              on:click={pasteFromClipboard}
              class="px-3 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-xl transition-all flex items-center justify-center gap-1.5 shrink-0"
              title={t(trans, 'hero.paste')}
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <span class="text-xs font-bold uppercase tracking-wide">Paste</span>
            </button>
          </div>

          <!-- Row 2: Download Button -->
          <button 
            on:click={fetchInfo}
            disabled={isLoading}
            class="w-full py-3 bg-red-600 hover:bg-red-700 text-white rounded-xl font-bold text-sm transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm shadow-red-200"
          >
            {#if isLoading}
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {t(trans, 'hero.loading')}
            {:else}
              {t(trans, 'hero.downloadButtonMobile')}
            {/if}
          </button>
        </div>
      </div>
      
      {#if error}
        <div class="mt-4 md:mt-8 p-3 md:p-4 bg-red-50 border border-red-100 text-red-600 rounded-lg max-w-2xl mx-auto text-sm md:text-base font-medium">
          ⚠️ {error}
        </div>
      {/if}
    </div>
</div>
