import type { PageLoad } from './$types';
import { SERVER_BASE_URL } from '$lib/constants/api';
import deserialize from '$lib/utils/deserialize';
import { redirect } from '@sveltejs/kit';

export const ssr = false;

export const load: PageLoad = async ({ fetch, params }) => {
	const username = params.username;

	const token = localStorage.getItem('access_token');

	const res = await fetch(`${SERVER_BASE_URL}/api/chat/messages/${username}`, {
		headers: {
			Authorization: `Bearer ${token}`,
			'Content-Type': 'application/json'
		}
	});

	if (!res.ok) {
		console.error('Failed to fetch conversations');
		redirect(302, '/chat');
	}

	const { messages } = await res.json();

	const sortedMessages = deserialize(messages).sort((a, b) => {
		const aDate = new Date(a.createdAt);
		const bDate = new Date(b.createdAt);

		return aDate.getTime() - bDate.getTime();
	});

	return {
		messages: sortedMessages
	};
};
