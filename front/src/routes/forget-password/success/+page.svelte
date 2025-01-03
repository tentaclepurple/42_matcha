<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import Button from '$lib/components/Button.svelte';
	import { goto } from '$app/navigation';
</script>

<PageWrapper>
	<h1 class="mb-4">Welcome back!</h1>
	<div>
		<p class="mb-4">
			Your password has been successfully reset. You can now log in with your new password.
		</p>

		<Button
			type="button"
			level="primary"
			onclick={() => {
				goto('/matcha/login', { replaceState: true });
			}}
		>
			Go to login
		</Button>
	</div>
</PageWrapper>
