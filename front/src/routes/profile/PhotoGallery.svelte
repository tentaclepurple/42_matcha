<script lang="ts">
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { DEFAULT_AVATAR_NAME } from '$lib/constants/avatar';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { fetchUserProfileData } from '$lib/stores/user-profile-data';
	import { writable } from 'svelte/store';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';

	let error = writable('');
	error.subscribe(() => {
		setTimeout(() => {
			error.set('');
		}, DEFAULT_TIMEOUT);
	});

	export let photos: UserProfileData['photos'];

	const handlePhotoUpload = async (e) => {
		try {
			error.set('');
			const token = localStorage.getItem('access_token');

			const photo = e.target.files[0];

			const formData = new FormData();
			formData.append('photo', photo);

			const input = e.target;
			const index = +input.dataset.id + 1;

			const res = await fetch(`${SERVER_BASE_URL}/api/profile/update_photo/${index}`, {
				method: 'PUT',
				headers: {
					authorization: `Bearer ${token}`
				},
				body: formData
			});

			if (!res.ok) {
				throw new Error('Failed to upload photo');
			}

			await fetchUserProfileData();
		} catch (e) {
			console.error(error);
			error.set('There was an error uploading the photo. Please try again.');
		} finally {
			e.target.value = '';
		}
	};
</script>

<div class="mb-2 flex items-end gap-4">
	<div class="flex items-end gap-2">
		{#each photos as photo, index}
			{#if photo.url.endsWith(DEFAULT_AVATAR_NAME)}
				<label class="cursor-pointer hover:shadow-lg">
					<span class="sr-only">Upload new picture</span>
					<input type="file" class="hidden" onchange={handlePhotoUpload} data-id={index} />
					<div
						class={`flex ${index === 0 ? 'h-56 w-40' : 'h-32 w-32'} items-center justify-center bg-gray-300 shadow-md`}
					>
						+
					</div>
				</label>
			{:else}
				<img
					src={getServerAsset(photo.url)}
					alt=""
					class={`${index === 0 ? 'h-56 w-40' : 'h-32 w-32'} border-2 border-gray-500 object-cover shadow-md`}
				/>
			{/if}
		{/each}
	</div>
</div>
{#if $error}
	<p class="text-sm text-red-500">{$error}</p>
{/if}
