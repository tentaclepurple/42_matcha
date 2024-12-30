<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { onMount } from 'svelte';

	const { children, confirmLabel, onClose, onConfirm, title } = $props();

	const handleEscPress = (e: KeyboardEvent) => {
		if (e.key === 'Escape') {
			onClose();
		}
	};

	onMount(() => {
		document.addEventListener('keydown', handleEscPress);

		return () => {
			document.removeEventListener('keydown', handleEscPress);
		};
	});
</script>

<div
	class="fixed left-0 top-0 z-50 flex h-full w-full items-start justify-center bg-black bg-opacity-50"
>
	<div class="mt-40 w-full max-w-lg rounded-md bg-white px-8 py-6">
		<h1 class="title-2 mx-auto mb-6 w-4/6 text-center">
			{title}
		</h1>

		<div>
			{@render children()}
		</div>

		<div class="mt-8 flex items-center justify-end gap-2">
			<Button level="secondary" type="button" onclick={onClose}>Cancel</Button>

			<Button level="danger" type="button" onclick={onConfirm}>{confirmLabel}</Button>
		</div>
	</div>
</div>
