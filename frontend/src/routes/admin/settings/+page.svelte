<script lang="ts">
  import { onMount } from 'svelte';

  let settings: Record<string, any> = {};
  let isLoading = true;
  let isSaving = false;
  let saveMessage = '';

  const settingsConfig = [
    { key: 'site_name', label: 'Site Name', type: 'string', placeholder: 'Anda-Downloader' },
    { key: 'site_tagline', label: 'Site Tagline', type: 'string', placeholder: 'Download videos from any platform' },
    { key: 'contact_email', label: 'Contact Email', type: 'string', placeholder: 'contact@example.com' },
    { key: 'default_language', label: 'Default Language', type: 'string', placeholder: 'en' },
    { key: 'maintenance_mode', label: 'Maintenance Mode', type: 'bool', placeholder: 'false' },
    { key: 'analytics_id', label: 'Google Analytics ID', type: 'string', placeholder: 'G-XXXXXXXXXX' },
  ];

  onMount(async () => {
    await fetchSettings();
  });

  async function fetchSettings() {
    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch('http://localhost:8000/admin/settings', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        const data = await res.json();
        settings = Object.fromEntries(
          Object.entries(data).map(([key, val]: [string, any]) => [key, val.value])
        );
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
        type: config.type,
        description: config.label
      }));

      const res = await fetch('http://localhost:8000/admin/settings', {
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
</script>

<div class="p-8">
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-slate-800 mb-2">General Settings</h1>
    <p class="text-slate-600">Configure your site settings and preferences</p>
  </div>

  {#if isLoading}
    <div class="flex items-center justify-center py-20">
      <svg class="animate-spin h-8 w-8 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  {:else}
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
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
            {:else}
              <input
                type="text"
                bind:value={settings[config.key]}
                placeholder={config.placeholder}
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
              />
            {/if}
          </div>
        {/each}

        {#if saveMessage}
          <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
            {saveMessage}
          </div>
        {/if}

        <div class="pt-4 border-t border-slate-200">
          <button
            on:click={saveSettings}
            disabled={isSaving}
            class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition disabled:opacity-70"
          >
            {isSaving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </div>
    </div>
  {/if}
</div>
