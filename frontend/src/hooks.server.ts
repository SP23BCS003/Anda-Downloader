import type { Handle } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

// Hardcoded admin path
const adminPath = '/khan';

export const handle: Handle = async ({ event, resolve }) => {
    const pathname = event.url.pathname;
    // const adminPath = await getAdminPath(); // REMOVED DYNAMIC FETCH

    // Normalize adminPath for comparison
    const isDefaultAdmin = adminPath === '/admin';

    // DEBUG LOG
    if (pathname.startsWith('/admin') || pathname.startsWith(adminPath)) {
        console.log(`[hooks] Request: ${pathname}, AdminPath: ${adminPath}, IsDefault: ${isDefaultAdmin}`);
    }

    // Case 1: User visits the CUSTOM admin path (e.g. /admin/anda/dashboard)
    // Rewrite to internal /admin/* route
    if (!isDefaultAdmin && pathname.startsWith(adminPath)) {
        // Get the sub-path after the custom prefix
        const subPath = pathname.slice(adminPath.length) || '';
        const internalPath = '/admin' + subPath;

        console.log(`[hooks] Rewriting ${pathname} -> ${internalPath}`);

        // Rewrite the URL to the internal admin route
        const newUrl = new URL(event.url);
        newUrl.pathname = internalPath;

        console.log(`[hooks] Rewriting ${pathname} -> ${internalPath}`);

        // Update route to match internal path on the ORIGINAL event object
        Object.defineProperty(event, 'url', { value: newUrl });

        // Also update the request object, as SvelteKit/Vite might use it for routing/matching
        const newRequest = new Request(newUrl.toString(), event.request);
        Object.defineProperty(event, 'request', { value: newRequest });

        return resolve(event);
    }

    // Case 2: User visits /admin/* directly but custom path is set
    // Block access (return 404)
    if (!isDefaultAdmin && pathname.startsWith('/admin')) {
        return new Response('Not Found', { status: 404 });
    }

    // Case 3: Default admin path (/admin) or non-admin route
    return resolve(event);
};
