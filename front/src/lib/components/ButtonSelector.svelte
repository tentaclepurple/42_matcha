<script lang="ts">
	const { children } = $props();
</script>

<div class="border-1 w-fit rounded-3xl border border-teal-500 bg-white px-3 py-2 text-xs">
	{@render children()}
</div>
