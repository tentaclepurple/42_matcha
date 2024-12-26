<script lang="ts">
	import { userProfileData } from '$lib/state/user-profile-data.svelte';

	const formatTimeStamp = (date: string) => {
		const parsedDate = new Date(date);
		return parsedDate.toLocaleString('en-US', {
			month: 'short',
			day: 'numeric',
			year: 'numeric',
			hour: 'numeric',
			minute: 'numeric',
			second: 'numeric'
		});
	};
</script>

{#if userProfileData.value}
	<div>
		<h2 class="mb-2">Likes received</h2>
		<details>
			<summary>Click here to see the users who liked your profile 🌶️</summary>
			<div class="py-6">
				<ul class="px-10 list-disc">
					{#each userProfileData.value.likesReceived as like}
						<li>
							<span class="text-sm text-gray-800">{formatTimeStamp(like.createdAt)}</span> -
							<a href={`/search/${like.username}?origin=profile`} class="font-bold"
								>{like.username}</a
							>
						</li>
					{/each}
				</ul>
			</div>
		</details>
	</div>
{/if}
