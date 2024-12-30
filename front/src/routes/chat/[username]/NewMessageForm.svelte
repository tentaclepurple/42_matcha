<script lang="ts">
	import { SERVER_BASE_URL } from '$lib/constants/api';

	import Button from '$lib/components/Button.svelte';

	const { username } = $props();

	let error = $state<null | string>(null);

	const handleFormSubmit = async (event) => {
		event.preventDefault();
		error = '';
		const form = event.target;
		const message = form.message.value;

		form.reset();
		form.message.focus();

		try {
			const token = localStorage.getItem('access_token');

			const res = await fetch(`${SERVER_BASE_URL}/api/chat/send/${username}`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ content: message, type: 'text' })
			});

			if (!res.ok) {
				throw new Error();
			}

			const data = await res.json();
		} catch (e) {
			console.error(e);
			error = 'Error sending message';
		}
	};

	const handleKeydown = (event) => {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			event.target.form.dispatchEvent(new Event('submit'));
		}
	};
</script>

<div class="flex flex-col items-end mt-auto">
	<div class="mb-4">
		{#if error}
			<p class="text-red-500">{error}</p>
		{/if}
	</div>
	<form class="flex w-full items-end gap-3" onsubmit={handleFormSubmit}>
		<textarea
			id="message"
			placeholder="Write a new message"
			required
			rows={3}
			minlength={1}
			maxlength={500}
			class="w-full"
			onkeydown={handleKeydown}
		></textarea>
		<Button type="submit" level="primary">
			<span class="sr-only sm:not-sr-only">Send</span>
			<img src="/icons/send.svg" alt="" class="w-5" />
		</Button>
	</form>
</div>
