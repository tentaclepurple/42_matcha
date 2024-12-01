<script>
	import NewMessageForm from './NewMessageForm.svelte';

	import { page } from '$app/stores';
	import { messagesData } from '$lib/state/messages.svelte';
	import { onDestroy } from 'svelte';
	import { POLLING_INTERVAL } from '$lib/constants/polling';
	import MessagesList from './MessagesList.svelte';

	let username = $state($page.params.username);
	$effect(() => {
		username = $page.params.username;
	});

	const interval = setInterval(() => {
		messagesData.fetchMessages({ username });
	}, POLLING_INTERVAL);

	onDestroy(() => {
		clearInterval(interval);
	});
</script>

<div class="w-full">
	<h2 class="mb-4">{username}</h2>
	<MessagesList />
	<NewMessageForm {username} />
</div>
