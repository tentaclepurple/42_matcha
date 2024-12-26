<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import spinnerAnimationData from '$lib/lotties/spinner.json';
	import Lottie from '$lib/components/Lottie.svelte';
	import { visitedProfileData } from '$lib/state/visited-profile-data.svelte';
	import { onMount } from 'svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';

	const selectedUser = $derived(visitedProfileData.value);

	onMount(() => {
		if (!selectedUser) {
			goto('/search');
		}
	});

	let isLikedByMe = $derived(Boolean(selectedUser?.likeInfo?.likedByMe));
	let isMatch = $derived(Boolean(selectedUser?.likeInfo?.isMatch));

	let isLoading = $state(false);

	let showTooltip = $state(false);

	const handleMatch = async () => {
		if (!selectedUser) return;

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

			await visitedProfileData.fetch(selectedUser?.username);
		} catch (error) {
			console.error(error);
		} finally {
			isLoading = false;
		}
	};

	const handleBlock = async () => {
		if (!selectedUser) return;

		const answer = confirm('Are you sure you want to block this user?');

		if (!answer) return;

		const token = localStorage.getItem('access_token');

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/interactions/block/${selectedUser.username}`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				throw new Error('Failed to like user');
			}

			await visitedProfileData.fetch(selectedUser?.username);
		} catch (error) {
			console.error(error);
		}
	};
</script>

{#if selectedUser}
	<div class="ml-auto">
		{#if userProfileData.hasProfilePicture}
			<div class="flex items-start justify-center gap-3">
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
					<button
						class="flex aspect-square w-12 items-center justify-center rounded-xl border border-2 border-black bg-red-500 p-2"
						aria-labelledby="block-button"
						onclick={handleBlock}
					>
						<img src="/icons/block.svg" alt="" class="w-full" />
					</button>
					<p class="text-sm" id="block-button">Block</p>
				</div>

				<div class="flex flex-col items-center justify-center">
					{#if isLoading}
						<button
							type="button"
							class="flex aspect-square w-12 cursor-not-allowed items-center justify-center rounded-xl border border-2 border-black bg-gray-300 p-2"
							aria-label="Loading"
						>
							<Lottie animationData={spinnerAnimationData} autoplay={true} loop={true} />
						</button>
					{:else}
						<button
							class={`flex aspect-square w-12 items-center justify-center rounded-xl border border-2 border-black ${isMatch ? 'bg-rose-400' : isLikedByMe ? 'bg-rose-200' : 'bg-transparent'} p-2`}
							aria-labelledby="like-button"
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
					<p class="text-sm" id="like-button">
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
		{:else}
			<div class="relative">
				<button
					class="flex cursor-not-allowed flex-col items-center justify-center opacity-60"
					disabled
					aria-disabled="true"
					onmouseenter={() => (showTooltip = true)}
					onmouseleave={() => (showTooltip = false)}
				>
					<div
						class={`flex aspect-square w-12 items-center justify-center rounded-xl border border-2 border-gray-700 bg-gray-100 p-2`}
					>
						<img src="/icons/like/heart-lock.svg" alt="" class="w-full" />
					</div>
					<p class="text-gray-700">Like</p>
				</button>
				{#if showTooltip}
					<div
						role="alert"
						class="-bottom-30 absolute right-0 mt-2 w-56 rounded-lg bg-gray-100 px-4 py-2 shadow-md"
					>
						<p>Add a profile picture to interact with other users.</p>
					</div>
				{/if}
			</div>
		{/if}
	</div>
{/if}
