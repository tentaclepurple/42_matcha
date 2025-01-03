<script lang="ts">
	import Lottie from '$lib/components/Lottie.svelte';
	import emptyStateAnimation from '$lib/lotties/empty-messages.json';
</script>

<div class="flex w-full sm:flex-col flex-col-reverse items-center justify-center text-center gap-8">
	<div class="sm:w-5/12">
		<Lottie animationData={emptyStateAnimation} loop={true} autoplay={true} />
	</div>
	<div class="flex flex-col items-center justify-center gap-2">
		<h2>It's lonely in here</h2>
		<p>Start a new conversation. Your next soulmate is waiting for you</p>
	</div>
</div>
