import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageLoad} */
export const load = async () => {
    // Redirect root admin accesses to login
    // The hook rewrites /khan -> /admin, so this handles /khan hits
    throw redirect(302, '/khan/login');
};
