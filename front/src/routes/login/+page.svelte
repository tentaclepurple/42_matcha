<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Form from '$lib/components/Form.svelte';
	import PasswordInput from '$lib/components/PasswordInput.svelte';

	import { goto } from '$app/navigation';

	let error: string = '';

	const handleSubmit = async (e) => {
		e.preventDefault();

		const formData = new FormData(e.target);

		const res = await fetch('http://localhost:5000/api/users/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(Object.fromEntries(formData))
		});

		if (!res.ok) {
			switch (res.status) {
				case 401:
					error = 'Your email address is not verified';
					break;
			}
		}

		const data = await res.json();

		console.log(data);
	};

	const handleCancel = () => {
		goto('/');
	};
</script>

<h1>Log in</h1>
<div>
	<p class="mb-4">This is where you can log in</p>
	<div>
		<Form onSubmit={handleSubmit}>
			<label>
				Username
				<input type="text" id="username" name="username" value="testuser" />
			</label>

			<label>
				Password
				<PasswordInput id="password" name="password" value="test123" />
			</label>

			<div>
				<Button type="button" level="secondary" onclick={handleCancel}>Cancel</Button>
				<Button type="submit">Log in</Button>
			</div>
		</Form>
		{#if error}
			<p class="mt-2 text-red-500">{error}</p>
		{/if}
	</div>

	<p class="mt-4">
		Don't have an account yet? <a href="/signup">Sign up</a>
	</p>
</div>
