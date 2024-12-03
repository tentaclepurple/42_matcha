<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';

	import { page } from '$app/stores';

	const { status, error } = $page;
</script>

<PageWrapper>
	<h1>{status}</h1>
	{#if error?.message}
		<p>{error?.message}</p>
	{:else}
		<p>An error occurred. Please try again later.</p>
	{/if}
</PageWrapper>
