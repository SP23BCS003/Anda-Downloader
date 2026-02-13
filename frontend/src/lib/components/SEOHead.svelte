<script lang="ts">
  export let pageId: string;
  export let seoData: Record<string, any> = {};

  $: pageSeo = seoData[pageId] || {};
  $: title = pageSeo.title || 'Video Downloader';
  $: description = pageSeo.description || 'Download videos from multiple platforms.';
  $: keywords = pageSeo.keywords || 'video downloader, free downloader';
  $: ogImage = pageSeo.og_image || '';
</script>

<svelte:head>
  <title>{title}</title>
  <meta name="description" content={description} />
  <meta name="keywords" content={keywords} />
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  {#if ogImage}
    <meta property="og:image" content={ogImage} />
  {/if}

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:title" content={title} />
  <meta property="twitter:description" content={description} />
  {#if ogImage}
    <meta property="twitter:image" content={ogImage} />
  {/if}
</svelte:head>
