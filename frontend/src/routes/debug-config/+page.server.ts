import { env } from '$env/dynamic/public';
import { env as privateEnv } from '$env/dynamic/private';

export async function load({ fetch }) {
    const apiUrl = env.PUBLIC_API_URL || 'http://localhost:8000';
    let apiStatus = 'unknown';
    let apiError = '';
    let settings = null;

    try {
        const start = Date.now();
        const res = await fetch(`${apiUrl}/api/public-settings`);
        const duration = Date.now() - start;

        apiStatus = `HTTP ${res.status} (${duration}ms)`;
        if (res.ok) {
            settings = await res.json();
        } else {
            apiError = await res.text();
        }
    } catch (e: any) {
        apiStatus = 'failed';
        apiError = e.message;
    }

    return {
        env: {
            PUBLIC_API_URL: apiUrl,
            NODE_ENV: privateEnv.NODE_ENV,
            // Don't expose sensitive keys
        },
        connectivity: {
            status: apiStatus,
            error: apiError,
            target: `${apiUrl}/api/public-settings`
        },
        settings
    };
}
