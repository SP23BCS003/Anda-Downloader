<script lang="ts">
  import { onMount } from 'svelte';
  import { API_BASE_URL } from '$lib/api';

  let settings: Record<string, any> = {};
  let isLoading = true;
  let isSaving = false;
  let saveMessage = '';
  
  // Profile state
  let profile = {
    username: '',
    password: '',
    current_password: ''
  };
  let isSavingProfile = false;
  let profileMessage = '';
  let profileError = '';

  // Cache state
  let isClearingCache = false;
  let cacheMessage = '';

  const settingsConfig = [
    { key: 'site_name', label: 'Site Name', type: 'string', placeholder: 'Anda-Downloader' },
    { key: 'site_tagline', label: 'Site Tagline', type: 'string', placeholder: 'Download videos from any platform' },
    { key: 'contact_email', label: 'Contact Email', type: 'string', placeholder: 'contact@example.com' },
    { key: 'default_language', label: 'Default Language', type: 'string', placeholder: 'en' },
    { key: 'maintenance_mode', label: 'Maintenance Mode', type: 'bool', placeholder: 'false' },
    { key: 'analytics_id', label: 'Google Analytics ID', type: 'string', placeholder: 'G-XXXXXXXXXX' },
    { key: 'favicon_url', label: 'Favicon URL', type: 'string', placeholder: '/favicon.ico or https://...' },
    { key: 'admin_panel_url', label: 'Admin Panel Path (Visual Only)', type: 'string', placeholder: '/admin' },
    { key: 'verification_tags', label: 'Verification Meta Tags', type: 'textarea', placeholder: '<meta name="google-site-verification" content="..." />' },
    { key: 'robots_txt', label: 'Robots.txt Content', type: 'textarea', placeholder: 'User-agent: *\nAllow: /' },
  ];

  onMount(async () => {
    await fetchSettings();
  });

  async function fetchSettings() {
    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/settings`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        const data = await res.json();
        settings = Object.fromEntries(
          Object.entries(data).map(([key, val]: [string, any]) => [key, val.value])
        );
        // Defaults
        settings.robots_txt = settings.robots_txt || 'User-agent: *\nAllow: /';
      }
    } catch (e) {
      console.error('Failed to fetch settings:', e);
    } finally {
      isLoading = false;
    }
  }

  async function saveSettings() {
    isSaving = true;
    saveMessage = '';

    try {
      const token = localStorage.getItem('admin_token');
      const payload = settingsConfig.map(config => ({
        key: config.key,
        value: settings[config.key] || '',
        type: config.type === 'textarea' ? 'string' : config.type,
        description: config.label
      }));

      const res = await fetch(`${API_BASE_URL}/admin/settings`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        saveMessage = 'Settings saved successfully! ✓';
        setTimeout(() => saveMessage = '', 3000);
      } else {
        throw new Error('Failed to save settings');
      }
    } catch (e: any) {
      saveMessage = `Error: ${e.message}`;
    } finally {
      isSaving = false;
    }
  }

  async function updateProfile() {
    if (!profile.current_password) {
      profileError = 'Current password is required';
      return;
    }
    
    isSavingProfile = true;
    profileMessage = '';
    profileError = '';

    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
           username: profile.username || undefined,
           password: profile.password || undefined,
           current_password: profile.current_password
        })
      });

      const data = await res.json();
      
      if (res.ok) {
        profileMessage = 'Profile updated! You may need to login again.';
        profile.current_password = '';
        profile.password = '';
      } else {
        profileError = data.detail || 'Failed to update profile';
      }
    } catch (e: any) {
      profileError = `Error: ${e.message}`;
    } finally {
      isSavingProfile = false;
    }
  }

  async function clearCache() {
    if (!confirm('Are you sure you want to clear all caches? This includes temporary files.')) return;
    
    isClearingCache = true;
    cacheMessage = '';

    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/cache/clear`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      const data = await res.json();
      if (res.ok) {
        cacheMessage = data.message;
      } else {
        cacheMessage = 'Failed to clear cache';
      }
    } catch (e: any) {
      cacheMessage = `Error: ${e.message}`;
    } finally {
      isClearingCache = false;
    }
  }
