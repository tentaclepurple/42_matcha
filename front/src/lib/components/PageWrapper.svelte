<script lang="ts">
	const { children, class: CLASS = '' } = $props();
</script>

<div class={`flex flex-1 justify-center p-4 ${CLASS}`}>
	<main class="flex w-full max-w-screen-xl flex-1 flex-col">
		{@render children()}
	</main>
</div>
