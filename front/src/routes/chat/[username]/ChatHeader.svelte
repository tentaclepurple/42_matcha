<script lang="ts">
	import getServerAsset from '$lib/utils/get-server-asset';

	const { profilePhoto, username } = $props();
</script>

<div class="mb-4 flex items-center justify-between">
	<div class="flex items-center gap-2">
		<img src={getServerAsset(profilePhoto)} alt="" class="h-8 w-8 rounded-md border border-1 border-teal-500" />
		<h2>{username}</h2>
	</div>
	<a href={`/search/${username}?origin=map`} class="flex items-center gap-1">
		<img src="/icons/avatar.svg" alt="" class="h-5 w-5" />
		Profile
	</a>
</div>
