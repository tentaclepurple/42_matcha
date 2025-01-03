<script lang="ts">
	import ButtonSelector from '$lib/components/ButtonSelector.svelte';
	import Tooltip from '$lib/components/Tooltip.svelte';
	const { children } = $props();
</script>

<Tooltip
	message="Recommended results cannot be filtered. If you need the filters, go to the All users tab."
	class="left-0 top-9"
>
	<ButtonSelector class="pointer-events-none cursor-not-allowed opacity-60">
		{@render children()}
	</ButtonSelector>
</Tooltip>
