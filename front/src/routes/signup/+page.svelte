<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Form from '$lib/components/Form.svelte';
	import PasswordInput from '$lib/components/PasswordInput.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';

	import { goto } from '$app/navigation';
	import { MIN_BIRTH_DATA } from '$lib/constants/user';
	import calcEighteenthBirthday from '$lib/utils/calc-eighteenth-birthday';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { DEFAULT_MESSAGE_TIMEOUT } from '$lib/constants/timeout';

	let error: string = $state('');
	$effect(() => {
		if (error) {
			const timeout = setTimeout(() => {
				error = '';
			}, DEFAULT_MESSAGE_TIMEOUT);

			return () => {
				clearTimeout(timeout);
			};
		}
	});

	let isLoading: boolean = $state(false);

	const handleSubmit = async (e) => {
		if (isLoading) return;
		e.preventDefault();

		isLoading = true;
		error = '';

		const form = e.target;
		const formData = new FormData(form);

		const username = formData.get('username') as string;
		const hasWhiteSpace = username.match(/\s/);
		if (hasWhiteSpace) {
			error = 'Username cannot contain spaces';
			isLoading = false;
			return;
		}

		const password = formData.get('password') as string;
		const confirmPassword = formData.get('confirm') as string;
		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			isLoading = false;
			return;
		}

		const birthDay = formData.get('age') as string;
		const birthYear = new Date(birthDay).getFullYear();
		const age = new Date().getFullYear() - birthYear;
		formData.set('age', age.toString());

		try {
			const response = await fetch(`${SERVER_BASE_URL}/api/users/register`, {
				method: 'POST',
				body: JSON.stringify(Object.fromEntries(formData)),
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (!response.ok) {
				const { error: errorMessage } = await response.json();
				error = errorMessage;

				return;
			}

			goto('/signup/verify');
		} catch (err) {
			error = 'An error occurred. Please try again later.';
		} finally {
			isLoading = false;
		}
	};
</script>

<PageWrapper>
	<h1 class="mb-4">Create a new account</h1>
	<div>
		<Form onSubmit={handleSubmit}>
			<fieldset disabled={isLoading} class="flex w-full flex-col gap-4 sm:w-auto">
				<div class="flex flex-col items-baseline justify-center gap-4 sm:flex-row">
					<label class="w-full">
						Username
						<input
							type="text"
							id="username"
							name="username"
							placeholder="Username"
							required
							minlength="5"
							maxlength="12"
							autocomplete="username"
							class="w-full"
						/>
					</label>
					<label class="w-full">
						E-mail
						<input
							type="email"
							id="email"
							name="email"
							placeholder="E-mail"
							autocomplete="email"
							required
							class="w-full"
						/>
					</label>
				</div>

				<div>
					<div class="mb-4 flex flex-col items-baseline justify-center gap-4 sm:flex-row">
						<label class="w-full">
							First name
							<input
								type="text"
								id="first_name"
								name="first_name"
								placeholder="First name"
								required
								maxlength="30"
								autocomplete="given-name"
								class="w-full"
							/>
						</label>
						<label class="w-full">
							Last name
							<input
								type="text"
								id="last_name"
								name="last_name"
								placeholder="Last name"
								required
								maxlength="30"
								autocomplete="family-name"
								class="w-full"
							/>
						</label>
					</div>

					<label>
						Birth date
						<input
							type="date"
							id="age"
							name="age"
							min={MIN_BIRTH_DATA}
							max={calcEighteenthBirthday()}
							required
							autocomplete="bday"
							class="w-full sm:w-auto"
						/>
					</label>
				</div>

				<div class="mb-4 flex flex-col gap-4">
					<label class="flex w-full flex-col items-start justify-center sm:w-auto">
						Password
						<PasswordInput
							id="password"
							name="password"
							required
							placeholder="Password"
							autocomplete="current-password"
							class="w-full sm:w-auto"
						/>
					</label>
					<label class="flex w-full flex-col items-start justify-center sm:w-auto">
						Confirm password
						<PasswordInput
							id="confirm"
							name="confirm"
							required
							placeholder="Confirm password"
							autocomplete="current-password"
							class="w-full sm:w-auto"
						/>
					</label>
				</div>
			</fieldset>

			{#if error}
				<p class="text-red-500">{error}</p>
			{/if}

			<div class="flex items-baseline justify-center gap-2">
				<Button
					type="button"
					level="secondary"
					onclick={() => {
						goto('/login');
					}}
				>
					Cancel
				</Button>
				<Button type="submit" level="primary" {isLoading}>Sign up</Button>
			</div>
		</Form>
	</div>
</PageWrapper>
