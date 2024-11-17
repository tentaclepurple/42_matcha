<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Form from '$lib/components/Form.svelte';
	import PasswordInput from '$lib/components/PasswordInput.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { login } from '$lib/stores/auth';

	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';

	let error: string = '';
	let isLoading: boolean = false;

	const handleSubmit = async (e) => {
		if (isLoading) return;

		isLoading = true;

		e.preventDefault();

		const formData = new FormData(e.target);

		const res = await fetch(`${SERVER_BASE_URL}/users/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(Object.fromEntries(formData))
		});

		if (!res.ok) {
			switch (res.status) {
				case 401:
					error = 'Invalid e-mail or password.';
					break;
				default:
					error = 'An error occurred. Please try again later.';
					break;
			}

			isLoading = false;
			return;
		}

		const { access_token, user } = await res.json();

		localStorage.setItem('access_token', access_token);
		login();
		isLoading = false;

		const { profile_completed: profileCompleted } = user;
		return profileCompleted ? goto('/dashboard') : goto('/profile');
	};

	const handleCancel = () => {
		goto('/');
	};
</script>

<PageWrapper>
	<h1>Log in</h1>
	<div>
		<p class="mb-4">This is where you can log in</p>
		<div>
			<Form onSubmit={handleSubmit}>
				<fieldset disabled={isLoading}>
					<label>
						E-mail
						<input
							type="email"
							id="email"
							name="email"
							value="chiamatemi.nico@gmail.com"
							required
						/>
					</label>

					<label>
						Password
						<PasswordInput id="password" name="password" value="Ciaociao1!" required />
					</label>
				</fieldset>

				<div class="flex items-baseline justify-center gap-2">
					<Button type="button" level="secondary" onclick={handleCancel}>Cancel</Button>
					<Button type="submit" {isLoading}>Log in</Button>
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
</PageWrapper>
