<script>
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';

	const { username } = $page.params;
</script>

<PageWrapper>
	<a href="/chat">Back to messages</a>
	<h1>Conversation with {username}</h1>
</PageWrapper>
