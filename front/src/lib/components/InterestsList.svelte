<script lang="ts">
	import { COLORS_PALETTE } from '$lib/constants/colors';

	const { interests, class: CLASS = '' } = $props();
</script>

<ul class={`flex flex-wrap items-baseline gap-1 ${CLASS}`}>
	{#each [...interests].sort() as interest, index}
		<li
			class="text-xs sm:text-sm shrink-0 rounded-md px-2 py-1"
			style={`background-color: ${COLORS_PALETTE[index % COLORS_PALETTE.length]}`}
		>
			#{interest.toLowerCase()}
		</li>
	{/each}
</ul>
