<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Form from '$lib/components/Form.svelte';

	import { goto } from '$app/navigation';
	import PasswordInput from '$lib/components/PasswordInput.svelte';

	let error: string = '';

	const handleSubmit = async (e) => {
		e.preventDefault();

		console.log('submitting form');

		const form = e.target;
		const formData = new FormData(form);

		const response = await fetch('http://localhost:5000/api/users/register', {
			method: 'POST',
			body: JSON.stringify(Object.fromEntries(formData)),
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (!response.ok) {
			switch (response.status) {
				case 409:
					error = 'User already exists';
					break;
			}
		}
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
			<input type="text" id="username" name="username" value="testuser" />
		</label>

		<label>
			First name
			<input type="text" id="first_name" name="first_name" value="Test" />
		</label>
		<label>
			Last name
			<input type="text" id="last_name" name="last_name" value="User" />
		</label>

		<label>
			Email
			<input type="email" id="email" name="email" value="ibanmontero@gmail.com" />
		</label>
		<label>
			Password
			<PasswordInput id="password" name="password" value="test123" />
		</label>

		<div>
			<Button type="button" level="secondary" onclick={handleCancel}>Cancel</Button>
			<Button type="submit" level="primary">Sign up</Button>
		</div>
	</Form>
	{#if error}
		<p class="mt-4 text-red-500">{error}</p>
	{/if}
</div>
