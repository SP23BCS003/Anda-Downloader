<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import { API_BASE_URL } from '$lib/api';
  
  export let data: any;

  let blogs: any[] = [];
  let isLoading = true;
  let error = '';

  import { onMount } from 'svelte';

  onMount(async () => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/blogs`);
        if (res.ok) {
            blogs = await res.json();
        } else {
            error = 'Failed to load blogs';
        }
    } catch (e: any) {
        error = e.message;
    } finally {
        isLoading = false;
    }
  });

  function formatDate(dateStr: string) {
      if(!dateStr) return '';
      return new Date(dateStr).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
      });
  }
</script>

<svelte:head>
  <title>Our Blog - {data.settings.site_name || 'Anda-Downloader'}</title>
  <meta name="description" content="Read our latest updates, guides, and news about video downloading." />
</svelte:head>

<div class="min-h-screen bg-slate-50 font-sans selection:bg-red-200 flex flex-col">
  <Navbar settings={data.settings} />

  <main class="flex-grow pt-28 pb-16 px-4">
      <div class="max-w-6xl mx-auto">
          <h1 class="text-4xl font-extrabold text-slate-800 mb-2 text-center">Our Blog</h1>
          <p class="text-slate-500 text-center mb-12 max-w-2xl mx-auto">Latest news, updates, and guides from our team.</p>

          {#if isLoading}
            <div class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
            </div>
          {:else if error}
             <div class="text-center text-red-600 py-10 bg-red-50 rounded-xl">
                 {error}
             </div>
          {:else if blogs.length === 0}
             <div class="text-center text-gray-500 py-20 bg-white rounded-xl shadow-sm border border-gray-100">
                 No blog posts found. Check back later!
             </div>
          {:else}
              <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {#each blogs as blog}
                      <a href="/blogs/{blog.slug}" class="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all group border border-gray-100 hover:border-red-100 block">
                          {#if blog.featured_image}
                              <div class="aspect-video overflow-hidden bg-gray-100">
                                  <img src={blog.featured_image} alt={blog.title} class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                              </div>
                          {:else}
                              <div class="aspect-video bg-gray-100 flex items-center justify-center text-gray-300">
                                  <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                              </div>
                          {/if}
                          
                          <div class="p-6">
                              <div class="text-xs font-bold text-red-600 uppercase tracking-wider mb-2">
                                  {formatDate(blog.published_at)}
                              </div>
                              <h2 class="text-xl font-bold text-slate-800 mb-3 group-hover:text-red-600 transition-colors line-clamp-2 leading-tight">
                                  {blog.title}
                              </h2>
                              <p class="text-slate-500 text-sm line-clamp-3 mb-4 leading-relaxed">
                                  {blog.excerpt || 'No excerpt available.'}
                              </p>
                              <span class="text-red-600 font-bold text-sm flex items-center gap-1 group-hover:gap-2 transition-all">
                                  Read Article <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                              </span>
                          </div>
                      </a>
                  {/each}
              </div>
          {/if}
      </div>
  </main>

  <Footer settings={data.settings} />
</div>
