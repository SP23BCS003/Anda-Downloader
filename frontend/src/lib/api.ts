/**
 * API Configuration
 * Centralized API endpoint configuration for the frontend
 */

// Get API URL from environment variable or fallback to localhost for development
// VITE_API_URL works on client-side, PUBLIC_API_URL works on both client and server
export const API_BASE_URL = import.meta.env.VITE_API_URL || import.meta.env.PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Helper function to build API endpoints
 * @param path - The API path (e.g., '/info', '/start_download')
 * @returns Full API URL
 */
export function apiUrl(path: string): string {
    // Ensure path starts with /
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;
    return `${API_BASE_URL}${normalizedPath}`;
}

/**
 * Common fetch wrapper with error handling
 */
export async function apiFetch<T>(
    path: string,
    options: RequestInit = {}
): Promise<T> {
    const url = apiUrl(path);
    const response = await fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || response.statusText);
    }

    return response.json();
}
