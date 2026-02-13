<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Downloader from '$lib/components/Downloader.svelte';
  import InfoSection from '$lib/components/InfoSection.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import SEOHead from '$lib/components/SEOHead.svelte';

  export let data: any;

  let fetchedData: any = null;

  $: seo = (data.seo && data.seo['youtube-to-mp3']) || {};
  $: pageTitle = seo.title || 'YouTube to <span class="text-red-600">MP3 Converter</span>';
  $: pageSubtitle = seo.description || 'Convert and download YouTube videos to MP3 instantly.';

  function handleData(event: CustomEvent) {
      fetchedData = event.detail;
  }

  function handleLoading(event: CustomEvent) {
      if(event.detail === true) fetchedData = null;
  }
</script>

<SEOHead pageId="youtube-to-mp3" seoData={data.seo} />

<div class="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
  <Navbar settings={data.settings} />
  <Hero title={pageTitle} subtitle={pageSubtitle} on:data={handleData} on:loading={handleLoading} />
  {#if fetchedData}<Downloader data={fetchedData} />{/if}
  <InfoSection title="How to Convert YouTube to MP3?" platformName="YouTube to MP3" />
  <Footer settings={data.settings} />
</div>
