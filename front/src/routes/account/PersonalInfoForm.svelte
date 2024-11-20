<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import type UserData from '$lib/interfaces/user-data.interface';

	export let currentUserData: UserData;

	let isEditing = false;
	let error = '';
	let success = '';

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
		} finally {
			isEditing = false;
		}
	};
</script>

<form onsubmit={handleSave}>
	<fieldset class="flex flex-col items-start gap-5">
		<label>
			Username:
			<input
				type="text"
				id="username"
				name="username"
				value={currentUserData.username}
				required
				readonly={!isEditing}
				minlength="5"
				maxlength="12"
			/>
		</label>

		<div class="flex items-center gap-3">
			<label>
				First name:
				<input
					type="text"
					id="first_name"
					name="first_name"
					value={currentUserData.firstName}
					readonly={!isEditing}
					maxlength="30"
					required
				/>
			</label>
			<label>
				Last name:
				<input
					type="text"
					id="last_name"
					name="last_name"
					value={currentUserData.lastName}
					readonly={!isEditing}
					maxlength="30"
					required
				/>
			</label>
		</div>

		<label>
			Email:
			<input
				type="email"
				id="email"
				name="email"
				required
				value={currentUserData.email}
				readonly={!isEditing}
			/>
		</label>

		{#if isEditing}
			<Button type="submit" level="primary">Save</Button>
		{:else}
			<Button
				type="button"
				level="secondary"
				onclick={() => {
					isEditing = !isEditing;
					error = '';
					success = '';
				}}
			>
				Update info
			</Button>
		{/if}
	</fieldset>
	{#if success}
		<p class="mt-4 text-green-500">{success}</p>
	{:else if error}
		<p class="mt-4 text-red-500">{error}</p>
	{/if}
</form>
