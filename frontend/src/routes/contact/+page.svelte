<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
  import SEOHead from '$lib/components/SEOHead.svelte';

  export let data: any;
  $: settings = data.settings || {};
</script>

<SEOHead pageId="contact" seoData={data.seo} />

<div class="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
  <Navbar settings={data.settings} />
  <div class="pt-32 pb-20 px-6 max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-slate-800">Contact Us</h1>
      <div class="prose prose-slate max-w-none bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <p class="text-lg text-gray-600 mb-6">
              We value your feedback and are here to help with any questions or issues you may have. 
              Please reach out to us using the contact information below.
          </p>
          
          <div class="space-y-4">
              <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                  <span class="font-bold text-gray-700">Email:</span>
                  <a href="mailto:{settings.contact_email || 'support@anda-downloader.com'}" class="text-red-600 hover:underline">{settings.contact_email || 'support@anda-downloader.com'}</a>
              </div>
              <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                  <span class="font-bold text-gray-700">Twitter:</span>
                  <a href="https://twitter.com/AndaDownloader" target="_blank" rel="noopener noreferrer" class="text-red-600 hover:underline">@AndaDownloader</a>
              </div>
          </div>

          <h3 class="text-2xl font-bold mt-12 mb-4 text-slate-800">Common Questions</h3>
          <p class="text-gray-600">
              Before contacting us, please check our <a href="/#faq" class="text-red-600 hover:underline">FAQ section</a> as your question might already be answered there.
          </p>
      </div>
  </div>
  <Footer settings={data.settings} />
</div>
