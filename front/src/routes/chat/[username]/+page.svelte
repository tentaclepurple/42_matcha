<script>
	import NewMessageForm from './NewMessageForm.svelte';

	import { page } from '$app/stores';
	import PastMessages from './PastMessages.svelte';

	let username = $state($page.params.username);
	$effect(() => {
		username = $page.params.username;
	});

	const messages = $page.data.messages;
</script>

<div class="w-full">
	<h2 class="mb-6">{username}</h2>
	<PastMessages {messages} />
	<NewMessageForm {username} />
</div>
