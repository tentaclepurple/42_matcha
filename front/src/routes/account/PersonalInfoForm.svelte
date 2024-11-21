<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import { userData } from '$lib/stores/user-data';
	import { writable } from 'svelte/store';

	$: currentUserData = $userData;

	let isEditing = false;
	let error = writable('');
	error.subscribe(() => {
		setTimeout(() => {
			error.set('');
		}, DEFAULT_TIMEOUT);
	});

	let success = writable('');
	success.subscribe(() => {
		setTimeout(() => {
			success.set('');
		}, DEFAULT_TIMEOUT);
	});

	const handleSave = async (e) => {
		e.preventDefault();
		error.set('');
		success.set('');

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

			success.set('Profile updated successfully');
		} catch (err) {
			console.error(err);
			error.set('An error occurred. Please try again later.');
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
				value={currentUserData ? currentUserData.username : ''}
				required
				readonly={!isEditing}
				minlength="5"
				maxlength="12"
				autocomplete="username"
			/>
		</label>

		<div class="flex items-center gap-3">
			<label>
				First name:
				<input
					type="text"
					id="first_name"
					name="first_name"
					value={currentUserData ? currentUserData.firstName : ''}
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
					value={currentUserData ? currentUserData.lastName : ''}
					readonly={!isEditing}
					maxlength="30"
					required
					autocomplete="family-name"
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
				value={currentUserData ? currentUserData.email : ''}
				readonly={!isEditing}
				autocomplete="email"
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
					error.set('');
					success.set('');
				}}
			>
				Update info
			</Button>
		{/if}
	</fieldset>
	{#if $success}
		<p class="mt-4 text-green-500">{$success}</p>
	{:else if $error}
		<p class="mt-4 text-red-500">{$error}</p>
	{/if}
</form>
