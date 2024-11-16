<script lang="ts">
	import Button from '$lib/components/Button.svelte';

	import { goto } from '$app/navigation';
</script>

<div>
	<h1 class="mb-2">Welcome on board!</h1>
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
</div>
