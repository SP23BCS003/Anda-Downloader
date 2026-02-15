<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { API_BASE_URL } from '$lib/api';

  export let data: any;

  let blog: any = null;
  let isLoading = true;
  let error = '';

  const slug = $page.params.slug;

  onMount(async () => {
    try {
        const res = await fetch(`${API_BASE_URL}/api/blogs/${slug}`);
        if (res.ok) {
            blog = await res.json();
        } else {
            error = 'Blog post not found';
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
  {#if blog}
      <title>{blog.meta_title || blog.title} - {data.settings.site_name}</title>
      <meta name="description" content={blog.meta_description || blog.excerpt} />
      
      <!-- Open Graph -->
      <meta property="og:title" content={blog.meta_title || blog.title} />
      <meta property="og:description" content={blog.meta_description || blog.excerpt} />
      {#if blog.featured_image}
        <meta property="og:image" content={blog.featured_image} />
      {/if}
      <meta property="og:type" content="article" />
  {:else}
      <title>Loading... - {data.settings.site_name}</title>
  {/if}
</svelte:head>

<div class="min-h-screen bg-slate-50 font-sans selection:bg-red-200 flex flex-col">
  <Navbar settings={data.settings} />

  <main class="flex-grow pt-28 pb-16 px-4">
      <div class="max-w-4xl mx-auto">
          {#if isLoading}
            <div class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
            </div>
          {:else if error}
             <div class="text-center py-20">
                 <h1 class="text-3xl font-bold text-slate-800 mb-4">404</h1>
                 <p class="text-slate-500 mb-8">{error}</p>
                 <a href="/blogs" class="text-red-600 font-bold hover:underline">Back to Blogs</a>
             </div>
          {:else if blog}
              <article>
                  <header class="mb-10 text-center">
                       <a href="/blogs" class="inline-flex items-center text-red-600 font-bold text-sm mb-6 hover:underline">
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                          Back to Blog
                       </a>
                       
                       <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 mb-6 leading-tight">{blog.title}</h1>
                       
                       <div class="flex items-center justify-center gap-4 text-sm text-slate-500 mb-8">
                           <span class="flex items-center gap-1">
                               <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                               {formatDate(blog.published_at)}
                           </span>
                           {#if blog.author}
                               <span class="w-1 h-1 bg-slate-300 rounded-full"></span>
                               <span class="flex items-center gap-1">
                                   <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                                   {blog.author}
                               </span>
                           {/if}
                       </div>

                       {#if blog.featured_image}
                           <div class="rounded-2xl overflow-hidden shadow-lg mb-10">
                               <img src={blog.featured_image} alt={blog.title} class="w-full h-auto" />
                           </div>
                       {/if}
                  </header>

                  <div class="prose prose-lg md:prose-xl max-w-none text-slate-700 prose-headings:font-bold prose-headings:text-slate-900 prose-a:text-red-600 prose-img:rounded-xl">
                      {@html blog.content}
                  </div>
              </article>
          {/if}
      </div>
  </main>

  <Footer settings={data.settings} />
</div>
