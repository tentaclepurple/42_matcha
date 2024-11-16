<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<div class="flex min-h-screen flex-col justify-between">
	<div class="flex items-center justify-center bg-lime-300 p-4">
		<header class="flex w-full max-w-screen-2xl items-baseline justify-between">
			<nav class="flex items-baseline justify-center gap-2">
				<a href="/">Home</a>
				<a href="/about">About</a>
			</nav>

			<div>
				<a href="/login">Log in</a>
			</div>
		</header>
	</div>

	<div class="flex flex-1 justify-center p-4">
		<main class="w-full max-w-screen-2xl flex-1">
			{@render children()}
		</main>
	</div>

	<div class="bg-lime-500 p-4 flex justify-center items-center">
		<footer class="w-full max-w-screen-2xl">This is the footer. Here we can mention something about ourselves.</footer>
	</div>
</div>
