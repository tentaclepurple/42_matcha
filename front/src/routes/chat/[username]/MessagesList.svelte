<script lang="ts">
	import { messagesData } from '$lib/state/messages.svelte';
	import { userData } from '$lib/state/user-data.svelte';

	$effect(() => {
		if (userData.value) {
			const lastMessage = document.querySelector('#message-' + (messagesData.value.length - 1));
			lastMessage?.scrollIntoView();
		}
	});
</script>

<ul
	class="mb-4 flex h-full max-h-[65vh] flex-col items-start gap-2 overflow-auto rounded-md bg-gray-100 px-3 py-6"
>
	{#each messagesData.value as message, i}
		{$inspect(message)}
		<li
			class={`flex flex-col gap-1 items-end ${message.fromMe ? 'self-end bg-teal-300' : 'bg-gray-300'} rounded-lg p-3 max-w-[70%]`}
			id={`message-${i}`}
		>
			{message.content}
			<span class="text-xs">
				{new Date(message.createdAt).toLocaleString('en-US', {
					hour: 'numeric',
					minute: 'numeric'
				})}
			</span>
		</li>
	{/each}
</ul>
