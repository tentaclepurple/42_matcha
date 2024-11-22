<script lang="ts">
	import { DEFAULT_AVATAR_NAME } from '$lib/constants/avatar';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';
	import getServerAsset from '$lib/utils/get-server-asset';

	export let avatarUrl: string;
	export let photos: UserProfileData['photos'];
</script>

<div class="mb-2 flex items-end gap-4">
	<img
		src={getServerAsset(avatarUrl)}
		alt=""
		class="max-h-80 w-56 border-2 border-gray-500 object-cover"
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
