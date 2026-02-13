import type { ServerLoadEvent } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

export async function load({ fetch }: ServerLoadEvent) {
    const apiUrl = env.PUBLIC_API_URL || 'http://localhost:8000';
    try {
        const [settingsRes, seoRes] = await Promise.all([
            fetch(`${apiUrl}/api/public-settings`),
            fetch(`${apiUrl}/api/public-seo`)
        ]);

        const settings = settingsRes.ok ? await settingsRes.json() : {};
        const seo = seoRes.ok ? await seoRes.json() : {};

        return {
            settings,
            seo
        };
    } catch (e) {
        console.error('Failed to load public data:', e);
    }
    return {
        settings: {},
        seo: {}
    };
};
