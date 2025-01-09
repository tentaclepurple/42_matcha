<script lang="ts">
	import { messagesData } from '$lib/state/messages.svelte';

	$effect(() => {
		if (messagesData.value) {
			const lastMessage = document.querySelector(
				`#message-${messagesData.value.messages.length - 1}`
			);
			lastMessage?.scrollIntoView({ behavior: 'smooth' });
		}
	});
</script>

<ul
	class="flex h-full flex-col items-start gap-2 overflow-auto rounded-md bg-gray-100 px-4 py-4 sm:mb-4 sm:px-12 sm:py-6"
>
	{#if messagesData.value?.messages}
		{#each messagesData.value.messages as message, i}
			<li
				class={`flex flex-col items-end gap-1 ${message.fromMe ? 'self-end bg-teal-300' : 'bg-gray-300'} max-w-lg rounded-lg p-3`}
				id={`message-${i}`}
			>
				<span class="text-sm sm:text-base">{message.content}</span>
				<span class="text-xs">
					{new Date(message.createdAt).toLocaleString('en-US', {
						hour: 'numeric',
						minute: 'numeric'
					})}
				</span>
			</li>
		{/each}
	{/if}
</ul>
