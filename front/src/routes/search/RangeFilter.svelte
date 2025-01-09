<script lang="ts">
	let {
		label,
		minValue,
		maxValue,
		min,
		max,
		step,
		onChangeMin = null,
		onChangeMax = null
	} = $props();
</script>

<div class="flex items-center gap-1">
	<p aria-hidden="true">{label}:</p>

	{#if onChangeMin}
		<label class="flex items-center gap-1">
			<span class="sr-only">{label} (min): {minValue}</span>
			<p aria-hidden="true">{minValue}</p>
			<input
				type="range"
				{min}
				{max}
				value={minValue}
				{step}
				oninput={(e) => onChangeMin(+e.target?.value)}
				class="w-20"
			/>
		</label>
	{/if}

	{#if onChangeMax}
		<label class="flex items-center gap-1">
			<span class="sr-only">{label} (max): {maxValue}</span>
			<input
				type="range"
				{min}
				{max}
				value={maxValue}
				{step}
				oninput={(e) => onChangeMax(+e.target?.value)}
				class="w-20"
			/>
			<p aria-hidden="true">{maxValue}</p>
		</label>
	{/if}
</div>
