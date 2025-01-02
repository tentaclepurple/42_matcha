<script lang="ts">
	const { fameRating } = $props();
</script>

<div class="flex flex-col items-center sm:block rounded-lg sm:rounded-xl bg-teal-400 p-2 sm:p-3">
	<span class="text-2xl sm:text-4xl font-bold">{fameRating}</span>% fame
</div>
