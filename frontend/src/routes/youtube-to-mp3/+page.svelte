<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Downloader from '$lib/components/Downloader.svelte';
  import InfoSection from '$lib/components/InfoSection.svelte';
  import Footer from '$lib/components/Footer.svelte';

  let fetchedData: any = null;
  let pageTitle = 'Free <span class="text-red-600">YouTube to MP3</span> Converter';
  let pageSubtitle = 'Convert YouTube videos to MP3 audio in seconds.';

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
  <InfoSection title="How to Convert YouTube to MP3?" platformName="YouTube to MP3" />
  <Footer />
</div>
