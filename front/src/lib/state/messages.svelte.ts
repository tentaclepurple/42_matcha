import { SERVER_BASE_URL } from '$lib/constants/api';
import type Messages from '$lib/interfaces/messages.interface';
import deserialize from '$lib/utils/deserialize';

class MessagesClass {
	#value = $state<Messages | null>(null);

	get value(): Messages | null {
		return this.#value;
	}

	set value(newValue: Messages | null) {
		this.#value = newValue;
	}

	fetchMessages = async ({ username }: { username: string }): Promise<void> => {
		try {
			const token = localStorage.getItem('access_token');

			const res = await fetch(`${SERVER_BASE_URL}/api/chat/messages/${username}`, {
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				throw new Error('Failed to fetch messages');
			}

			const { messages, other_user: otherUser } = await res.json();

			const sortedMessages = deserialize(messages).sort((a, b) => {
				const aDate = new Date(a.createdAt);
				const bDate = new Date(b.createdAt);

				return aDate.getTime() - bDate.getTime();
			});

			if (
				this.#value?.messages.length === sortedMessages.length &&
				this.#value?.otherUser.userId === otherUser.userId
			) {
				return;
			}

			this.#value = {
				messages: sortedMessages,
				otherUser: deserialize(otherUser)
			};
		} catch (e) {
			throw new Error(e);
		}
	};
}

export const messagesData: MessagesClass = new MessagesClass();
