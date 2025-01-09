import type Conversation from '$lib/interfaces/conversation.interface';
import { SERVER_BASE_URL } from '$lib/constants/api';
import deserialize from '$lib/utils/deserialize';

class ConversationsClass {
	#value = $state<null | Conversation[]>(null);

	get value(): null | Conversation[] {
		return this.#value;
	}

	set value(value: null | Conversation[]) {
		this.#value = value;
	}

	fetch = async (): Promise<void> => {
		try {
			const token = localStorage.getItem('access_token');

			const res = await fetch(`${SERVER_BASE_URL}/api/chat/conversations`, {
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (!res.ok) {
				throw new Error('Failed to fetch conversations');
			}

			const { conversations } = await res.json();

			const sortedConversations = deserialize(conversations).toSorted((a, b) => {
				const aUsername = a.user.username.toLowerCase();
				const bUsername = b.user.username.toLowerCase();

				return aUsername.localeCompare(bUsername);
			});

			this.#value = sortedConversations;
		} catch (error: unknown) {
			console.error(error);
			throw new Error('Failed to fetch conversations');
		}
	};
}

export const conversations = new ConversationsClass();
