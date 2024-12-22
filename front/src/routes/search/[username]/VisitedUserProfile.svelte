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

	const { origin } = $props();

	const selectedUser = $derived(visitedProfileData.value);
</script>

{#if selectedUser}
	<div
		class="items-between m-8 flex w-3/5 flex-col items-start justify-between rounded-lg bg-teal-200 p-6"
	>
		<nav class="mb-12 flex w-full items-center justify-between">
			{#if origin}
				<Button
					type="button"
					level="primary"
					onclick={() => {
						goto(`/search?view=${origin}`, { replaceState: true });
					}}
				>
					← Back
				</Button>
			{/if}

			<UserActions {selectedUser} />
		</nav>

		<div class="w-full">
			<div class="mb-6 flex items-center justify-between">
				<div class="relative">
					<img
						class="h-40 w-40 rounded-lg bg-white object-cover shadow-md"
						src={getServerAsset(
							selectedUser.photos.filter((photo) => photo.isProfile)[0].url || 'icons/avatar.svg'
						)}
						alt=""
					/>
					<p
						class={`absolute bottom-0 right-0 h-7 w-7 rounded-full border border-2 border-teal-200 ${selectedUser.online ? 'bg-green-500' : 'bg-slate-400'}`}
						style="right: -8px; bottom: -8px;"
					>
						<span class="sr-only">{selectedUser.online ? 'Online' : 'Offline'}</span>
					</p>
				</div>

				<FameRating fameRating={selectedUser.fameRating} />
			</div>
			<h2 class="mb-4">{selectedUser.username}, {selectedUser.age}</h2>

			<div class="description-list mb-6 flex flex-col gap-3">
				<dl>
					<dt>Bio:</dt>
					<dd>{selectedUser.biography}</dd>
				</dl>

				<dl>
					<dt>Gender:</dt>
					<dd>{selectedUser.gender} <GenderSymbol gender={selectedUser.gender} /></dd>
				</dl>

				<dl>
					<dt>Preference:</dt>
					<dd>
						{selectedUser.sexualPreferences}
						<PreferenceSymbol preference={selectedUser.sexualPreferences} />
					</dd>
				</dl>

				<dl>
					<dt class="mb-1">Interests</dt>
					<dd>
						<InterestsList interests={selectedUser.interests} />
					</dd>
				</dl>
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
