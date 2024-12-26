<script lang="ts">
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
	items,
	summary,
	title
}: {
	summary: string;
	title: string;
	items: View[] | Like[];
})}
	<div>
		<h2 class="mb-2">{title}</h2>
		<details>
			<summary>{summary}</summary>
			<div class="pt-4">
				<ul class="list-disc px-10 flex flex-col gap-2">
					{#each items as item}
						<li>
							<span class="text-sm text-gray-800"
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
	</div>
{/snippet}

{#if userProfileData.value}
	{@render HistorySection({
		items: userProfileData.value.likesReceived,
		title: 'Likes received',
		summary: 'Click here to see the users who liked your profile 🌶️'
	})}

	{@render HistorySection({
		items: userProfileData.value.profileViews,
		title: 'Views received',
		summary: 'Click here to see the users who viewed your profile 👀'
	})}
{/if}
