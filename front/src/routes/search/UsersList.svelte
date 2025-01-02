<script lang="ts">
	import { goto } from '$app/navigation';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import Lottie from '$lib/components/Lottie.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';
	import emptyAnimationData from '$lib/lotties/empty-users.json';
	import InterestsList from '$lib/components/InterestsList.svelte';
	import { userSearchData } from '$lib/state/user-search.svelte';

	const NUM_RESULTS = 15;

	const { results } = $props();

	let currentPage = $state<number>(0);
	let totalPages = $state(Math.ceil(results.length / NUM_RESULTS));

	$effect(() => {
		totalPages = Math.ceil(results.length / NUM_RESULTS);
	});

	$effect(() => {
		if (results) {
			currentPage = 0;
		}
	});

	const currentResults = $derived(
		results.slice(currentPage * NUM_RESULTS, currentPage * NUM_RESULTS + NUM_RESULTS)
	);

	const handleOpenUser = async (event) => {
		const button = event.currentTarget as HTMLButtonElement;
		const username = button.dataset.username;

		goto(`/search/${username}?origin=list`);
	};
</script>

{#if userSearchData.value}
	<div class="flex items-center justify-center">
		{#if results.length === 0}
			<div class="flex flex-col items-center p-6">
				<h2 class="mb-2">It's lonely in here</h2>
				<p class="mb-6">There are no users with these filters. Try again with different filters.</p>
				<div class="sm:w-96">
					<Lottie animationData={emptyAnimationData} loop={true} autoplay={true} />
				</div>
			</div>
		{:else}
			<div class="items-between flex h-full w-full flex-1 flex-col">
				<ul
					class="grid w-full grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-2 p-2 sm:grid-cols-[repeat(auto-fill,minmax(200px,1fr))] sm:gap-3 sm:p-8"
				>
					{#each currentResults as user}
						<li class="flex items-center justify-center rounded-md bg-teal-50 p-2 shadow-md sm:p-3">
							<button
								type="button"
								data-username={user.username}
								onclick={handleOpenUser}
								class="flex h-full w-full flex-col items-center gap-1 text-xs"
							>
								<img
									src={getServerAsset(user.profilePhoto)}
									alt=""
									class="mb-2 aspect-square w-full rounded-md object-cover"
								/>
								<span class="text-sm font-bold">{user.username}</span>
								<span class="flex">
									{user.age}, {user.gender}
									<GenderSymbol gender={user.gender} />
								</span>
								<span>
									Likes: {user.sexualPreferences}
									<PreferenceSymbol preference={user.sexualPreferences} />
								</span>
								<span>
									{#if user.distance < 1}
										{user.distance * 1000} m
									{:else}
										{user.distance} km
									{/if} away</span
								>
								<span class="mb-4">{user.fameRating}% popularity</span>
								<InterestsList
									interests={user.interests}
									class="flex items-center justify-center"
								/>
							</button>
						</li>
					{/each}
				</ul>
				<nav
					class="mx-auto mt-auto flex flex-wrap items-center justify-center gap-4 px-12 pb-6 sm:w-4/6"
				>
					{#each Array.from({ length: totalPages }, (_, i) => i) as _, index}
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
		{/if}
	</div>
{/if}
