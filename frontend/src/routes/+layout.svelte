<script lang="ts">
  import "../app.css";
  export let data;
  
  $: settings = data.settings || {};
</script>

<svelte:head>
  {#if settings.favicon_url}
    <link rel="icon" href={settings.favicon_url} />
  {/if}
  
  {#if settings.verification_tags}
    {@html settings.verification_tags}
  {/if}
  
  {#if settings.site_name}
    <meta name="application-name" content={settings.site_name} />
  {/if}
</svelte:head>

<slot />
