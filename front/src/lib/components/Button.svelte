<script lang="ts">
	import Lottie from '$lib/components/Lottie.svelte';
	import spinnerAnimation from '$lib/lotties/spinner.json';

	type ButtonType = 'button' | 'submit' | 'reset';
	type ButtonLevel = 'primary' | 'secondary' | 'danger';

	let {
		children,
		isLoading = false as boolean,
		level = 'primary' as ButtonLevel,
		type = 'button' as ButtonType,
		class: CLASS = '' as string,
		...restProps
	} = $props();

	let styles;

	switch (level) {
		case 'primary':
			styles = 'rounded bg-teal-500 px-4 py-2 font-bold text-white hover:bg-teal-700';
			break;
		case 'secondary':
			styles =
				'bg-transparent hover:bg-teal-500 text-teal-700 font-semibold hover:text-white py-2 px-4 border border-2 border-teal-500 hover:border-transparent rounded';
			break;
		case 'danger':
			styles = 'rounded bg-red-500 px-4 py-2 font-bold text-white hover:bg-red-700';
			break;
	}
	level === 'primary';
</script>

<button {type} {...restProps} class={`${styles} flex items-center justify-center gap-2 ${CLASS}`}>
	{@render children()}
	{#if isLoading === true}
		<div class="w-5">
			<Lottie animationData={spinnerAnimation} loop={true} autoplay={true} />
		</div>
	{/if}
</button>
