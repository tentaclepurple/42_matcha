<script lang="ts">
	import NewMessageForm from './NewMessageForm.svelte';

	import { page } from '$app/stores';
	import { messagesData } from '$lib/state/messages.svelte';
	import { onDestroy } from 'svelte';
	import { POLLING_INTERVAL } from '$lib/constants/polling';
	import MessagesList from './MessagesList.svelte';
	import ChatHeader from './ChatHeader.svelte';
	import type Conversation from '$lib/interfaces/conversation.interface';

	let username = $state($page.params.username);
	$effect(() => {
		username = $page.params.username;
	});

	const { conversations } = $page.data;

	const user = $derived<Conversation['user']>(
		conversations.find((conversation: Conversation) => conversation.user.username === username).user
	);

	const interval = setInterval(() => {
		messagesData.fetchMessages({ username });
	}, POLLING_INTERVAL);

	onDestroy(() => {
		clearInterval(interval);
	});
</script>

<div class="w-full">
	<ChatHeader username={user.username} profilePhoto={user.profilePhoto} />
	<MessagesList />
	<NewMessageForm {username} />
</div>
