import { SERVER_BASE_URL } from '$lib/constants/api';
import type Message from '$lib/interfaces/message.interface';
import deserialize from '$lib/utils/deserialize';

class MessagesClass {
	#value = $state<Message[]>([]);

	get value(): Message[] {
		return this.#value;
	}

	set value(newValue: Message[]) {
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

			const { messages } = await res.json();

			const sortedMessages = deserialize(messages).sort((a, b) => {
				const aDate = new Date(a.createdAt);
				const bDate = new Date(b.createdAt);

				return aDate.getTime() - bDate.getTime();
			});

			if (JSON.stringify(this.#value) === JSON.stringify(sortedMessages)) {
				return;
			}

			this.#value = sortedMessages;
		} catch (e) {
			throw new Error(e);
		}
	};
}

export const messagesData: MessagesClass = new MessagesClass();
