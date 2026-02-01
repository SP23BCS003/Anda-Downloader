<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Downloader from '$lib/components/Downloader.svelte';
  import InfoSection from '$lib/components/InfoSection.svelte';
  import Footer from '$lib/components/Footer.svelte';

  let fetchedData: any = null;
  let pageTitle = 'TikTok <span class="text-red-600">Video Downloader</span> Without Watermark';
  let pageSubtitle = 'Download TikTok videos without watermark in HD quality.';

  function handleData(event: CustomEvent) {
      fetchedData = event.detail;
  }

  function handleLoading(event: CustomEvent) {
      if(event.detail === true) fetchedData = null;
  }
</script>

<div class="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
  <Navbar />
  <Hero title={pageTitle} subtitle={pageSubtitle} on:data={handleData} on:loading={handleLoading} />
  {#if fetchedData}<Downloader data={fetchedData} />{/if}
  <InfoSection title="How to Download TikTok Videos?" platformName="TikTok Downloader" />
  <Footer />
</div>
