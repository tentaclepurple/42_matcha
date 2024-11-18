<script lang="ts">
	import Button from '$lib/components/Button.svelte';

	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
</script>

<PageWrapper>
	<h1 class="mb-2">You're almost there!</h1>
	<p>We sent you an e-mail. Confirm your e-mail address and you'll be able to log in.</p>

	<Button
		type="button"
		level="primary"
		class="mt-4"
		onclick={() => {
			goto('/login');
		}}
	>
		Go to log in
	</Button>
</PageWrapper>
