<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import { userData } from '$lib/state/user-data.svelte';

	let isEditing: boolean = $state(false);

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

	let success: string = $state('');
	$effect(() => {
		if (success) {
			const timeout = setTimeout(() => {
				success = '';
			}, DEFAULT_TIMEOUT);

			return () => {
				clearTimeout(timeout);
			};
		}
	});

	const handleSave = async (e) => {
		e.preventDefault();
		error = '';
		success = '';

		const formData = new FormData(e.target);

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/users/update_user`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('access_token')}`
				},
				body: JSON.stringify({
					username: formData.get('username'),
					first_name: formData.get('first_name'),
					last_name: formData.get('last_name'),
					email: formData.get('email')
				})
			});

			if (!res.ok) {
				throw new Error('Something went wrong');
			}

			success = 'Profile updated successfully';
		} catch (err) {
			console.error(err);
			error = 'An error occurred. Please try again later.';

			// Reset form values to the current user data
			e.target.username.value = userData?.value?.username ?? '';
			e.target.first_name.value = userData?.value?.firstName ?? '';
			e.target.last_name.value = userData?.value?.lastName ?? '';
			e.target.email.value = userData?.value?.email ?? '';
		} finally {
			isEditing = false;
		}
	};
</script>

<form onsubmit={handleSave}>
	<fieldset class="grid grid-cols-2 grid-rows-3 gap-x-3 gap-y-5">
		<label class="col-span-2">
			Username:
			<input
				type="text"
				id="username"
				name="username"
				value={userData?.value ? userData.value.username : ''}
				required
				readonly={!isEditing}
				minlength="5"
				maxlength="12"
				autocomplete="username"
			/>
		</label>

		<label>
			First name:
			<input
				type="text"
				id="first_name"
				name="first_name"
				value={userData?.value ? userData.value.firstName : ''}
				readonly={!isEditing}
				maxlength="30"
				required
				autocomplete="given-name"
			/>
		</label>

		<label>
			Last name:
			<input
				type="text"
				id="last_name"
				name="last_name"
				value={userData?.value ? userData.value.lastName : ''}
				readonly={!isEditing}
				maxlength="30"
				required
				autocomplete="family-name"
			/>
		</label>

		<label class="col-span-2">
			Email:
			<input
				type="email"
				id="email"
				name="email"
				required
				value={userData?.value ? userData.value.email : ''}
				readonly={!isEditing}
				autocomplete="email"
				class="w-full"
			/>
		</label>
	</fieldset>

	<div class="mt-6">
		{#if isEditing}
			<Button type="submit" level="primary">Save</Button>
		{:else}
			<Button
				type="button"
				level="primary"
				onclick={() => {
					isEditing = !isEditing;
					error = '';
					success = '';
				}}
			>
				Update info
			</Button>
		{/if}
	</div>

	{#if success}
		<p class="mt-4 text-green-500">{success}</p>
	{:else if error}
		<p class="mt-4 text-red-500">{error}</p>
	{/if}
</form>
