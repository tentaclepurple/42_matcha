import { SERVER_BASE_URL } from '$lib/constants/api';
import type Notification from '$lib/interfaces/notification.interface';
import deserialize from '$lib/utils/deserialize';

interface NotificationsData {
	count: number;
	notifications: Notification[];
}

class NotificationsDataClass {
	#value = $state<NotificationsData | null>(null);

	get value(): NotificationsData | null {
		return this.#value;
	}

	set value(newValue: NotificationsData | null) {
		this.#value = newValue;
	}

	fetch = async () => {
		const token = localStorage.getItem('access_token');

		if (!token) {
			return;
		}

		const res = await fetch(`${SERVER_BASE_URL}/api/notifications/unread`, {
			headers: {
				Authorization: `Bearer ${token}`
			}
		});

		if (!res.ok) {
			console.error('Failed to fetch notifications');
			return;
		}

		const data = await res.json();
		console.log('Fetching notifications', deserialize(data));

		const deserializedData = deserialize(data);
		const sortedNotifications = deserializedData.notifications.sort(
			(a: Notification, b: Notification) => {
				return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
			}
		);

		const newValue = {
			...deserializedData,
			notifications: sortedNotifications
		};

		// check if newValue is different from this.#value, deep compare
		if (JSON.stringify(newValue) !== JSON.stringify(this.#value)) {
			this.#value = newValue;
		}
	};

	markAsRead = async (notificationId: string) => {
		if (!notificationId) {
			console.error('No notification ID provided');
			return;
		}

		const token = localStorage.getItem('access_token');

		if (!token) {
			return;
		}

		const res = await fetch(`${SERVER_BASE_URL}/api/notifications/mark_as_read/${notificationId}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		});

		if (!res.ok) {
			console.error('Failed to mark notification as read');
			return;
		}

		this.fetch();
	};
}

export const notificationsData = new NotificationsDataClass();
