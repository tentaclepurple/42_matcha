import type { PageLoad } from './$types';
import { messagesData } from '$lib/state/messages.svelte';
import { redirect } from '@sveltejs/kit';

export const ssr = false;

export const load: PageLoad = async ({ params }) => {
	const username = params.username;

	try {
		await messagesData.fetchMessages({ username });

		return {
			messages: messagesData.value?.messages ?? [],
			otherUser: messagesData.value?.otherUser ?? null
		};
	} catch (e) {
		console.error(e);
		redirect(302, '/chat');
	}
};
