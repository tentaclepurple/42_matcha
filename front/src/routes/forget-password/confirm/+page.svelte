<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import Button from '$lib/components/Button.svelte';
	import { goto } from '$app/navigation';
</script>

<PageWrapper>
	<h1 class="mb-4">Your new password is on the way!</h1>
	<div>
		<p class="mb-6">
			If you have a Matcha account, you'll receive an e-mail with instructions on how to set a new
			password.
		</p>
		<Button
			level="primary"
			type="button"
			onclick={() => {
				goto('/matcha/login', { replaceState: true });
			}}
		>
			Back to login
		</Button>
	</div>
</PageWrapper>
