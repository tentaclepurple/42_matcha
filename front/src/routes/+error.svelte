<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';

	import { page } from '$app/stores';
</script>

<PageWrapper>
	<h1>{$page.status}</h1>
	{#if $page.error?.message}
		<p>{$page.error?.message}</p>
	{:else}
		<p>An error occurred. Please try again later.</p>
	{/if}
</PageWrapper>
