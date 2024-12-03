<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
</script>

<PageWrapper>
	<h1 class="mb-4">Huzzah!</h1>
	<p class="mb-6">Your e-mail has been verified. You can now log in.</p>
	<Button type="button" level="primary" onclick={() => goto('/login')} class="w-fit">
		Go to login
	</Button>
</PageWrapper>
