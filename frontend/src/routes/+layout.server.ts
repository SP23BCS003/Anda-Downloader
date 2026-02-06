import type { ServerLoadEvent } from '@sveltejs/kit';

export async function load({ fetch }: ServerLoadEvent) {
    try {
        const res = await fetch('http://localhost:8000/api/public-settings');
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
