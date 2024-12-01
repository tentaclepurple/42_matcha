<script lang="ts">
	import { SERVER_BASE_URL } from '$lib/constants/api';

	import Button from '$lib/components/Button.svelte';

	const { username } = $props();

	let error = $state<null | string>(null);

	const handleNewMessage = async (event) => {
		event.preventDefault();
		const form = event.target;

		try {
			const message = form.message.value;

			const token = localStorage.getItem('access_token');

			const res = await fetch(`${SERVER_BASE_URL}/api/chat/send/${username}`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ content: message, type: 'text' })
			});

			if (res.ok) {
				throw new Error();
			}

			const data = await res.json();
		} catch (e) {
			console.error(e);
			error = 'Error sending message';
		} finally {
			form.reset();
		}
	};
</script>

<div class="flex flex-col items-end">
	<div class="mb-4">
		{$inspect(error)}
		{#if error}
			<p class="text-red-500">{error}</p>
		{/if}
	</div>
	<form class="flex w-full items-end gap-3" onsubmit={handleNewMessage}>
		<textarea
			id="message"
			placeholder="Write a new message"
			rows={4}
			required
			minlength={1}
			maxlength={500}
			class="w-full"
		></textarea>
		<Button type="submit" level="primary">Send</Button>
	</form>
</div>
