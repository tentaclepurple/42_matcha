<script>
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import Conversations from './Conversations.svelte';

	const { children } = $props();
	const { conversations } = $page.data;
</script>

<PageWrapper>
	<h1>Messages</h1>
	<div class="flex items-stretch gap-8">
		<div class="w-full min-w-[200px] max-w-[300px] rounded-md bg-teal-200 p-3">
			<h2 class="sr-only mb-4">List of chats</h2>
			<Conversations {conversations} />
		</div>

		{@render children()}
	</div>
</PageWrapper>
