<script lang="ts">
	import { onMount } from 'svelte';
	import lottie from 'lottie-web';

	export let animationData: object;
	export let loop: boolean = true;
	export let autoplay: boolean = true;

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
