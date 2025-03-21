<script lang="ts">
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { DEFAULT_AVATAR_NAME } from '$lib/constants/avatar';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { fetchUserProfileData } from '$lib/stores/user-profile-data';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';

	const { photos }: { photos: UserProfileData['photos'] } = $props();

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

	let showDeleteButton: null | number = $state(null);

	const handlePhotoUpload = async (e) => {
		try {
			error = '';
			const token = localStorage.getItem('access_token');

			const photo = e.target.files[0];

			const formData = new FormData();
			formData.append('photo', photo);

			const input = e.target;
			const index = input.dataset.id;

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
			error = 'There was an error uploading the photo. Please try again.';
		} finally {
			e.target.value = '';
		}
	};

	const handlePhotoMouseEnter = (e: MouseEvent, index: number) => {
		const target = e.target as HTMLElement;
		const targetIndex = Number(target?.dataset?.id);

		if (targetIndex === index) showDeleteButton = index;
	};

	const handlePhotoMouseLeave = () => {
		showDeleteButton = null;
	};

	const handlePhotoDelete = async (index: number) => {
		const isRelevantButton = index === showDeleteButton;

		if (!isRelevantButton) return;

		const token = localStorage.getItem('access_token');

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/profile/delete_photo/${index}`, {
				method: 'DELETE',
				headers: {
					authorization: `Bearer ${token}`
				}
			});

			if (!res.ok) {
				throw new Error('Failed to delete photo');
			}

			await res.json();

			await fetchUserProfileData();
		} catch (e) {
			console.error(e);
			error = 'There was an error deleting the photo. Please try again.';
		}
	};
</script>

<div class="mb-2 grid grid-cols-[200px_170px_170px] grid-rows-2 gap-2">
	{#each photos as photo, index}
		<div class={`${index === 0 ? 'row-span-2' : ''} h-full min-h-40`}>
			{#if photo.url.endsWith(DEFAULT_AVATAR_NAME)}
				<label class="h-full cursor-pointer hover:shadow-lg">
					<span class="sr-only">Upload new picture</span>
					<input type="file" class="hidden" onchange={handlePhotoUpload} data-id={index} />
					<div class="flex h-full items-center justify-center bg-gray-300 shadow-md">
						<img src="/icons/plus.svg" alt="" class="h-8 w-8" />
					</div>
				</label>
			{:else}
				<div
					onmouseenter={(event) => handlePhotoMouseEnter(event, index)}
					onmouseleave={handlePhotoMouseLeave}
					onclick={() => handlePhotoDelete(index)}
					data-id={index}
					class={`relative ${showDeleteButton === index ? 'shadow-lg' : ''} h-full`}
					role={showDeleteButton === index ? 'button' : ''}
				>
					{#if showDeleteButton === index}
						<img
							src="/icons/delete.svg"
							alt=""
							class="absolute inset-0 m-auto h-10 w-10 rounded-full bg-red-500 p-2"
						/>
					{/if}
					<img
						src={getServerAsset(photo.url)}
						alt=""
						class={`h-full border-2 border-gray-500 object-cover shadow-md`}
					/>
				</div>
			{/if}
		</div>
	{/each}
</div>
{#if error}
	<p class="text-sm text-red-500">{error}</p>
{/if}
