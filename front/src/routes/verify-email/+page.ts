import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
	const params: URLSearchParams = url.searchParams;
	const token: string | null = params.get('token');

	if (!token) {
		throw redirect(302, '/');
	}

	const res = await fetch(`http://backend:5000/api/users/verify/${token}`, {
		method: 'GET'
	});
	if (!res.ok) {
		throw redirect(302, `/error?error=invalid-verification-link`);
	}

	throw redirect(302, '/verify-email/success');
};
