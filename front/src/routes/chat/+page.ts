import type { PageLoad } from './$types';
import { SERVER_BASE_URL } from '$lib/constants/api';
import { error } from '@sveltejs/kit';

export const ssr = false;

export const load: PageLoad = async () => {
	const token = localStorage.getItem('access_token');

	const res = await fetch(`${SERVER_BASE_URL}/api/chat/conversations`, {
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		error(500, 'Failed to fetch conversations');
	}

	const { conversations } = await res.json();

	return {
		conversations
	};
};
