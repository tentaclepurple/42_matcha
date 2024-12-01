<script lang="ts">
	import { page } from '$app/stores';

	const { conversations } = $props();

	let username = $state<string | null>(null);

	$effect(() => {
		username = $page.params.username ?? null;
	});
</script>

<ul class="flex flex-col gap-2">
	{#each conversations as conversation}
		<li class={`${username === conversation.user.username && 'bg-gray-300'} rounded-md p-1`}>
			<a href={`/chat/${conversation.user.username}`} class="flex items-center gap-2">
				<img src="/icons/avatar.svg" alt="" class="h-6 w-6 rounded-md bg-white object-cover" />
				<span>{conversation.user.username}</span>
			</a>
		</li>
	{/each}
</ul>
