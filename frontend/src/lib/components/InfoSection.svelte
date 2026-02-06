<script lang="ts">
  import SupportedSites from '$lib/components/SupportedSites.svelte';

  export let title = 'How to Download Videos with Anda-Downloader?';
  export let platformName = 'Anda-Downloader';

  const commonFaqs = [
      { q: `Is ${platformName} free to use?`, a: `Yes, ${platformName} is completely free. No hidden fees, no subscriptions.` },
      { q: 'Do I need to install any software?', a: `No. ${platformName} is fully web-based. It works on Chrome, Safari, Firefox, and Edge.` },
      { q: 'Where are videos saved?', a: 'Videos are saved in your default "Downloads" folder.' },
      { q: 'What formats are supported?', a: 'We support MP4 (SD, HD, 4K), MP3, WEBM, and M4A. You can select your preferred quality before downloading.' },
      { q: 'Is it safe to use?', a: 'Absolutely. We do not host any videos or store copies. All downloads come directly from the source server to your device.' },
      { q: 'Can I download Live videos?', a: 'Yes, once the live stream has ended and the video is processed by the platform, you can download it just like any other video.' },
      { q: 'Are there download limits?', a: 'No limits. Download as many videos as you want, 24/7.' }
  ];
</script>

<div class="space-y-20">

    <!-- Why Choose Section (Interactive Grid) -->
    <div class="max-w-6xl mx-auto px-6 pt-16">
        <h2 class="text-3xl font-bold mb-12 text-center text-slate-800">Why Choose {platformName}?</h2>
        <div class="grid md:grid-cols-3 gap-8">
            <div class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group">
                <div class="w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                    <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                </div>
                <h3 class="text-xl font-bold mb-3 text-gray-800">Lightning Fast</h3>
                <p class="text-gray-500 leading-relaxed">Our advanced servers ensure the fastest download speeds available, even for 4K content.</p>
            </div>
            
            <div class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group">
                <div class="w-14 h-14 bg-purple-100 text-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                    <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                </div>
                <h3 class="text-xl font-bold mb-3 text-gray-800">100% Secure</h3>
                <p class="text-gray-500 leading-relaxed">No data retention. No tracking. SSL encrypted. Your privacy is guaranteed.</p>
            </div>

            <div class="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group">
                <div class="w-14 h-14 bg-green-100 text-green-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                    <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path></svg>
                </div>
                <h3 class="text-xl font-bold mb-3 text-gray-800">Top Quality</h3>
                <p class="text-gray-500 leading-relaxed">Download in original quality. We support HD, Full HD, 4K, and 8K resolutions.</p>
            </div>
        </div>
    </div>

    <!-- How to Download Section (Steps) -->
    <div id="how-to-download" class="bg-gradient-to-b from-white to-slate-50 py-20 px-6">
        <div class="max-w-5xl mx-auto">
            <h2 class="text-3xl font-bold mb-16 text-center text-slate-800">{title}</h2>
            <div class="relative grid md:grid-cols-3 gap-10">
                <!-- Connector Line (Desktop) -->
                <div class="hidden md:block absolute top-12 left-1/6 right-1/6 h-0.5 bg-gray-200 -z-10"></div>
                
                <div class="relative bg-white p-8 rounded-3xl shadow-sm border border-gray-100 text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-2">
                    <div class="w-20 h-20 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-3xl shadow-lg mx-auto mb-6 border-4 border-white">1</div>
                    <h3 class="font-bold text-xl mb-3 text-gray-800">Paste Link</h3>
                    <p class="text-gray-500">Copy the URL of the video you want to download and paste it into the search box.</p>
                </div>

                <div class="relative bg-white p-8 rounded-3xl shadow-sm border border-gray-100 text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-2">
                    <div class="w-20 h-20 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-3xl shadow-lg mx-auto mb-6 border-4 border-white">2</div>
                    <h3 class="font-bold text-xl mb-3 text-gray-800">Choose Quality</h3>
                    <p class="text-gray-500">Wait a moment for processing, then select your desired format (MP4/MP3) and quality.</p>
                </div>

                <div class="relative bg-white p-8 rounded-3xl shadow-sm border border-gray-100 text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-2">
                    <div class="w-20 h-20 bg-red-600 text-white rounded-full flex items-center justify-center font-bold text-3xl shadow-lg mx-auto mb-6 border-4 border-white">3</div>
                    <h3 class="font-bold text-xl mb-3 text-gray-800">Download</h3>
                    <p class="text-gray-500">Click the Download button. The file will be saved to your device immediately.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Supported Sites -->
    <SupportedSites />

    <!-- FAQ Moved Above Formats -->
    <div id="faq" class="bg-slate-50 py-16 px-6">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-2xl font-bold mb-8 text-center text-slate-800">Frequently Asked Questions</h2>
            <div class="space-y-4">
                {#each commonFaqs as faq}
                <details class="group bg-white rounded-2xl border border-gray-100 open:shadow-md transition-all duration-300">
                    <summary class="flex justify-between items-center font-bold cursor-pointer list-none p-5 text-gray-800 group-open:text-red-600 select-none">
                        <span>{faq.q}</span>
                        <span class="transition-transform duration-300 group-open:rotate-180 text-gray-400 group-open:text-red-600">
                            <svg fill="none" height="20" width="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"></path></svg>
                        </span>
                    </summary>
                    <p class="text-gray-600 mt-0 px-5 pb-5 text-sm leading-relaxed animate-in fade-in slide-in-from-top-2 duration-200">
                        {faq.a}
                    </p>
                </details>
                {/each}
            </div>
        </div>
    </div>

    <!-- Supported Formats & Tools -->
    <div class="bg-white py-16 px-6">
        <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-16">
            <!-- Supported Formats -->
            <div>
                <h2 class="text-2xl font-bold mb-8 text-slate-800">Supported Formats</h2>
                <div class="flex flex-wrap gap-3">
                    {#each ['MP4', 'MP3', 'WEBM', 'M4A', '3GP', 'JPG', 'PNG'] as fmt}
                        <span class="px-5 py-2.5 bg-gray-50 hover:bg-gray-100 border border-gray-200 hover:border-gray-300 rounded-xl text-gray-700 font-bold transition-all cursor-default hover:scale-105 shadow-sm">
                            {fmt}
                        </span>
                    {/each}
                </div>
            </div>

            <!-- Popular Tools -->
            <div>
                 <h2 class="text-2xl font-bold mb-8 text-slate-800">Popular Tools</h2>
                <div class="grid grid-cols-2 gap-4">
                    {#each [
                        {name: 'YouTube Downloader', url: '/youtube-downloader', color: 'bg-red-500'},
                        {name: 'TikTok Downloader', url: '/tiktok-downloader', color: 'bg-black'},
                        {name: 'Instagram Downloader', url: '/instagram-downloader', color: 'bg-pink-600'},
                        {name: 'Facebook Downloader', url: '/facebook-downloader', color: 'bg-blue-600'}
                    ] as tool}
                    <a href={tool.url} class="group flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition-colors">
                        <span class="w-2 h-2 rounded-full {tool.color} ring-2 ring-white shadow-sm"></span>
                        <span class="font-medium text-gray-600 group-hover:text-gray-900">{tool.name}</span>
                    </a>
                    {/each}
                </div>
            </div>
        </div>
    </div>
</div>
