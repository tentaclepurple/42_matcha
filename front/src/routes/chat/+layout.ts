import { error } from '@sveltejs/kit';
import type { PageLoad } from '../account/$types';
import { conversations } from '$lib/state/conversations.svelte';
import type Conversation from '$lib/interfaces/conversation.interface';

export const ssr = false;

export const load: PageLoad = async (): Promise<{ conversations: Conversation[] }> => {
	try {
		await conversations.fetch();

		if (!conversations.value) {
			error(500, 'Failed to fetch conversations');
		}

		return {
			conversations: conversations.value
		};
	} catch {
		error(500, 'Failed to fetch conversations');
	}
};
