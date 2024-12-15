<script>
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import ConversationsList from './ConversationsList.svelte';

	const { children } = $props();
	const { conversations } = $page.data;
</script>

<PageWrapper>
	<h1>Messages</h1>
	<div class="flex flex-1 items-stretch gap-8">
		<div class="w-full max-w-[225px] rounded-md bg-teal-100 p-3">
			<h2 class="sr-only mb-4">List of chats</h2>
			<ConversationsList {conversations} />
		</div>

		{@render children()}
	</div>
</PageWrapper>
