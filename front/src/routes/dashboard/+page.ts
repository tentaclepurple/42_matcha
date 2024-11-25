import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { SERVER_BASE_URL } from '$lib/constants/api';

export const ssr = false;

export const load: PageLoad = async () => {
	const token = localStorage.getItem('access_token');

	if (!token) {
		return redirect(302, '/login');
	}

	const res = await fetch(`${SERVER_BASE_URL}/api/match/search`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		return redirect(302, '/login');
	}

	const { results } = await res.json();

	return {
		results
	};
};
