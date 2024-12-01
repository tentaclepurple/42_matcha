<script lang="ts">
	const { children } = $props();
</script>

<div class="flex flex-1 justify-center p-4">
	<main class="w-full max-w-screen-2xl flex-1 flex flex-col">
		{@render children()}
	</main>
</div>
