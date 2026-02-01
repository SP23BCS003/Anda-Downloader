<script lang="ts">
  import Navbar from '$lib/components/Navbar.svelte';
  import Footer from '$lib/components/Footer.svelte';
</script>

<div class="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
  <Navbar />
  <div class="pt-32 pb-20 px-6 max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold mb-8 text-slate-800">Terms of Service</h1>
      <div class="prose prose-slate max-w-none bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-gray-600 leading-relaxed">
          <p class="mb-4">Last Updated: January 14, 2026</p>

          <h2 class="text-xl font-bold text-slate-800 mt-8 mb-4">1. Acceptance of Terms</h2>
          <p class="mb-4">By accessing and using Anda-Downloader, you accept and agree to be bound by the terms and provision of this agreement.</p>

          <h2 class="text-xl font-bold text-slate-800 mt-8 mb-4">2. Use License</h2>
          <p class="mb-4">Anda-Downloader is a tool designed to help users download videos for personal use. Users are responsible for checking the copyright terms of the content they download.</p>
          <p class="mb-4">You may not:</p>
          <ul class="list-disc pl-5 mb-4 space-y-2">
              <li>Use the service for any illegal purpose</li>
              <li>Attempt to decompile or reverse engineer any software contained on the website</li>
              <li>Remove any copyright or other proprietary notations from the materials</li>
          </ul>

          <h2 class="text-xl font-bold text-slate-800 mt-8 mb-4">3. Disclaimer</h2>
          <p class="mb-4">The materials on Anda-Downloader's website are provided "as is". Anda-Downloader makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties.</p>
      </div>
  </div>
  <Footer />
</div>
