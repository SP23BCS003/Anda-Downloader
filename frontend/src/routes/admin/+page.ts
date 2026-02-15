import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
    // Redirect root admin accesses to login
    // The hook rewrites /khan -> /admin, so this handles /khan hits
    throw redirect(302, '/khan/login');
};
