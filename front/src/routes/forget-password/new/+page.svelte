<script lang="ts">
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import PasswordInput from '$lib/components/PasswordInput.svelte';
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { goto } from '$app/navigation';

	let error = '';
	let loading = false;

	const handleSubmit = async (e) => {
		e.preventDefault();

		loading = true;
		error = '';

		const params = new URLSearchParams(window.location.search);
		const token = params.get('token');

		const formData = new FormData(e.target);
		const password = formData.get('password') as string;
		const confirm = formData.get('confirm') as string;

		if (password !== confirm) {
			error = 'Passwords do not match';
			loading = false;
			return;
		}

		const res = await fetch(`${SERVER_BASE_URL}/api/users/reset_password/${token}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				password
			})
		});

		if (!res) {
			error = 'An error occurred. Please try again later.';
			loading = false;
			return;
		}

		loading = false;
		goto('/forget-password/success', { replaceState: true });
	};
</script>

<PageWrapper>
	<h1 class="mb-4">Set your new password</h1>
	<p class="mb-4">You're one step away from getting a new password.</p>

	<form onsubmit={handleSubmit}>
		<fieldset class="mb-4">
			<label class="flex flex-col items-start justify-center">
				Password
				<PasswordInput
					id="password"
					name="password"
					value="Ciaociao1!"
					required
					autocomplete="new-password"
				/>
			</label>
			<label class="flex flex-col items-start justify-center">
				Confirm password
				<PasswordInput
					id="confirm"
					name="confirm"
					value="Ciaociao1!"
					required
					autocomplete="new-password"
				/>
			</label>
		</fieldset>
		{#if error}
			<p class="mb-4 text-red-500">{error}</p>
		{/if}

		<Button type="submit">Set new password</Button>
	</form>
</PageWrapper>
