<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import Button from '$lib/components/Button.svelte';
	import { goto } from '$app/navigation';
</script>

<PageWrapper>
	<h1 class="mb-4">Your new password is on the way!</h1>
	<div>
		<p class="mb-4">
			If you have an account with us, you'll receive an e-mail with instructions on how to set a new
			password.
		</p>
		<Button
			level="primary"
			type="button"
			onclick={() => {
				goto('/matcha/', { replaceState: true });
			}}
		>
			Back to home
		</Button>
	</div>
</PageWrapper>
