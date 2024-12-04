<script lang="ts">
	import NewMessageForm from './NewMessageForm.svelte';

	import { page } from '$app/stores';
	import { messagesData } from '$lib/state/messages.svelte';
	import { onDestroy } from 'svelte';
	import { POLLING_INTERVAL } from '$lib/constants/polling';
	import MessagesList from './MessagesList.svelte';
	import ChatHeader from './ChatHeader.svelte';

	let username = $state($page.params.username);
	$effect(() => {
		username = $page.params.username;
	});

	const { otherUser } = $page.data;

	const interval = setInterval(() => {
		messagesData.fetchMessages({ username });
	}, POLLING_INTERVAL);

	onDestroy(() => {
		clearInterval(interval);
	});
</script>

<div class="w-full">
	<ChatHeader username={otherUser.username} profilePhoto={otherUser.profilePhoto} />
	<MessagesList />
	<NewMessageForm {username} />
</div>
