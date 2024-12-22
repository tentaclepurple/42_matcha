<script>
	import { beforeNavigate, goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userAuth } from '$lib/state/auth.svelte';

	beforeNavigate(() => {
		if (userAuth.isAuthenticated) {
			goto('/search', { replaceState: true });
		}
	});
</script>

<div class="wrapper flex flex-1 flex-col items-center justify-center">
	<PageWrapper>
		<div class="mt-32 flex h-full flex-1 flex-col items-center justify-start">
			<h1 class="mb-4 text-6xl sm:text-9xl">
				<div aria-hidden="true">M<span class="text-5xl sm:text-8xl">🍵</span>tcha</div>
				<div class="sr-only">Matcha</div>
			</h1>
			<p class="mb-4 text-3xl sm:text-4xl">Dating. Made easy.</p>
		</div>
	</PageWrapper>
</div>

<div class="flex items-center justify-center bg-teal-500 p-3">
	<footer class="flex w-full max-w-screen-2xl justify-center sm:justify-end text-sm">
		<small>
			Made with <span class="animate-pulse">♡</span> by
			<a href="https://github.com/tentaclepurple" target="_blank" rel="noopener noreferrer">
				imontero
			</a>
			and
			<a href="https://github.com/nicolasgasco" target="_blank" rel="noopener noreferrer">ngasco</a
			>.
		</small>
	</footer>
</div>

<style>
	.wrapper {
		background: url('/images/splash.jpg') no-repeat center center;
		background-size: cover;
		background-position: bottom;
	}
</style>
