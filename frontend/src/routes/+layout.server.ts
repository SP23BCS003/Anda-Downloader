import type { ServerLoadEvent } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

export async function load({ fetch }: ServerLoadEvent) {
    const apiUrl = env.PUBLIC_API_URL || 'http://localhost:8000';
    try {
        const res = await fetch(`${apiUrl}/api/public-settings`);
        if (res.ok) {
            const settings = await res.json();
            return {
                settings
            };
        }
    } catch (e) {
        console.error('Failed to load public settings:', e);
    }
    return {
        settings: {}
    };
};
