import type { RequestEvent } from '@sveltejs/kit';

export async function GET({ fetch }: RequestEvent) {
    try {
        const res = await fetch('http://localhost:8000/api/public-settings');
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
