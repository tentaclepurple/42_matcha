<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { writable } from 'svelte/store';

	let error = writable('');
	let isLoading = false;

	const handleReset = async (e) => {
		e.preventDefault();

		isLoading = true;
		error.set('');

		const formData = new FormData(e.target);
		const email = formData.get('email');

		const res = await fetch(`${SERVER_BASE_URL}/api/users/forgot_password`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email: email?.toString().toLowerCase() })
		});

		if (!res) {
			error.set('An error occurred. Please try again later.');
			isLoading = false;
			return;
		}

		goto('/forget-password/confirm', { replaceState: true });
	};
</script>

<PageWrapper>
	<h1 class="mb-4">Forgot your password?</h1>
	<p class="mb-4">We'll send you an e-mail to reset your password.</p>
	<form onsubmit={handleReset}>
		<fieldset class="mb-4 flex flex-col items-start">
			<label class="mb-4">
				E-mail
				<input
					type="email"
					id="email"
					name="email"
					value="chiamatemi.Nico@gmail.com"
					required
					autocomplete="email"
				/>
			</label>

			<Button level="primary" type="submit" {isLoading}>Reset password</Button>
		</fieldset>
	</form>

	{#if $error}
		<p style="text-red-500">{$error}</p>
	{/if}
</PageWrapper>
