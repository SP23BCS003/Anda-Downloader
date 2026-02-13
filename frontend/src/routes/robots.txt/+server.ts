import type { RequestEvent } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

export async function GET({ fetch }: RequestEvent) {
    // Default to localhost, but prefer env var if set
    const apiUrl = env.PUBLIC_API_URL || 'http://localhost:8000';

    // Default safe content
    const defaultRobots = 'User-agent: *\nAllow: /';

    try {
        const res = await fetch(`${apiUrl}/api/public-settings`);

        if (res.ok) {
            const data = await res.json();
            if (data.robots_txt) {
                return new Response(data.robots_txt, {
                    headers: {
                        'Content-Type': 'text/plain',
                        'Cache-Control': 'max-age=3600'
                    }
                });
            }
        }
    } catch (e) {
        console.error('Failed to fetch robots.txt settings:', e);
        // Fallback to default
    }

    return new Response(defaultRobots, {
        headers: {
            'Content-Type': 'text/plain',
            'Cache-Control': 'max-age=3600'
        }
    });
};
