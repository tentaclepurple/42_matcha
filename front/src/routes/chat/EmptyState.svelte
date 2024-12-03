<script lang="ts">
	import Lottie from '$lib/components/Lottie.svelte';
	import emptyStateAnimation from '$lib/lotties/empty-messages.json';
</script>

<div class="flex w-full flex-col items-center justify-center">
	<div class="mb-8 w-5/12">
		<Lottie animationData={emptyStateAnimation} loop={true} autoplay={true} />
	</div>
	<h2 class="mb-2">It's lonely in here</h2>
	<p>Start a new conversation. Your next soulmate is waiting for you</p>
</div>
