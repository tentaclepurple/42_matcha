<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { SERVER_BASE_URL } from '$lib/constants/api';

	let userIdMenu: string | null = $state(null);
	let unblockedUsername: string | null = $state(null);

	const handleUnblock = async (username: string) => {
		const userAnswer = confirm(
			'Are you sure you want to unblock this user? You will be able to see their profile and interact with them again.'
		);

		if (!userAnswer) return;

		const accessToken = localStorage.getItem('access_token');

		if (!accessToken) {
			console.error('No access token found');
			return;
		}

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/interactions/unblock/${username}`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${accessToken}`,
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				throw new Error('Failed to like user');
			}

			unblockedUsername = username;
			await userProfileData.fetch();
		} catch (error) {
			console.error(error);
		}
	};
</script>

{#if userProfileData.value}
	<div>
		<h2 class="mb-2">Blocked users</h2>
		{#if userProfileData.value.blockedUsers.length === 0}
			<p>You haven't blocked any users yet.</p>
		{:else}
			<details>
				<summary>Click here to see a list of users you blocked</summary>
				<div class="mt-2">
					<ul class="flex flex-wrap items-center gap-3">
						{#each userProfileData.value.blockedUsers as blockedUser}
							<li
								class="relative"
								onmouseenter={() => (userIdMenu = blockedUser.userId)}
								onmouseleave={() => (userIdMenu = null)}
							>
								{$inspect(userIdMenu, blockedUser.userId)}
								{#if userIdMenu === blockedUser.userId}
									<div
										class="absolute left-0 top-0 flex h-full w-full items-center justify-center rounded-md"
									>
										<Button class="absolute" onclick={() => handleUnblock(blockedUser.username)}>
											Unblock
										</Button>
									</div>
								{/if}
								<div class="flex flex-col items-center gap-1">
									<img
										src={getServerAsset(blockedUser.profilePhoto)}
										alt=""
										class="w-28 rounded-md shadow-md"
									/>
									<span class="text-xs">{blockedUser.username}</span>
								</div>
							</li>
						{/each}
					</ul>
				</div>
			</details>
		{/if}
		{#if unblockedUsername}
			<div class="mt-2">
				<p role="status" class="text-green-500">
					You unblocked <span class="font-bold">{unblockedUsername}</span>! Visit
					<a href={`/search/${unblockedUsername}?origin=profile`}>their profile</a> to interact with
					them again.
				</p>
			</div>
		{/if}
	</div>
{/if}
