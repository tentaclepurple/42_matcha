<script lang="ts">
	let { onSubmit, children } = $props();
</script>

<form onsubmit={onSubmit} class="flex flex-col items-start gap-4">
	{@render children()}
</form>
