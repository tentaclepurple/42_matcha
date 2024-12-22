<script lang="ts">
	import { goto } from '$app/navigation';
	import RoundAvatar from '$lib/components/RoundAvatar.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { DEFAULT_AVATAR_NAME } from '$lib/constants/avatar';
	import { AVATAR_MAX_SIZE } from '$lib/constants/files';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import { userData } from '$lib/state/user-data.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { onMount } from 'svelte';

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

	let isLoading: boolean = $state(false);

	let avatarUrl: string = $derived(
		getServerAsset(userData?.value?.profilePhoto ?? '/icons/avatar.svg')
	);

	const token = localStorage.getItem('access_token');

	onMount(async () => {
		if (!token) {
			goto('/login', { replaceState: true });
		}

		await userData.fetch();
	});

	const handleEditAvatar = async (e) => {
		error = '';
		success = '';
		isLoading = true;

		const { files } = e.target;
		const file = files[0];

		if (!file) {
			error = 'Something went wrong. Please try again.';
			return;
		}

		if (file.size > AVATAR_MAX_SIZE) {
			error = 'File is too large. Please choose a smaller one.';
			return;
		}

		const formData = new FormData();
		formData.append('photo', file, file.name);
		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/profile/update_photo/0`, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${token}`
				},
				body: formData
			});

			if (!res.ok) {
				throw new Error();
			}

			await userData.fetch();

			success = 'Avatar updated successfully!';
		} catch (err) {
			console.error(err);
			error = 'Something went wrong. Please try again.';
		} finally {
			isLoading = false;
			e.target.value = '';
		}
	};

	const handleDeleteAvatar = async () => {
		error = '';
		success = '';
		isLoading = true;

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/profile/delete_photo/0`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (!res.ok) {
				throw new Error();
			}

			await userData.fetch();

			success = 'Avatar deleted successfully!';
		} catch (err) {
			console.error(err);
			error = 'Something went wrong. Please try again.';
		} finally {
			isLoading = false;
		}
	};
</script>

<h2>Avatar</h2>
<div class="gap-42 flex max-w-sm items-center gap-4">
	<div class="relative">
		<RoundAvatar src={avatarUrl} alt="" size="l" />
		{#if !userData?.value?.profilePhoto.endsWith(DEFAULT_AVATAR_NAME) && !isLoading}
			<button
				type="button"
				class="absolute bottom-0 left-0 rounded-full bg-red-500 p-2 shadow-md hover:bg-red-600"
				aria-label="Delete"
				onclick={handleDeleteAvatar}
			>
				<img src="/icons/delete.svg" alt="" class="w-6" />
			</button>
		{/if}
	</div>
	<form>
		<fieldset class="flex flex-col items-start gap-4">
			<label
				class="cursor-pointer rounded bg-teal-500 px-4 py-2 font-bold text-white hover:bg-teal-700"
			>
				Change avatar
				<input
					type="file"
					id="photo"
					name="photo"
					accept="image/png, image/jpeg"
					class="sr-only"
					onchange={handleEditAvatar}
					onclick={() => {
						error = '';
						success = '';
					}}
				/>
			</label>
			<p class="text-sm text-gray-600">
				Double-check that the image is in PNG or JPG format and that it does not exceed 5 MB.
			</p>
		</fieldset>
	</form>
</div>
{#if success}
	<p class="mt-4 text-green-500">{success}</p>
{:else if error}
	<p class="mt-4 text-red-500">{error}</p>
{/if}
