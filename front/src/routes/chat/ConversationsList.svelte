<script lang="ts">
	import { page } from '$app/stores';
	import getServerAsset from '$lib/utils/get-server-asset';

	const { conversations } = $props();

	let username = $state<string | null>(null);

	$effect(() => {
		username = $page.params.username ?? null;
	});
</script>

<ul class="flex flex-col gap-2">
	{#if conversations.length === 0}
		<p>There are no conversations yet</p>
	{:else}
		{#each conversations as conversation}
			<li class={`${username === conversation.user.username && 'bg-gray-200'} rounded-md p-1`}>
				<a
					href={`/matcha/chat/${conversation.user.username}`}
					class="flex items-center gap-2 no-underline"
				>
					<div class="relative" aria-hidden="true">
						<img
							src={getServerAsset(conversation.user.profilePhoto) ?? '/matcha/icons/avatar.svg'}
							alt=""
							class="h-6 w-6 rounded-md bg-white object-cover"
						/>
						<span
							class={`border-1 absolute h-2 w-2 rounded-full border ${conversation.user.online ? 'border-black bg-green-500' : 'border-slate-700 bg-slate-200'}`}
							style="bottom: -1px; right: -1px"
						></span>
					</div>
					<span>
						{conversation.user.username}
						<span class="sr-only">
							{#if conversation.user.online}
								Online
							{:else}
								Offline
							{/if}
						</span>
					</span>
				</a>
			</li>
		{/each}
	{/if}
</ul>
