<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
</script>

<PageWrapper>
	<h1>Huzzah!</h1>
	<p>Your e-mail has been verified. You can now log in.</p>
	<Button type="button" level="primary" onclick={() => goto('/login')}>Go to login</Button>
</PageWrapper>
