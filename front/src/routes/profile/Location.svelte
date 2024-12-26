<script lang="ts">
	import { DefaultMarker, MapLibre } from 'svelte-maplibre';
	import { userLocation } from '$lib/state/geolocation.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import Button from '$lib/components/Button.svelte';
	import IconTitle from '$lib/components/IconTitle.svelte';

	const handleLocationUpdate = async () => {
		await userLocation.getUserLocation();
	};
</script>

{#if userProfileData.value}
	<div class="mt-6 w-full">
		<IconTitle title="Your location" icon="/icons/location.svg" />
		<p class="mb-6">
			Your location is detected automatically from your device. Use the Refresh button to force an
			update.
		</p>
		<div class="relative rounded-lg shadow-md">
			<Button
				level="primary"
				class="absolute right-0 top-0 z-20 mr-2 mt-2 shadow-md"
				onclick={handleLocationUpdate}
			>
				Refresh
				{#if userLocation.isLoading}
					<img src="/icons/reload.svg" alt="" class="h-4 w-4 animate-spin" />
				{/if}
			</Button>
			<MapLibre
				center={userLocation?.value ?? userProfileData.value.location.coordinates}
				class="z-10 h-[250px] w-full rounded-md"
				interactive={false}
				maxZoom={18}
				minZoom={10}
				standardControls
				style="https://tiles.basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
				zoom={11}
			>
				<DefaultMarker lngLat={userLocation?.value ?? userProfileData.value.location.coordinates} />
			</MapLibre>
		</div>
	</div>
{/if}
