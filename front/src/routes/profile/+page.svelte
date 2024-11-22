<script lang="ts">
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { DEFAULT_AVATAR_NAME } from '$lib/constants/avatar';
	import getServerAsset from '$lib/utils/get-server-asset';

	let {
		data
	}: {
		data: {
			profileData: {
				age: number;
				photos: {
					is_profile: boolean;
					uploaded_at: string;
					url: string;
				}[];
				username: string;
			};
		};
	} = $props();

	const avatarUrl = data.profileData.photos.filter((photo) => photo.is_profile)[0]?.url;
	const photos = data.profileData.photos.filter((photo) => !photo.is_profile);
</script>

<PageWrapper>
	<div class="mb-12">
		<h1>Profile</h1>
		<p>This is the profile page.</p>
	</div>

	<div class="mb-4 flex w-fit flex-col items-start">
		<div class="mb-2 flex items-end gap-4">
			<img
				src={getServerAsset(avatarUrl)}
				alt=""
				class="w-56 border-2 border-gray-500 object-cover"
			/>
			<div class="flex items-center gap-2">
				{#each photos as photo}
					{#if photo.url.endsWith(DEFAULT_AVATAR_NAME)}
						<div
							class="flex h-32 w-32 cursor-pointer items-center justify-center bg-gray-300 shadow-md"
						>
							+
						</div>
					{:else}
						<img
							src={getServerAsset(photo.url)}
							alt=""
							class="w-32 border-2 border-gray-500 object-cover shadow-md"
						/>
					{/if}
				{/each}
			</div>
		</div>
		<div class="flex w-56 items-baseline justify-between">
			<p class="text-3xl">{data.profileData.username}</p>
			<p class="text-2xl">{data.profileData.age}</p>
		</div>
	</div>
</PageWrapper>
