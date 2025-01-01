<script lang="ts">
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { DEFAULT_AVATAR_NAME } from '$lib/constants/avatar';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import { userData } from '$lib/state/user-data.svelte';
	import { AVATAR_ALLOWED_TYPES } from '$lib/constants/files';

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

	let photoActionsIndex: null | number = $state(null);

	let showPicturePreviewIndex = $state<null | number>(null);

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
				const errorData = await res.json();
				throw new Error(errorData.error);
			}

			await userProfileData.fetch();
			await userData.fetch();
		} catch (e) {
			console.error(e);
			error = e;
		} finally {
			e.target.value = '';
		}
	};

	const handlePhotoMouseEnter = (e: MouseEvent, index: number) => {
		const target = e.target as HTMLElement;
		const targetIndex = Number(target?.dataset?.id);

		if (targetIndex === index) photoActionsIndex = index;
	};

	const handlePhotoMouseLeave = () => {
		photoActionsIndex = null;
	};

	const handlePhotoDelete = async (index: number) => {
		const isRelevantButton = index === photoActionsIndex;

		if (!isRelevantButton) return;

		const token = localStorage.getItem('access_token');

		const isProfilePicture = photos[index].isProfile;
		const isLastPicture =
			photos.filter((photo) => !photo.url.endsWith(DEFAULT_AVATAR_NAME)).length === 1;

		if (isProfilePicture && !isLastPicture) {
			error =
				'You cannot delete your profile picture. Please set another picture as profile picture first.';
			return;
		}

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

			await userProfileData.fetch();
			await userData.fetch();
		} catch (e) {
			console.error(e);
			error = 'There was an error deleting the photo. Please try again.';
		}
	};

	const handleNewAvatar = async (index: number) => {
		const token = localStorage.getItem('access_token');

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/profile/update_avatar/${index}`, {
				method: 'PUT',
				headers: {
					authorization: `Bearer ${token}`
				}
			});

			if (!res.ok) {
				throw new Error('Failed to delete photo');
			}

			await userProfileData.fetch();
			await userData.fetch();
		} catch (e) {
			console.error(e);
			error = 'There was an error setting the new avatar. Please try again.';
		}
	};
</script>

<div
	class="mb-2 flex grid-rows-2 flex-wrap items-center justify-start gap-2 sm:grid sm:grid-cols-[200px_170px_170px]"
>
	{#each photos as photo, index}
		<div class={`${index === 0 ? 'sm:row-span-2' : ''} h-full`}>
			{#if photo.url.endsWith(DEFAULT_AVATAR_NAME)}
				<label class="h-full cursor-pointer hover:shadow-lg">
					<span class="sr-only">Upload new picture</span>
					<input
						type="file"
						accept={AVATAR_ALLOWED_TYPES}
						class="hidden"
						onchange={handlePhotoUpload}
						data-id={index}
					/>
					<div
						class="flex h-full min-h-40 w-full min-w-40 items-center justify-center bg-gray-300 shadow-md"
					>
						<img src="/icons/plus.svg" alt="" class="h-8 w-8" />
					</div>
				</label>
			{:else}
				<div
					onmouseenter={(event) => handlePhotoMouseEnter(event, index)}
					onmouseleave={handlePhotoMouseLeave}
					data-id={index}
					role="dialog"
					class={`relative ${photoActionsIndex === index ? 'shadow-lg' : ''} h-full`}
				>
					<div
						class={`${photoActionsIndex === index ? '' : 'sm:hidden'} absolute inset-0 m-auto flex h-full w-full flex-col items-center justify-center gap-2 sm:gap-3 bg-gray-900 bg-opacity-50`}
					>
						<button onclick={() => handlePhotoDelete(index)} title="Delete">
							<img src="/icons/delete.svg" alt="" class="h-10 w-10 rounded-full bg-red-500 p-2" />
						</button>

						<button title="Show" onclick={() => (showPicturePreviewIndex = index)}>
							<img src="/icons/show.svg" alt="" class="h-10 w-10 rounded-full bg-teal-500 p-2" />
						</button>

						{#if !photo.isProfile}
							<button title="Choose as avatar" onclick={() => handleNewAvatar(index)}>
								<img
									src="/icons/avatar.svg"
									alt=""
									class="h-10 w-10 rounded-full bg-slate-200 p-2"
								/>
							</button>
						{/if}
					</div>
					{#if photo.isProfile}
						<div
							class="absolute left-0 top-0 ml-1 mt-1 flex items-center gap-1 rounded-lg bg-teal-100 bg-opacity-80 px-2 py-1 shadow-xl"
						>
							<img src="/icons/avatar.svg" alt="" class="h-4 w-4" />
							<p class="text-sm">Profile picture</p>
						</div>
					{/if}
					<img
						src={getServerAsset(photo.url)}
						alt=""
						class={`h-full min-h-40 min-w-40 sm:min-w-full max-w-40 max-h-40 sm:min-h-full border-2 border-gray-500 object-cover shadow-md`}
					/>
					{#if showPicturePreviewIndex !== null}
						<div
							class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900 bg-opacity-80 p-12"
						>
							<button
								aria-label="Close"
								class="absolute right-0 top-0 mr-3 mt-3 rounded-lg bg-teal-500 p-4 shadow-xl"
								onclick={() => (showPicturePreviewIndex = null)}
							>
								<img src="/icons/close.svg" class="h-8 w-8" alt="" />
							</button>
							<img
								src={getServerAsset(photos[showPicturePreviewIndex].url)}
								alt=""
								class="max-w-screen max-h-screen"
							/>
						</div>
					{/if}
				</div>
			{/if}
		</div>
	{/each}
</div>
{#if error}
	<p class="text-sm text-red-500">{error}</p>
{/if}
