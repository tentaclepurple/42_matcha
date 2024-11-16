<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Form from '$lib/components/Form.svelte';
	import PasswordInput from '$lib/components/PasswordInput.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';

	import { goto } from '$app/navigation';

	let error: string = '';
	let isLoading: boolean = false;

	const handleSubmit = async (e) => {
		if (isLoading) return;

		isLoading = true;

		e.preventDefault();

		const form = e.target;
		const formData = new FormData(form);

		const response = await fetch(`${SERVER_BASE_URL}/users/register`, {
			method: 'POST',
			body: JSON.stringify(Object.fromEntries(formData)),
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (!response.ok) {
			switch (response.status) {
				case 409:
					error = 'User and/or email already exists';
					break;
				default:
					error = 'An error occurred. Please try again later.';
					break;
			}

			isLoading = false;
			return;
		}

		goto('/signup/verify');
	};

	const handleCancel = () => {
		goto('/');
	};
</script>

<h1>Create a new account</h1>
<div>
	<Form onSubmit={handleSubmit}>
		<label>
			Username
			<input
				type="text"
				id="username"
				name="username"
				value="testuser"
				required
				minlength="5"
				maxlength="12"
			/>
		</label>

		<label>
			First name
			<input type="text" id="first_name" name="first_name" value="Test" required maxlength="30" />
		</label>
		<label>
			Last name
			<input type="text" id="last_name" name="last_name" value="User" required maxlength="30" />
		</label>

		<label>
			Email
			<input type="email" id="email" name="email" value="ibanmontero@gmail.com" required />
		</label>
		<label>
			Password
			<PasswordInput id="password" name="password" value="test123" required />
		</label>

		<div class="flex items-baseline justify-center gap-2">
			<Button type="button" level="secondary" onclick={handleCancel}>Cancel</Button>
			<Button type="submit" level="primary" {isLoading}>Sign up</Button>
		</div>
	</Form>
	{#if error}
		<p class="mt-4 text-red-500">{error}</p>
	{/if}
</div>
