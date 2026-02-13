<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Downloader from '$lib/components/Downloader.svelte';
  import InfoSection from '$lib/components/InfoSection.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import SEOHead from '$lib/components/SEOHead.svelte';

  export let data: any;

  let fetchedData: any = null;

  $: seo = (data.seo && data.seo['facebook-downloader']) || {};
  $: pageTitle = seo.title || 'Facebook <span class="text-red-600">Video Downloader</span>';
  $: pageSubtitle = seo.description || 'Download public and private Facebook videos in 1080p.';

  function handleData(event: CustomEvent) {
      fetchedData = event.detail;
  }

  function handleLoading(event: CustomEvent) {
      if(event.detail === true) fetchedData = null;
  }
</script>

<SEOHead pageId="facebook-downloader" seoData={data.seo} />

<div class="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
  <Navbar settings={data.settings} />
  <Hero title={pageTitle} subtitle={pageSubtitle} on:data={handleData} on:loading={handleLoading} />
  {#if fetchedData}<Downloader data={fetchedData} />{/if}
  <InfoSection title="How to Download Facebook Videos?" platformName="Facebook Downloader" />
  <Footer settings={data.settings} />
</div>
