<script lang="ts">
    export let data;
</script>

<div class="p-10 font-mono text-sm">
    <h1 class="text-2xl font-bold mb-6">System Diagnostics</h1>

    <section class="mb-8">
        <h2 class="text-xl font-bold mb-2">Environment</h2>
        <pre class="bg-gray-100 p-4 rounded">{JSON.stringify(data.env, null, 2)}</pre>
    </section>

    <section class="mb-8">
        <h2 class="text-xl font-bold mb-2">API Connectivity</h2>
        <div class="p-4 rounded {data.connectivity.status.includes('200') ? 'bg-green-100' : 'bg-red-100'}">
            <p><strong>Target:</strong> {data.connectivity.target}</p>
            <p><strong>Status:</strong> {data.connectivity.status}</p>
            {#if data.connectivity.error}
                <p class="text-red-700 mt-2"><strong>Error:</strong> {data.connectivity.error}</p>
            {/if}
        </div>
    </section>

    <section>
        <h2 class="text-xl font-bold mb-2">Fetched Settings</h2>
        {#if data.settings}
            <pre class="bg-gray-100 p-4 rounded">{JSON.stringify(data.settings, null, 2)}</pre>
        {:else}
            <p class="text-gray-500 italic">No settings fetched.</p>
        {/if}
    </section>
</div>
