<script>
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userAuth } from '$lib/state/auth.svelte';
	import { onMount } from 'svelte';

	onMount(() => {
		if (userAuth.isAuthenticated) {
			goto('/search', { replaceState: true });
		}
	});
</script>

<div class="wrapper flex flex-1 flex-col items-center justify-center">
	<PageWrapper>
		<div class="mt-32 flex h-full flex-1 flex-col items-center justify-start">
			<h1 class="mb-4 text-9xl">Matcha</h1>
			<p class="mb-4 text-4xl">Dating. Made easy.</p>
		</div>
	</PageWrapper>
</div>

<div class="flex items-center justify-center bg-teal-500 p-4">
	<footer class="w-full max-w-screen-2xl">
		<nav class="flex items-baseline justify-between gap-2">
			<a href="/about">About</a>
			This is the footer. Here we can mention something about ourselves.
		</nav>
	</footer>
</div>

<style>
	.wrapper {
		background: url('/images/splash.jpg') no-repeat center center;
		background-size: cover;
		background-position: bottom;
	}
</style>
