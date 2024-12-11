<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import deserialize from '$lib/utils/deserialize';
	import spinnerAnimationData from '$lib/lotties/spinner.json';
	import Lottie from '$lib/components/Lottie.svelte';
	import { visitedProfileData } from '$lib/state/visited-profile-data.svelte';
	import { onMount } from 'svelte';

	const selectedUser = $derived(visitedProfileData.value);

	onMount(() => {
		if (!selectedUser) {
			goto('/search');
		}
	});

	let isLikedByMe = $derived(Boolean(selectedUser?.likeInfo?.likedByMe));
	let isMatch = $derived(Boolean(selectedUser?.likeInfo?.isMatch));

	let isLoading = $state(false);

	const handleMatch = async () => {
		isLoading = true;
		const token = localStorage.getItem('access_token');

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/interactions/like/${selectedUser.username}`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				throw new Error('Failed to like user');
			}

			const data = await res.json();

			const { likeAdded } = deserialize(data);

			await visitedProfileData.fetch(selectedUser?.username);
		} catch (error) {
			console.error(error);
		} finally {
			isLoading = false;
		}
	};
</script>

<div class="ml-auto flex items-start justify-center gap-3">
	{#if isMatch}
		<Button
			type="button"
			level="primary"
			onclick={() => {
				goto(`/chat/${selectedUser.username}`);
			}}
			aria-label="Send new message"
		>
			<img src="/icons/message.svg" alt="" class="h-7" />
		</Button>
	{/if}

	<div class="flex flex-col items-center justify-center">
		{#if isLoading}
			<button
				type="button"
				class="flex aspect-square w-12 cursor-not-allowed items-center justify-center rounded-xl border border-2 border-black bg-gray-300 p-2"
			>
				<Lottie animationData={spinnerAnimationData} autoplay={true} loop={true} />
			</button>
		{:else}
			<button
				class={`flex aspect-square w-12 items-center justify-center rounded-xl border border-2 border-black ${isMatch ? 'bg-rose-400' : isLikedByMe ? 'bg-rose-200' : 'bg-transparent'} p-2`}
				aria-label="Match"
				onclick={handleMatch}
			>
				{#if isMatch}
					<img src="/icons/like/heart-unlock.svg" alt="" class="w-full" />
				{:else if isLikedByMe}
					<img src="/icons/like/heart-lock.svg" alt="" class="w-full" />
				{:else}
					<img src="/icons/like/heart.svg" alt="" class="w-full" />
				{/if}
			</button>
		{/if}
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
