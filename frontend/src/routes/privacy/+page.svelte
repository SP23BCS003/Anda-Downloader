<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import SEOHead from '$lib/components/SEOHead.svelte';

  export let data: any;
</script>

<SEOHead pageId="privacy" seoData={data.seo} />

<div class="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
  <Navbar settings={data.settings} />
  <div class="pt-32 pb-20 px-6 max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-slate-800">Privacy Policy</h1>
      <div class="prose prose-slate max-w-none bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-gray-600 leading-relaxed">
           <p class="mb-4">Last Updated: January 14, 2026</p>

          <h2 class="text-xl font-bold text-slate-800 mt-8 mb-4">1. Information We Collect</h2>
          <p class="mb-4">We do not collect any personal information from our users. You can use our service without registration. We may collect anonymous usage data (like browser type, time of visit) to improve our service.</p>

          <h2 class="text-xl font-bold text-slate-800 mt-8 mb-4">2. Cookies</h2>
          <p class="mb-4">We use cookies to enhance your experience. You can choose to disable cookies through your browser settings.</p>

          <h2 class="text-xl font-bold text-slate-800 mt-8 mb-4">3. Download History</h2>
          <p class="mb-4">We do not store a history of your downloads. All file processing is temporary and files are deleted from our servers shortly after processing.</p>
          
           <h2 class="text-xl font-bold text-slate-800 mt-8 mb-4">4. Third-Party Links</h2>
          <p class="mb-4">Our website may contain links to other websites. We are not responsible for the privacy practices of other sites.</p>
      </div>
  </div>
  <Footer settings={data.settings} />
</div>
