<script lang="ts">
	const { alt = '', src, ...restProps } = $props();
</script>

<div class="rounded-full border-2 border-teal-500 p-4">
	<img {src} {alt} {...restProps} />
</div>
