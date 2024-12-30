<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import spinnerAnimationData from '$lib/lotties/spinner.json';
	import Lottie from '$lib/components/Lottie.svelte';
	import { visitedProfileData } from '$lib/state/visited-profile-data.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import Tooltip from '$lib/components/Tooltip.svelte';

	const selectedUser = $derived(visitedProfileData.value);

	let isLikedByMe = $derived(Boolean(selectedUser?.likeInfo?.likedByMe));
	let isMatch = $derived(Boolean(selectedUser?.likeInfo?.isMatch));

	let isLoading = $state(false);

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
				throw new Error('Failed to match user');
			}

			await visitedProfileData.fetch(selectedUser?.username);
		} catch (error) {
			console.error(error);
		} finally {
			isLoading = false;
		}
	};
</script>

{#if selectedUser}
	<div class="ml-auto flex items-center gap-3">
		{#if userProfileData.hasProfilePicture}
			<div class="flex items-center justify-center gap-3">
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

				<div class="relative flex flex-col items-center justify-center">
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
							class={`flex aspect-square w-12 items-center justify-center rounded-xl border border-2 border-black ${isMatch ? 'bg-rose-300' : isLikedByMe ? 'bg-rose-200' : 'bg-transparent'} p-2`}
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
					<p class="absolute -bottom-5 text-xs" id="like-button">
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
			<Tooltip
				message="Add a profile picture to interact with other users."
				class="-bottom-30 right-0"
			>
				<button
					class="flex cursor-not-allowed flex-col items-center justify-center opacity-60"
					disabled
					aria-disabled="true"
				>
					<div
						class={`flex aspect-square w-12 items-center justify-center rounded-xl border border-2 border-gray-700 bg-gray-100 p-2`}
					>
						<img src="/icons/like/heart-lock.svg" alt="" class="w-full" />
					</div>
				</button>
			</Tooltip>
		{/if}
	</div>
{/if}
