<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import deserialize from '$lib/utils/deserialize';

	const { selectedUser } = $props();
	console.log('miao', selectedUser);

	let isLikedByMe = $state(selectedUser.likeInfo?.likedByMe);
	let isMatch = $state(selectedUser.likeInfo?.isMatch);

	const handleMatch = async () => {
		const token = localStorage.getItem('access_token');

		const res = await fetch(`${SERVER_BASE_URL}/api/interactions/like/${selectedUser.username}`, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			}
		});

		if (!res.ok) {
			console.error(res);
			return;
		}

		const data = await res.json();

		const { likeAdded } = deserialize(data);

		isLikedByMe = Boolean(likeAdded);
	};
</script>

<div class="flex items-start justify-center gap-3">
	{#if isMatch}
		<Button
			type="button"
			level="primary"
			onclick={() => {
				goto(`/chat/?username=${selectedUser.username}`);
			}}
			aria-label="Send new message"
		>
			<img src="/icons/message.svg" alt="" class="h-7" />
		</Button>
	{/if}

	<div class="flex flex-col items-center justify-center">
		<button
			class={`flex aspect-square items-center justify-center rounded-xl border border-2 border-black ${isMatch ? 'bg-rose-400' : isLikedByMe ? 'bg-rose-200' : 'bg-transparent'} p-2`}
			aria-label="Match"
			onclick={handleMatch}
		>
			{#if isMatch}
				<img src="/icons/like/heart-unlock.svg" alt="" class="h-7" />
			{:else if isLikedByMe}
				<img src="/icons/like/heart-lock.svg" alt="" class="h-7" />
			{:else}
				<img src="/icons/like/heart.svg" alt="" class="h-7" />
			{/if}
		</button>
		<p class="text-sm">
			{#if isMatch}
				Matched
			{:else if isLikedByMe}
				Liked
			{:else}
				Like
			{/if}
		</p>
	</div>
</div>
