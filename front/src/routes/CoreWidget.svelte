<script lang="ts">
	const { count, icon, onClick, disabled = false } = $props();
</script>

<button
	class="relative flex h-9 w-9 items-center justify-center rounded-full border border-2 border-teal-500 bg-teal-100"
	{disabled}
	onclick={onClick}
>
	<img src={icon} alt="" class="w-5" />
	<p
		class={`absolute flex h-5 w-5 items-center justify-center rounded-full ${count > 0 ? 'bg-red-600' : 'bg-gray-500'} text-xs font-bold text-white`}
		style="bottom: -8px; right: -8px;"
	>
		{count ? count : '0'}
	</p>
</button>
