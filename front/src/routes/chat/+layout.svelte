<script>
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
    const {children} = $props();

    const {conversations} = $page.data;
</script>

<PageWrapper>
	<h1>Chat</h1>
    <h2>List of chats</h2>
    <ul>
        {#each conversations as conversation}
        {$inspect(conversation)}
            <li>{conversation}</li>
        {/each}
    </ul>
    {@render children()}
</PageWrapper>