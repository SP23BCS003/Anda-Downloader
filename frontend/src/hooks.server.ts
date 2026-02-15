import type { Handle } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

// Cache the admin path setting
let cachedAdminPath: string | null = null;
let cacheTimestamp = 0;
const CACHE_TTL = 60_000; // 60 seconds

async function getAdminPath(): Promise<string> {
    const now = Date.now();
    if (cachedAdminPath !== null && (now - cacheTimestamp) < CACHE_TTL) {
        return cachedAdminPath;
    }

    try {
        const apiUrl = env.PUBLIC_API_URL || 'http://localhost:8000';
        const res = await fetch(`${apiUrl}/api/public-settings`);
        if (res.ok) {
            const settings = await res.json();
            // Normalize: ensure starts with /, remove trailing slash
            let path = settings.admin_panel_url || '/admin';
            if (!path.startsWith('/')) path = '/' + path;
            path = path.replace(/\/+$/, ''); // remove trailing slashes

            console.log('[hooks] Fetched admin path:', path); // DEBUG
            cachedAdminPath = path;
            cacheTimestamp = now;
            return path;
        } else {
            console.error(`[hooks] Failed to fetch settings. Status: ${res.status} URL: ${apiUrl}/api/public-settings`);
        }
    } catch (e) {
        console.error('[hooks] Critical error fetching admin path:', e);
    }

    return cachedAdminPath || '/admin';
}

export const handle: Handle = async ({ event, resolve }) => {
    const pathname = event.url.pathname;
    const adminPath = await getAdminPath();

    // Normalize adminPath for comparison
    const isDefaultAdmin = adminPath === '/admin';

    // Case 1: User visits the CUSTOM admin path (e.g. /admin/anda/dashboard)
    // Rewrite to internal /admin/* route
    if (!isDefaultAdmin && pathname.startsWith(adminPath)) {
        // Get the sub-path after the custom prefix
        const subPath = pathname.slice(adminPath.length) || '';
        const internalPath = '/admin' + subPath;

        // Rewrite the URL to the internal admin route
        const newUrl = new URL(event.url);
        newUrl.pathname = internalPath;

        // Create a new request with the rewritten URL
        const newEvent = { ...event, url: newUrl };
        // Update route to match internal path
        Object.defineProperty(newEvent, 'url', { value: newUrl });

        return resolve(newEvent);
    }

    // Case 2: User visits /admin/* directly but custom path is set
    // Block access (return 404)
    if (!isDefaultAdmin && pathname.startsWith('/admin')) {
        return new Response('Not Found', { status: 404 });
    }

    // Case 3: Default admin path (/admin) or non-admin route
    return resolve(event);
};
