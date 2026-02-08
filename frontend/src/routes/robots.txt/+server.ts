import type { RequestEvent } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

export async function GET({ fetch }: RequestEvent) {
    const apiUrl = env.PUBLIC_API_URL || 'http://localhost:8000';
    try {
        const res = await fetch(`${apiUrl}/api/public-settings`);
        let content = 'User-agent: *\nAllow: /';

        if (res.ok) {
            const data = await res.json();
            if (data.robots_txt) {
                content = data.robots_txt;
            }
        }

        return new Response(content, {
            headers: {
                'Content-Type': 'text/plain',
                'Cache-Control': 'max-age=3600'
            }
        });
    } catch (e) {
        return new Response('User-agent: *\nAllow: /', {
            headers: { 'Content-Type': 'text/plain' }
        });
    }
};
