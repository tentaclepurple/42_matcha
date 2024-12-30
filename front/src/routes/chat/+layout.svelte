<script>
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import ConversationsList from './ConversationsList.svelte';

	const { children } = $props();
	const { conversations } = $page.data;
</script>

<PageWrapper>
	<h1 class="sr-only mb-4 sm:not-sr-only">Messages</h1>
	<div class="flex flex-1 flex-col items-stretch gap-2 sm:gap-8 sm:flex-row">
		<div class="w-full rounded-md bg-teal-100 p-3 sm:max-w-[225px]">
			<h2 class="sr-only mb-4">List of chats</h2>
			<ConversationsList {conversations} />
		</div>

		{@render children()}
	</div>
</PageWrapper>
