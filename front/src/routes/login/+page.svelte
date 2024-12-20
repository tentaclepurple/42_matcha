<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Form from '$lib/components/Form.svelte';
	import PasswordInput from '$lib/components/PasswordInput.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';

	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import { userLocation } from '$lib/state/geolocation.svelte';
	import { userAuth } from '$lib/state/auth.svelte';
	import { userData } from '$lib/state/user-data.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';

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
			userAuth.login();
			await userLocation.getUserLocation();
			await userData.fetch();
			await userProfileData.fetch();

			const { profile_completed: profileCompleted } = user;
			return profileCompleted ? goto('/search') : goto('/profile?welcome=true');
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
		<Form onSubmit={handleSubmit}>
			<fieldset disabled={isLoading} class="flex w-full flex-col items-start gap-3">
				<label>
					E-mail
					<input
						type="email"
						id="email"
						name="email"
						autocomplete="email"
						placeholder="Your e-mail"
						required
						class="min-w-[300px]"
					/>
				</label>

				<label>
					Password
					<PasswordInput
						id="password"
						name="password"
						required
						autocomplete="current-password"
						placeholder="Your password"
						class="min-w-[300px]"
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

		<p class="mt-4">
			Don't have an account yet? <a href="/signup">Sign up</a>
		</p>
	</div>
</PageWrapper>
