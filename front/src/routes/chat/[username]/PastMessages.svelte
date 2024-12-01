<script lang="ts">
	const { messages } = $props();
</script>

<ul class="flex flex-col items-start gap-2 px-3 py-6 bg-gray-50 rounded-md mb-4">
	{#each messages as message}
		{$inspect(message)}
		<li
			class={`flex flex-col items-end ${message.fromMe ? 'self-end bg-teal-300' : 'bg-gray-300'} rounded-lg p-3`}
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
