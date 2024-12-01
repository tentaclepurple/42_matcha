import { SERVER_BASE_URL } from '$lib/constants/api';
import { error } from '@sveltejs/kit';
import deserialize from '$lib/utils/deserialize';
import type { PageLoad } from '../account/$types';

export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {
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

	const sortedConversations = deserialize(conversations).sort((a, b) => {
		const aUsername = a.user.username.toLowerCase();
		const bUsername = b.user.username.toLowerCase();

		return aUsername.localeCompare(bUsername);
	});

	return {
		conversations: sortedConversations
	};
};
