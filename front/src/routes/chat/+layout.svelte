<script>
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import ConversationsList from './ConversationsList.svelte';

	const { children } = $props();
	const { conversations } = $page.data;
</script>

<PageWrapper>
	<h1 class="sr-only">Messages</h1>
	<div class="flex flex-1 flex-col items-stretch gap-2 sm:flex-row sm:gap-8">
		<div class="w-full rounded-md bg-teal-100 p-3 sm:max-w-[225px] flex flex-col gap-4">
			<h2 class="sr-only sm:not-sr-only">List of chats</h2>
			<ConversationsList {conversations} />
		</div>

		{@render children()}
	</div>
</PageWrapper>
