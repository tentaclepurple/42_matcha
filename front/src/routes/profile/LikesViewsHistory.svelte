<script lang="ts">
	import IconTitle from '$lib/components/IconTitle.svelte';
	import type { Like, View } from '$lib/interfaces/user-profile-data.interface';
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

{#snippet HistorySection({
	icon,
	items,
	summary,
	title
}: {
	icon: string;
	summary: string;
	title: string;
	items: View[] | Like[];
})}
	<div>
		<IconTitle {title} {icon} />
		{#if items.length === 0}
			<p class="text-gray-800">You currently have no history to show.</p>
		{:else}
			<details>
				<summary>{summary}</summary>
				<div class="pt-4">
					<ul class="flex list-disc flex-col gap-2 px-10">
						{#each items as item}
							<li>
								<span class="text-xs sm:text-sm text-gray-800"
									>{#if 'createdAt' in item}
										{formatTimeStamp(item.createdAt)}
									{:else if 'lastView' in item}
										{formatTimeStamp(item.lastView)}
									{/if}
								</span>
								-
								<a href={`/search/${item.username}?origin=profile`} class="font-bold">
									{item.username}
								</a>
							</li>
						{/each}
					</ul>
				</div>
			</details>
		{/if}
	</div>
{/snippet}

{#if userProfileData.value}
	{@render HistorySection({
		icon: '/icons/like.svg',
		items: userProfileData.value.likesReceived,
		title: 'Likes received',
		summary: 'Click here to see the users who liked your profile.'
	})}

	{@render HistorySection({
		icon: '/icons/view.svg',
		items: userProfileData.value.profileViews,
		title: 'Views received',
		summary: 'Click here to see the users who viewed your profile.'
	})}
{/if}
