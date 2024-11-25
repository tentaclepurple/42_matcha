<script lang="ts">
	import { onMount } from 'svelte';
	import lottie from 'lottie-web';

	const {
		autoplay = true,
		animationData,
		loop = true
	}: {
		autoplay: boolean;
		animationData: object;
		loop: boolean;
	} = $props();

	let container: HTMLDivElement;

	onMount(() => {
		lottie.loadAnimation({
			container,
			renderer: 'svg',
			loop,
			autoplay,
			animationData
		});
	});
</script>

<div bind:this={container}></div>

<style>
	div {
		width: 100%;
		height: 100%;
	}
</style>
