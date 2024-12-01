<script lang="ts">
	const { username } = $props();
</script>

<div class="mb-4 flex items-center justify-between">
	<h2>{username}</h2>
	<a href={`/search/${username}?origin=map`} class="flex items-center gap-1">
		<img src="/icons/avatar.svg" alt="" class="h-5 w-5" />
		Profile
	</a>
</div>
