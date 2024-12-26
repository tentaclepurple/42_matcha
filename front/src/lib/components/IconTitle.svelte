<script lang="ts">
	const { title, icon } = $props();
</script>

<h2 class="mb-2 flex items-center gap-2">
	<img src={icon} alt="" class="w-6 opacity-70" />
	{title}
</h2>