</script>

<div class="p-8 pb-20">
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-slate-800 mb-2">Settings</h1>
    <p class="text-slate-600">Configure system parameters and admin account.</p>
  </div>

  {#if isLoading}
    <div class="flex items-center justify-center py-20">
      <svg class="animate-spin h-8 w-8 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  {:else}
    <div class="space-y-8">
      <!-- General Settings -->
      <section class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 class="text-xl font-semibold text-slate-800 mb-6">General Configuration</h2>
        <div class="space-y-6">
          {#each settingsConfig as config}
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">{config.label}</label>
              {#if config.type === 'bool'}
                <select
                  bind:value={settings[config.key]}
                  class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
                >
                  <option value="false">Disabled</option>
                  <option value="true">Enabled</option>
                </select>
              {:else if config.type === 'textarea'}
                <textarea
                  bind:value={settings[config.key]}
                  placeholder={config.placeholder}
                  rows="4"
                  class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none font-mono text-sm"
                ></textarea>
              {:else}
                <input
                  type="text"
                  bind:value={settings[config.key]}
                  placeholder={config.placeholder}
                  class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
                />
              {/if}
              {#if config.key === 'admin_panel_url'}
                <p class="text-xs text-slate-500 mt-1">Note: This only stores the value. You must verify your server configuration if changing the actual route path.</p>
              {/if}
            </div>
          {/each}

          {#if saveMessage}
            <div class="{saveMessage.includes('Error') ? 'bg-red-50 text-red-700 border-red-200' : 'bg-green-50 text-green-700 border-green-200'} border px-4 py-3 rounded-lg text-sm transition-all">
              {saveMessage}
            </div>
          {/if}

          <div class="pt-4 border-t border-slate-200">
            <button
              on:click={saveSettings}
              disabled={isSaving}
              class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition disabled:opacity-70"
            >
              {isSaving ? 'Saving...' : 'Save Configuration'}
            </button>
          </div>
        </div>
      </section>

      <!-- Admin Profile -->
      <section class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 class="text-xl font-semibold text-slate-800 mb-6">Admin Account</h2>
        <div class="space-y-6 max-w-xl">
           <div>
             <label class="block text-sm font-medium text-slate-700 mb-2">New Username (Optional)</label>
             <input type="text" bind:value={profile.username} class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none" autocomplete="off" />
           </div>
           <div>
             <label class="block text-sm font-medium text-slate-700 mb-2">New Password (Optional)</label>
             <input type="password" bind:value={profile.password} class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none" autocomplete="new-password" />
           </div>
           <div class="pt-4">
             <label class="block text-sm font-medium text-slate-700 mb-2">Current Password (Required)</label>
             <input type="password" bind:value={profile.current_password} class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none" autocomplete="current-password" />
           </div>

           {#if profileMessage}
             <div class="bg-green-50 text-green-700 border border-green-200 px-4 py-3 rounded-lg text-sm">{profileMessage}</div>
           {/if}
           {#if profileError}
             <div class="bg-red-50 text-red-700 border border-red-200 px-4 py-3 rounded-lg text-sm">{profileError}</div>
           {/if}

           <div class="pt-2">
            <button
              on:click={updateProfile}
              disabled={isSavingProfile}
              class="px-6 py-3 bg-slate-800 hover:bg-slate-900 text-white font-semibold rounded-lg transition disabled:opacity-70"
            >
              {isSavingProfile ? 'Updating...' : 'Update Credentials'}
            </button>
          </div>
        </div>
      </section>
      
      <!-- System Actions -->
      <section class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 class="text-xl font-semibold text-slate-800 mb-6">System Operations</h2>
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <button
              on:click={clearCache}
              disabled={isClearingCache}
              class="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-lg transition disabled:opacity-70 flex items-center gap-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              {isClearingCache ? 'Clearing...' : 'Clear All Caches'}
            </button>
            
            {#if cacheMessage}
              <span class="text-sm font-medium text-slate-600">{cacheMessage}</span>
            {/if}
        </div>
        <p class="text-sm text-slate-500 mt-2">Removes temporary downloads, generated files, and system cache.</p>
      </section>
    </div>
  {/if}
</div>
