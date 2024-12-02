<script lang="ts">
	import { goto } from '$app/navigation';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';

	const { results } = $props();

	const handleOpenUser = async (event) => {
		const button = event.currentTarget as HTMLButtonElement;
		const username = button.dataset.username;

		goto(`/search/${username}?origin=list`);
	};
</script>

<ul class="grid w-full grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-3 p-8">
	{#each results as user (user.user_id)}
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
					class="mb-2 aspect-square object-cover w-full rounded-md"
				/>
				<span class="text-sm font-bold">{user.username}</span>
				<span class="flex text-xs">
					{user.age}, {user.gender}
					<GenderSymbol gender={user.gender} />
				</span>
				<span class="text-xs">{user.distance} km away</span>
			</button>
		</li>
	{/each}
</ul>
