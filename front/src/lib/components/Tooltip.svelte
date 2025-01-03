<script lang="ts">
	const { children, message, class: CLASS = '' } = $props();

	let showTooltip = $state(false);
</script>

<button
	class="relative"
	onmouseenter={() => (showTooltip = true)}
	ontouchstart={() => (showTooltip = true)}
	onmouseleave={() => (showTooltip = false)}
	ontouchend={() => (showTooltip = false)}
	onclick={() => (showTooltip = !showTooltip)}
	aria-label="Press to show a tooltip"
>
	{@render children()}
	{#if showTooltip}
		<div
			role="alert"
			class={`absolute mt-2 w-56 rounded-lg bg-gray-100 px-4 py-2 shadow-md z-10 ${CLASS}`}
		>
			<p class="text-sm">{message}</p>
		</div>
	{/if}
</button>
