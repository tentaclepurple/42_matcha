<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import FameRating from '$lib/components/FameRating.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import { DefaultMarker, MapLibre } from 'svelte-maplibre';
	import getServerAsset from '$lib/utils/get-server-asset';
	import UserActions from './UserActions.svelte';
	import { visitedProfileData } from '$lib/state/visited-profile-data.svelte';
	import InterestsList from '$lib/components/InterestsList.svelte';
	import { DEFAULT_AVATAR_NAME } from '$lib/constants/avatar';

	const { origin } = $props();

	const selectedUser = $derived(visitedProfileData.value);
</script>

{#if selectedUser}
	<div
		class="items-between m-8 flex w-3/5 flex-col items-start justify-between rounded-lg bg-teal-100 p-6"
	>
		<nav class="mb-12 flex w-full items-center justify-between">
			{#if origin}
				<Button
					type="button"
					level="primary"
					onclick={() => {
						switch (origin) {
							case 'profile':
								goto('/profile', { replaceState: true });
								break;
							case 'search':
								goto('/search', { replaceState: true });
								break;
							default:
								goto(`/search?view=${origin}`, { replaceState: true });
						}
					}}
				>
					← Back
				</Button>
			{/if}

			<UserActions {selectedUser} />
		</nav>

		<div class="w-full">
			<div class="mb-6 flex items-center justify-between">
				<div class="flex items-center gap-5">
					<div class="relative">
						<img
							class="h-44 w-44 rounded-lg bg-white object-cover shadow-md"
							src={getServerAsset(
								selectedUser.photos.filter((photo) => photo.isProfile)[0].url || 'icons/avatar.svg'
							)}
							alt=""
						/>
						<p
							class={`absolute bottom-0 right-0 h-7 w-7 rounded-full border border-2 border-teal-100 ${selectedUser.online ? 'bg-green-500' : 'bg-slate-400'}`}
							style="right: -8px; bottom: -8px;"
						>
							<span class="sr-only">{selectedUser.online ? 'Online' : 'Offline'}</span>
						</p>
					</div>
					<ul class="grid grid-flow-col grid-rows-2 gap-3">
						{#each selectedUser.photos.filter((photo) => !photo.isProfile && !photo.url.includes(DEFAULT_AVATAR_NAME)) as photo}
							<li>
								<img
									class="h-20 w-20 rounded-lg bg-white object-cover shadow-md"
									src={getServerAsset(photo.url)}
									alt=""
								/>
							</li>
						{/each}
					</ul>
				</div>

				<FameRating fameRating={selectedUser.fameRating} />
			</div>

			<h2 class="mb-4">{selectedUser.username}, {selectedUser.age}</h2>

			<div class="description-list mb-6 flex flex-col gap-3">
				<dl>
					<dt>Name:</dt>
					<dd>{selectedUser.firstName} {selectedUser.lastName}</dd>
				</dl>

				<dl>
					<dt>Bio:</dt>
					<dd>{selectedUser.biography}</dd>
				</dl>

				<dl>
					<dt>Gender:</dt>
					<dd>
						{selectedUser.gender[0].toUpperCase() + selectedUser.gender.slice(1)}
						<GenderSymbol gender={selectedUser.gender} />
					</dd>
				</dl>

				<dl>
					<dt>Preference:</dt>
					<dd>
						{selectedUser.sexualPreferences[0].toUpperCase() +
							selectedUser.sexualPreferences.slice(1)}
						<PreferenceSymbol preference={selectedUser.sexualPreferences} />
					</dd>
				</dl>

				<dl>
					<dt class="mb-1">Interests</dt>
					<dd>
						<InterestsList interests={selectedUser.interests} />
					</dd>
				</dl>

				{#if !selectedUser.online}
					<dl>
						<dt>Last connected:</dt>
						<dd>
							{new Date(selectedUser.lastConnection).toLocaleDateString('en-US', {
								year: 'numeric',
								month: 'long',
								day: 'numeric',
								hour: 'numeric',
								minute: 'numeric',
								second: 'numeric'
							})}
						</dd>
					</dl>
				{/if}
			</div>
		</div>

		<MapLibre
			center={selectedUser.location.coordinates}
			class="h-[250px] w-full rounded-md"
			interactive={false}
			maxZoom={18}
			minZoom={11}
			standardControls
			style="https://tiles.basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
			zoom={15}
		>
			<DefaultMarker lngLat={selectedUser.location.coordinates} />
		</MapLibre>
	</div>
{/if}

<style>
	.description-list {
		dt {
			font-weight: bold;
		}
	}
</style>
