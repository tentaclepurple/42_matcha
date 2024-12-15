<script lang="ts">
	import { goto } from '$app/navigation';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';

	const NUM_RESULTS = 15;

	const { results } = $props();

	let currentPage = $state<number>(0);
	const totalPages = Math.ceil(results.length / NUM_RESULTS);

	const currentResults = $derived(
		results.slice(currentPage * NUM_RESULTS, currentPage * NUM_RESULTS + NUM_RESULTS)
	);

	const handleOpenUser = async (event) => {
		const button = event.currentTarget as HTMLButtonElement;
		const username = button.dataset.username;

		goto(`/search/${username}?origin=list`);
	};
</script>

<div class="items-between flex h-full w-full flex-1 flex-col">
	<ul class="grid w-full grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-3 p-8">
		{#each currentResults as user (user.user_id)}
			<li class="flex items-center justify-center rounded-md bg-teal-50 p-3 shadow-md">
				<button
					type="button"
					data-username={user.username}
					onclick={handleOpenUser}
					class="flex w-full flex-col items-center gap-1"
				>
					<img
						src={getServerAsset(user.profile_photo)}
						alt=""
						class="mb-2 aspect-square w-full rounded-md object-cover"
					/>
					<span class="text-sm font-bold">{user.username}</span>
					<span class="flex text-xs">
						{user.age}, {user.gender}
						<GenderSymbol gender={user.gender} />
					</span>
					<span class="text-xs">
						Likes: {user.sexual_preferences}
						<PreferenceSymbol preference={user.sexual_preferences} />
					</span>
					<span class="text-xs">{user.distance} km away</span>
					<span class="text-xs">{user.fame_rating}% popularity</span>
				</button>
			</li>
		{/each}
	</ul>
	<nav class="mt-auto flex items-center justify-center gap-4 pb-6">
		{#each Array.from({ length: totalPages }, (_, i) => i) as page, index}
			<button
				type="button"
				class={`${index === currentPage ? 'underline' : ''}`}
				onclick={() => (currentPage = index)}
			>
				{index + 1}
			</button>
		{/each}
	</nav>
</div>
