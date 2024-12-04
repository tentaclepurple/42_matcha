<script lang="ts">
	import { goto } from '$app/navigation';
	import getServerAsset from '$lib/utils/get-server-asset';

	const { profilePhoto, username } = $props();
</script>

<div class="mb-4 flex items-center justify-between">
	<h2 class="sr-only">{username}</h2>
	<button
		class="flex items-center gap-2"
		onclick={() => {
			goto(`/search/${username}?origin=messages`);
		}}
	>
		<img
			src={profilePhoto ? getServerAsset(profilePhoto) : '/icons/avatar.svg'}
			alt=""
			class="border-1 h-8 w-8 rounded-md border border-teal-500 object-cover"
		/>
		<span class="text-xl font-bold">{username}</span>
	</button>
</div>
