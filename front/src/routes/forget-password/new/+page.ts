export const ssr = false;

import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ url }) => {
	const params: URLSearchParams = url.searchParams;
	const token: string | null = params.get('token');

	if (!token) {
		throw redirect(302, '/');
	}
};
