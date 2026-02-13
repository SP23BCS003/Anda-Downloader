<script lang="ts">
  import { API_BASE_URL } from '$lib/api';
  
  export let data: any = null;

  let activeTab = 'video';
  let downloading = false;
  let downloadReady = false;
  let progress = 0;
  let statusText = 'Starting...';
  let finalDownloadUrl = '';
  
  // Advanced Tab State
  let advFormat = 'mp4';
  let advQuality = '';
  let startTime = '00:00:00';
  let endTime = '00:00:10';

  // We need 'url' for downloading, let's extract it from data if possible or pass it?
  // The 'data' object usually has 'original_url' or 'webpage_url' from yt-dlp info.
  // Assuming data.webpage_url is available. If not, we might need to pass url as prop.
  // Let's rely on data.webpage_url or webpage_url_basename? 
  // Actually, yt-dlp dump-json includes 'webpage_url'.
  // But wait, the previous code used a specific 'url' variable.
  // Let's add 'url' as a prop to be safe.
  export let url = ''; 

  async function download(format_id: string, start?: string, end?: string) {
    if (downloading) return;
    downloading = true;
    downloadReady = false;
    progress = 0;
    statusText = 'Starting...';

    try {
        const payload: any = { url: url || data.webpage_url, format_id };
        if (start && end) {
            payload.start_time = start;
            payload.end_time = end;
        }

        const startRes = await fetch(`${API_BASE_URL}/start_download`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        
        if (!startRes.ok) throw new Error('Failed to start download');
        const { job_id } = await startRes.json();

        const interval = setInterval(async () => {
            try {
                const statusRes = await fetch(`${API_BASE_URL}/status/${job_id}`);
                const job = await statusRes.json();
                
                if (job.status === 'downloading') {
                    progress = job.progress || 0;
                    statusText = `Server Downloading... ${progress.toFixed(1)}%`;
                } else if (job.status === 'processing') {
                     progress = 100;
                     statusText = 'Processing file...';
                } else if (job.status === 'completed') {
                    clearInterval(interval);
                    progress = 100;
                    statusText = 'File Ready!';
                    downloadReady = true;
                    finalDownloadUrl = `${API_BASE_URL}/serve_file/${job_id}`;
                } else if (job.status === 'error') {
                    clearInterval(interval);
                    alert(`Error: ${job.error}`);
                    downloading = false;
                }
            } catch (e) {
                console.error(e);
            }
        }, 250);

    } catch (e: any) {
        alert(e.message);
        downloading = false;
    }
  }

  function triggerFileSave() {
      const link = document.createElement('a');
      link.href = finalDownloadUrl;
      link.setAttribute('download', '');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      setTimeout(() => {
          downloading = false;
          downloadReady = false;
      }, 1000);
  }
</script>

{#if data}
<div class="max-w-6xl mx-auto px-4 pb-20 animate-in fade-in slide-in-from-bottom-8 duration-500">
  <div class="flex flex-col lg:flex-row gap-8 items-start">
      
      <!-- Left: Thumbnail & Info -->
      <div class="w-full lg:w-1/3 space-y-4">
          <div class="bg-black rounded-xl overflow-hidden shadow-lg relative aspect-video">
              {#if data.thumbnail}
                <img src={data.thumbnail} alt={data.title} class="w-full h-full object-contain" />
              {/if}
              <div class="absolute bottom-2 right-2 bg-black/80 text-white text-xs px-2 py-1 rounded">
                  {data.duration ? new Date(data.duration * 1000).toISOString().substr(11, 8) : 'HD'}
              </div>
          </div>
          <h2 class="text-xl font-bold text-gray-800 leading-snug">{data.title}</h2>
          <p class="text-sm text-gray-500">Source: {data.extractor_key || 'Unknown'}</p>
      </div>

      <!-- Right: Tabs & Downloads -->
      <div class="w-full lg:w-2/3">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
              <!-- Tabs Header -->
              <div class="flex bg-gray-50 border-b border-gray-200">
                  <button 
                    class="flex-1 py-4 font-bold text-center flex items-center justify-center gap-2 transition-colors {activeTab === 'video' ? 'text-white bg-red-600' : 'text-gray-600 hover:bg-gray-100'}"
                    on:click={() => activeTab = 'video'}
                  >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.818v6.364a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                      Video
                  </button>
                  <button 
                    class="flex-1 py-4 font-bold text-center flex items-center justify-center gap-2 transition-colors {activeTab === 'audio' ? 'text-white bg-red-600' : 'text-gray-600 hover:bg-gray-100'}"
                    on:click={() => activeTab = 'audio'}
                  >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
                      Audio
                  </button>
                  <button 
                    class="flex-1 py-4 font-bold text-center flex items-center justify-center gap-2 transition-colors {activeTab === 'advanced' ? 'text-white bg-red-600' : 'text-gray-600 hover:bg-gray-100'}"
                    on:click={() => activeTab = 'advanced'}
                  >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                      Advanced
                  </button>
              </div>

              <!-- Content -->
              <div class="p-0">
                  {#if activeTab === 'video'}
                    <!-- Mobile Card Layout -->
                    <div class="md:hidden divide-y divide-gray-100">
                        {#each data.formats.filter((f: any) => f.quality !== 'audio') as fmt}
                        <div class="p-4 hover:bg-gray-50 transition-colors">
                            <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center gap-2">
                                    <span class="font-bold text-gray-800 uppercase">{fmt.ext}</span>
                                    <span class="text-gray-400">-</span>
                                    <span class="font-medium text-gray-600">{fmt.quality}</span>
                                    {#if fmt.quality === '1080p' || fmt.quality === '2160p'}
                                        <span class="px-1.5 py-0.5 bg-blue-500 text-white text-[10px] uppercase font-bold rounded-sm">HD</span>
                                    {/if}
                                </div>
                                <span class="text-gray-500 font-mono text-xs">
                                    {#if fmt.filesize}
                                        {(fmt.filesize / 1024 / 1024).toFixed(1)} MB
                                    {:else}
                                        --
                                    {/if}
                                </span>
                            </div>
                            <button 
                                on:click={() => download(fmt.format_id)}
                                class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded-lg shadow-sm transition-all hover:shadow-md"
                            >
                                Download
                            </button>
                        </div>
                        {/each}
                    </div>
                    
                    <!-- Desktop Table Layout -->
                    <div class="hidden md:block overflow-x-auto">
                        <table class="w-full min-w-[400px]">
                            <thead>
                                <tr class="bg-white border-b border-gray-100 text-left text-sm font-bold text-gray-700">
                                    <th class="p-4 pl-6">File type</th>
                                    <th class="p-4">File size</th>
                                    <th class="p-4 pr-6 text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-50">
                                {#each data.formats.filter((f: any) => f.quality !== 'audio') as fmt}
                                <tr class="hover:bg-gray-50 transition-colors group">
                                    <td class="p-4 pl-6">
                                        <div class="flex items-center gap-2">
                                            <span class="font-bold text-gray-800 uppercase">{fmt.ext}</span>
                                            <span class="text-gray-400">-</span>
                                            <span class="font-medium text-gray-600">{fmt.quality}</span>
                                            {#if fmt.quality === '1080p' || fmt.quality === '2160p'}
                                                <span class="px-1.5 py-0.5 bg-blue-500 text-white text-[10px] uppercase font-bold rounded-sm">HD</span>
                                            {/if}
                                        </div>
                                    </td>
                                    <td class="p-4 text-gray-500 font-mono text-sm">
                                        {#if fmt.filesize}
                                            {(fmt.filesize / 1024 / 1024).toFixed(1)} MB
                                        {:else}
                                            --
                                        {/if}
                                    </td>
                                    <td class="p-4 pr-6 text-right">
                                        <button 
                                            on:click={() => download(fmt.format_id)}
                                            class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded shadow-sm transition-all hover:shadow-md"
                                        >
                                            Download
                                        </button>
                                    </td>
                                </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                  {:else if activeTab === 'audio'}
                    <!-- Mobile Card Layout -->
                    <div class="md:hidden divide-y divide-gray-100">
                        {#each data.formats.filter((f: any) => f.quality === 'audio') as fmt}
                        <div class="p-4 hover:bg-gray-50 transition-colors">
                            <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center gap-2">
                                    <span class="font-bold text-gray-800 uppercase">{fmt.ext}</span>
                                    <span class="text-gray-400">-</span>
                                    <span class="font-medium text-gray-600">128kbps</span>
                                </div>
                                <span class="text-gray-500 font-mono text-xs">-- MB</span>
                            </div>
                            <button 
                                on:click={() => download(fmt.format_id)}
                                class="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded-lg shadow-sm transition-all hover:shadow-md"
                            >
                                Download
                            </button>
                        </div>
                        {/each}
                    </div>

                    <!-- Desktop Table Layout -->
                    <div class="hidden md:block overflow-x-auto">
                        <table class="w-full">
                            <thead>
                                <tr class="bg-white border-b border-gray-100 text-left text-sm font-bold text-gray-700">
                                    <th class="p-4 pl-6">File type</th>
                                    <th class="p-4">File size</th>
                                    <th class="p-4 pr-6 text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-50">
                                {#each data.formats.filter((f: any) => f.quality === 'audio') as fmt}
                                <tr class="hover:bg-gray-50 transition-colors">
                                    <td class="p-4 pl-6">
                                        <span class="font-bold text-gray-800 uppercase">{fmt.ext}</span>
                                        <span class="text-gray-400">-</span>
                                        <span class="font-medium text-gray-600">128kbps</span>
                                    </td>
                                    <td class="p-4 text-gray-500 font-mono text-sm">-- MB</td>
                                    <td class="p-4 pr-6 text-right">
                                        <button 
                                            on:click={() => download(fmt.format_id)}
                                            class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded shadow-sm transition-all hover:shadow-md"
                                        >
                                            Download
                                        </button>
                                    </td>
                                </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                  {:else}
                     <div class="p-8 space-y-6">
                        <div class="grid md:grid-cols-2 gap-6">
                            <div class="space-y-2">
                                <label class="block text-sm font-bold text-gray-700">1. Select format:</label>
                                <select bind:value={advFormat} class="w-full p-2.5 border border-gray-300 rounded-lg text-gray-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none">
                                    <option value="mp4">Video (.MP4)</option>
                                    <option value="mp3">Audio (.MP3)</option>
                                </select>
                            </div>
                            <div class="space-y-2">
                                <label class="block text-sm font-bold text-gray-700">2. Select quality:</label>
                                <select bind:value={advQuality} class="w-full p-2.5 border border-gray-300 rounded-lg text-gray-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none">
                                    {#if advFormat === 'mp4'}
                                        {#each data.formats.filter((f: any) => f.quality !== 'audio') as fmt}
                                            <option value={fmt.format_id}>{fmt.quality} ({((fmt.filesize || 0)/1024/1024).toFixed(1)} MB)</option>
                                        {/each}
                                    {:else}
                                         {#each data.formats.filter((f: any) => f.quality === 'audio') as fmt}
                                            <option value={fmt.format_id}>Audio (Best)</option>
                                        {/each}
                                    {/if}
                                </select>
                            </div>
                        </div>
                        
                        <div class="space-y-4">
                            <label class="block text-sm font-bold text-gray-700">3. Cut Video (Start - End time):</label>
                            <div class="flex gap-4">
                                 <div class="flex items-center gap-2 bg-gray-50 px-3 py-2 rounded border border-gray-200 flex-1">
                                     <span class="text-xs font-bold text-gray-500 uppercase">Start</span>
                                     <input bind:value={startTime} type="text" class="bg-transparent font-mono text-gray-800 w-full outline-none" placeholder="00:00:00" />
                                 </div>
                                 <div class="flex items-center gap-2 bg-gray-50 px-3 py-2 rounded border border-gray-200 flex-1">
                                     <span class="text-xs font-bold text-gray-500 uppercase">End</span>
                                     <input bind:value={endTime} type="text" class="bg-transparent font-mono text-gray-800 w-full outline-none" placeholder="00:10:00" />
                                 </div>
                            </div>
                            <p class="text-xs text-gray-400">Format: HH:MM:SS (e.g. 00:01:30)</p>
                        </div>

                         <button 
                            on:click={() => {
                                if (advQuality) download(advQuality, startTime, endTime);
                                else alert('Please select a quality first');
                            }}
                            class="w-full py-3 bg-teal-500 hover:bg-teal-600 text-white font-bold rounded-lg shadow-md transition-all">
                            PROCESS CUSTOM VIDEO
                        </button>
                     </div>
                  {/if}
              </div>
          </div>
      </div>
  </div>
</div>

<!-- Download Popup Modal -->
{#if downloading}
<div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 backdrop-blur-sm animate-in fade-in duration-200">
    <div class="bg-white rounded-2xl shadow-2xl p-8 max-w-sm w-full text-center transform scale-100 animate-in zoom-in-95 duration-200">
        <div class="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">{statusText}</h3>
        
        {#if !downloadReady}
            <p class="text-gray-500 mb-6 font-mono text-sm">Please wait while we prepare your file.</p>
            <!-- Progress Bar -->
            <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden relative">
                 <div 
                    class="h-full bg-blue-600 rounded-full transition-all duration-300 ease-out flex items-center justify-center text-[10px] text-white font-bold"
                    style="width: {progress}%"
                >
                    {progress > 5 ? Math.round(progress) + '%' : ''}
                </div>
            </div>
        {:else}
             <p class="text-gray-500 mb-6 font-mono text-sm">File is ready for download!</p>
             <button 
                on:click={triggerFileSave}
                class="w-full py-3 bg-green-500 hover:bg-green-600 text-white font-bold rounded-lg shadow-md animate-bounce"
            >
                SAVE VIDEO
            </button>
        {/if}
    </div>
</div>
{/if}

<style>
  @keyframes progress {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
  }
</style>
{/if}
