<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import Form from '$lib/components/Form.svelte';
	import PasswordInput from '$lib/components/PasswordInput.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';

	import { goto } from '$app/navigation';
	import validatePassword from '$lib/utils/validate-password';
	import { MIN_BIRTH_DATA } from '$lib/constants/user';
	import calcEighteenthBirthday from '$lib/utils/calc-eighteenth-birthday';
	import PageWrapper from '$lib/components/PageWrapper.svelte';

	let error: string = $state('');
	$effect(() => {
		if (error) {
			const timeout = setTimeout(() => {
				error = '';
			}, 5000);

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

		const { isValid: isPasswordValid, message: passwordError } = validatePassword(password);
		if (!isPasswordValid) {
			error = passwordError;
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
				switch (response.status) {
					case 409:
						error = 'Username or email already in use';
						break;
					default:
						throw new Error('An error occurred. Please try again later.');
				}
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
	<h1>Create a new account</h1>
	<div>
		<Form onSubmit={handleSubmit}>
			<fieldset disabled={isLoading} class="flex flex-col gap-4">
				<div class="flex items-baseline justify-center gap-4">
					<label>
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
						/>
					</label>
					<label>
						E-mail
						<input type="email" id="email" name="email" placeholder="E-mail" autocomplete="email" />
					</label>
				</div>

				<div>
					<div class="mb-4 flex items-baseline justify-center gap-4">
						<label>
							First name
							<input
								type="text"
								id="first_name"
								name="first_name"
								placeholder="First name"
								required
								maxlength="30"
								autocomplete="given-name"
							/>
						</label>
						<label>
							Last name
							<input
								type="text"
								id="last_name"
								name="last_name"
								placeholder="Last name"
								required
								maxlength="30"
								autocomplete="family-name"
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
						/>
					</label>
				</div>

				<div class="mb-4 flex flex-col gap-4">
					<label class="flex flex-col items-start justify-center">
						Password
						<PasswordInput
							id="password"
							name="password"
							required
							placeholder="Password"
							autocomplete="current-password"
						/>
					</label>
					<label class="flex flex-col items-start justify-center">
						Confirm password
						<PasswordInput
							id="confirm"
							name="confirm"
							required
							placeholder="Confirm password"
							autocomplete="current-password"
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
