<script lang="ts">
	const { results } = $props();
</script>

<ul class="grid w-full grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-2 p-8">
	{#each results as user}
		<li class="flex h-[150px] w-[150px] items-center justify-center bg-teal-50 p-3">
			<img src={user.profile_photo} alt="" />
			<span>{user.username}, {user.age}</span>
		</li>
	{/each}
</ul>
