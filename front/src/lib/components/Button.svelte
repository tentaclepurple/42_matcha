<script lang="ts">
	import Lottie from '$lib/components/Lottie.svelte';
	import spinnerAnimation from '$lib/lotties/spinner.json';

	type ButtonType = 'button' | 'submit' | 'reset';
	type ButtonLevel = 'primary' | 'secondary';

	let {
		children,
		isLoading = false as boolean,
		level = 'primary' as ButtonLevel,
		type = 'button' as ButtonType,
		...restProps
	} = $props();

	let styles =
		level === 'primary'
			? 'rounded bg-teal-500 px-4 py-2 font-bold text-white hover:bg-teal-700'
			: 'bg-transparent hover:bg-teal-500 text-teal-700 font-semibold hover:text-white py-2 px-4 border border-teal-500 hover:border-transparent rounded';
</script>

<button
	{type}
	{...restProps}
	class={`${styles} ${restProps.class} flex items-center justify-center gap-2`}
>
	{@render children()}
	{#if isLoading === true}
		<div class="w-5">
			<Lottie animationData={spinnerAnimation} loop={true} autoplay={true} />
		</div>
	{/if}
</button>
