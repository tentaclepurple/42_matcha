<script lang="ts">
	import { goto } from '$app/navigation';
	import { NOTIFICATIONS_TYPES } from '$lib/constants/notifications';
	import { notificationsData } from '$lib/state/notifications.svelte';
	import CoreWidget from './CoreWidget.svelte';

	const messagesNotifications = $derived(
		notificationsData.value
			? notificationsData.value.notifications.filter((notification) => {
					return notification.type === NOTIFICATIONS_TYPES.MESSAGE;
				})
			: []
	);
</script>

<CoreWidget
	count={messagesNotifications.length}
	icon="/matcha/icons/notifications/envelope.svg"
	onClick={() => goto('/matcha/chat')}
/>
