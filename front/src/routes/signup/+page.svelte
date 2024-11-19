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

	let error: string = '';
	let isLoading: boolean = false;

	const handleSubmit = async (e) => {
		if (isLoading) return;

		isLoading = true;
		e.preventDefault();

		const form = e.target;
		const formData = new FormData(form);

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

<PageWrapper>
	<h1>Create a new account</h1>
	<div>
		<Form onSubmit={handleSubmit}>
			<fieldset disabled={isLoading} class="flex flex-col gap-3">
				<div class="mb-4 flex items-baseline justify-center gap-4">
					<label>
						Username
						<input
							type="text"
							id="username"
							name="username"
							value="ngasco"
							required
							minlength="5"
							maxlength="12"
						/>
					</label>
					<label>
						Email
						<input
							type="email"
							id="email"
							name="email"
							value="chiamatemi.nico@gmail.com"
							required
						/>
					</label>
				</div>

				<div class="mb-4">
					<div class="flex items-baseline justify-center gap-4">
						<label>
							First name
							<input
								type="text"
								id="first_name"
								name="first_name"
								value="Nicolas"
								required
								maxlength="30"
							/>
						</label>
						<label>
							Last name
							<input
								type="text"
								id="last_name"
								name="last_name"
								value="Gasco"
								required
								maxlength="30"
							/>
						</label>
					</div>

					<label>
						Birth year
						<input
							type="date"
							id="age"
							name="age"
							value="1992-01-07"
							min={MIN_BIRTH_DATA}
							max={calcEighteenthBirthday()}
							required
						/>
					</label>
				</div>

				<div class="mb-4">
					<label class="flex flex-col items-start justify-center">
						Password
						<PasswordInput id="password" name="password" value="Ciaociao1!" required />
					</label>
					<label class="flex flex-col items-start justify-center">
						Confirm password
						<PasswordInput id="confirm" name="confirm" value="Ciaociao1!" required />
					</label>
				</div>
			</fieldset>

			{#if error}
				<p class="text-red-500">{error}</p>
			{/if}

			<div class="flex items-baseline justify-center gap-2">
				<Button type="button" level="secondary" onclick={handleCancel}>Cancel</Button>
				<Button type="submit" level="primary" {isLoading}>Sign up</Button>
			</div>
		</Form>
	</div>
</PageWrapper>
