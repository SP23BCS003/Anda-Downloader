<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Hero from '$lib/components/Hero.svelte';
  import Downloader from '$lib/components/Downloader.svelte';
  import InfoSection from '$lib/components/InfoSection.svelte';
  import Footer from '$lib/components/Footer.svelte';

  let fetchedData: any = null;
  // Default title for Home
  let currentTitle = 'Free Online <span class="text-red-600">Video Downloader</span>';

  function handleData(event: CustomEvent) {
      fetchedData = event.detail;
  }

  function handleLoading(event: CustomEvent) {
      if(event.detail === true) {
          fetchedData = null; // Reset results on new fetch
      }
  }
</script>

<div class="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
  <Navbar />
  
  <Hero 
    title={currentTitle}
    on:data={handleData} 
    on:loading={handleLoading}
  />
  
  {#if fetchedData}
      <Downloader data={fetchedData} />
  {/if}

  <InfoSection />
  
  <Footer />
</div>
