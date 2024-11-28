<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import FameRating from '$lib/components/FameRating.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import { DefaultMarker, MapLibre } from 'svelte-maplibre';
	import getServerAsset from '$lib/utils/get-server-asset';

	const { selectedUser, origin } = $props();
</script>

{#if selectedUser}
	<div class="items-between m-8 flex w-3/5 flex-col justify-between rounded-lg bg-teal-200 p-6">
		<nav class="mb-12">
			<Button
				type="button"
				level="primary"
				onclick={() => {
					goto(`/search?view=${origin}`, { replaceState: true });
				}}
			>
				← Back
			</Button>
		</nav>
		<div>
			<div class="flex items-center justify-between">
				<img
					class="shadow-mg h-32 w-32 bg-white object-cover"
					src={getServerAsset(
						selectedUser.photos.filter((photo) => photo.is_profile)[0].url || 'icons/avatar.svg'
					)}
					alt=""
				/>

				<FameRating fameRating={selectedUser.fameRating} />
			</div>
			<h2>{selectedUser.username}, {selectedUser.age}</h2>

			<div class="description-list mb-6 flex flex-col gap-3">
				<dl>
					<dt>Gender:</dt>
					<dd>{selectedUser.gender} <GenderSymbol gender={selectedUser.gender} /></dd>
				</dl>

				<dl>
					<dt>Interested in:</dt>
					<dd>
						{selectedUser.sexualPreference}
						<PreferenceSymbol preference={selectedUser.sexualPreference} />
					</dd>
				</dl>

				<dl>
					<dt>Bio:</dt>
					<dd>{selectedUser.biography}</dd>
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
			zoom={14}
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
