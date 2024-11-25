<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Form from '$lib/components/Form.svelte';
	import PasswordInput from '$lib/components/PasswordInput.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { login } from '$lib/stores/auth';

	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { fetchUserData } from '$lib/stores/user-data';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import { getUserLocation } from '$lib/stores/geolocation';

	let error: string = $state('');
	$effect(() => {
		if (error) {
			const timeout = setTimeout(() => {
				error = '';
			}, DEFAULT_TIMEOUT);

			return () => {
				clearTimeout(timeout);
			};
		}
	});

	let isLoading: boolean = $state(false);

	const handleSubmit = async (e) => {
		if (isLoading) return;

		isLoading = true;
		error = '';

		e.preventDefault();

		const formData = new FormData(e.target);

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/users/login`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(Object.fromEntries(formData))
			});

			if (!res.ok) {
				switch (res.status) {
					case 401:
						error = 'Invalid e-mail or password';
						break;
					default:
						error = 'An error occurred. Please try again later.';
						break;
				}

				return;
			}

			const { access_token, user } = await res.json();

			localStorage.setItem('access_token', access_token);
			login();
			await getUserLocation();
			await fetchUserData();

			const { profile_completed: profileCompleted } = user;
			return profileCompleted ? goto('/dashboard') : goto('/profile');
		} catch (err) {
			error = 'An error occurred. Please try again later.';
			return;
		} finally {
			isLoading = false;
		}
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
							autocomplete="email"
							required
						/>
					</label>

					<label>
						Password
						<PasswordInput
							id="password"
							name="password"
							value="Ciaociao1!"
							required
							autocomplete="current-password"
						/>
					</label>
				</fieldset>

				<a href="/forget-password">Forgot your password?</a>

				<div class="flex items-baseline justify-center gap-2">
					<Button type="button" level="secondary" onclick={handleCancel}>Cancel</Button>
					<Button type="submit" {isLoading}>Log in</Button>
				</div>

				{#if error}
					<p class="mt-2 text-red-500">{error}</p>
				{/if}
			</Form>
		</div>

		<p class="mt-4">
			Don't have an account yet? <a href="/signup">Sign up</a>
		</p>
	</div>
</PageWrapper>
