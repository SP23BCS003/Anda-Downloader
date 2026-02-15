<script lang="ts">
  import { currentLanguage, translations, languages, setLanguage, t } from '$lib/i18n';
  
  export let settings: any = {};

  let isMobileMenuOpen = false;
  let isLangDropdownOpen = false;
  
  $: currentLangCode = $currentLanguage;
  $: currentLangName = languages[currentLangCode as keyof typeof languages]?.split(' ')[0] || 'EN';
  $: trans = $translations;

  function toggleMobileMenu() {
    isMobileMenuOpen = !isMobileMenuOpen;
    isLangDropdownOpen = false;
  }

  function closeMobileMenu() {
    isMobileMenuOpen = false;
  }

  function toggleLangDropdown() {
    isLangDropdownOpen = !isLangDropdownOpen;
  }

  function changeLang(lang: string) {
    setLanguage(lang);
    isLangDropdownOpen = false;
  }
  function handleWindowClick(e: MouseEvent) {
    const target = e.target as HTMLElement;
    if (!target.closest('[class*="relative"]')) {
      isLangDropdownOpen = false;
    }
  }
</script>

<nav class="bg-white border-b border-gray-100 py-3 md:py-4 px-4 md:px-6 fixed w-full z-10 top-0 shadow-sm">
  <div class="max-w-6xl mx-auto flex items-center justify-between">
      <div class="flex items-center gap-2">
         <a href="/" class="flex items-center gap-2 group">
            <div class="w-7 h-7 md:w-8 md:h-8 bg-red-600 rounded-lg flex items-center justify-center text-white font-bold text-lg md:text-xl group-hover:scale-110 transition-transform">A</div>
            <span class="text-lg md:text-xl font-bold tracking-tight text-gray-800 group-hover:text-red-600 transition-colors">
              {#if settings.site_name}
                {settings.site_name}
              {:else}
                Anda-<span class="text-red-600 group-hover:text-gray-800 transition-colors">Downloader</span>
              {/if}
            </span>
        </a>
      </div>

      <!-- Desktop Menu -->
      <div class="hidden md:flex items-center gap-6">
          <a href="/blogs" class="text-sm font-medium text-gray-500 hover:text-red-600 transition-colors">Blogs</a>
          <a href="#how-to-download" class="text-sm font-medium text-gray-500 hover:text-red-600 transition-colors">{t(trans, 'nav.howToDownload')}</a>
          <a href="#supported-sites" class="text-sm font-medium text-gray-500 hover:text-red-600 transition-colors">{t(trans, 'nav.supportedSites')}</a>
          <a href="#faq" class="text-sm font-medium text-gray-500 hover:text-red-600 transition-colors">{t(trans, 'nav.faq')}</a>
          
          <!-- Language Selector -->
          <div class="relative">
              <button
                  on:click={toggleLangDropdown}
                  class="flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-red-600 transition-colors px-3 py-1.5 rounded-lg hover:bg-red-50"
              >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                  </svg>
                  {currentLangName}
                  <svg class="w-3 h-3 transition-transform {isLangDropdownOpen ? 'rotate-180' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
              </button>
              
              {#if isLangDropdownOpen}
                  <div class="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 py-2 max-h-96 overflow-y-auto z-20">
                      {#each Object.entries(languages) as [code, name]}
                          <button
                              on:click={() => changeLang(code)}
                              class="w-full text-left px-4 py-2 text-sm hover:bg-red-50 transition-colors {currentLangCode === code ? 'bg-red-50 text-red-600 font-medium' : 'text-gray-700'}"
                          >
                              {name}
                          </button>
                      {/each}
                  </div>
              {/if}
          </div>
      </div>

      <!-- Mobile Menu Button -->
      <button
          on:click={toggleMobileMenu}
          class="md:hidden p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
          aria-label="Toggle menu"
      >
          {#if isMobileMenuOpen}
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
          {:else}
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
          {/if}
      </button>
  </div>

  <!-- Mobile Menu -->
  {#if isMobileMenuOpen}
      <div class="md:hidden mt-4 pb-4 space-y-2 border-t border-gray-100 pt-4">
          <a href="/blogs" on:click={closeMobileMenu} class="block px-4 py-2 text-sm font-medium text-gray-700 hover:bg-red-50 hover:text-red-600 rounded-lg transition-all">Blogs</a>
          <a href="#how-to-download" on:click={closeMobileMenu} class="block px-4 py-2 text-sm font-medium text-gray-700 hover:bg-red-50 hover:text-red-600 rounded-lg transition-all">{t(trans, 'nav.howToDownload')}</a>
          <a href="#supported-sites" on:click={closeMobileMenu} class="block px-4 py-2 text-sm font-medium text-gray-700 hover:bg-red-50 hover:text-red-600 rounded-lg transition-all">{t(trans, 'nav.supportedSites')}</a>
          <a href="#faq" on:click={closeMobileMenu} class="block px-4 py-2 text-sm font-medium text-gray-700 hover:bg-red-50 hover:text-red-600 rounded-lg transition-all">{t(trans, 'nav.faq')}</a>
          
          <div class="px-4 py-2">
              <p class="text-xs font-medium text-gray-500 mb-2">{t(trans, 'nav.language')}</p>
              <div class="grid grid-cols-2 gap-2">
                  {#each Object.entries(languages).slice(0, 6) as [code, name]}
                      <button
                          on:click={() => { changeLang(code); closeMobileMenu(); }}
                          class="text-left px-3 py-2 text-xs rounded-lg {currentLangCode === code ? 'bg-red-600 text-white font-medium' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} transition-all"
                      >
                          {name.split('(')[0].trim()}
                      </button>
                  {/each}
              </div>
          </div>
      </div>
  {/if}
</nav>

<!-- Close dropdowns when clicking outside -->
<svelte:window on:click={handleWindowClick} />
