<script>
	import { DEFAULT_LOCATION } from '$lib/constants/geolocation';
	import { userLocation } from '$lib/state/geolocation.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import { MapLibre, Marker, Popup } from 'svelte-maplibre';

	const { results } = $props();
</script>

{#snippet marker({ user, coordinates, isCurrentUser })}
	<Marker lngLat={coordinates}>
		<div
			class={`h-6 w-6 rounded-full ${isCurrentUser ? 'bg-yellow-500' : 'bg-teal-500'} shadow-lg`}
			aria-label="User marker"
		></div>

		<Popup openOn="click" offset={[0, 0]}>
			<span class="flex h-20 w-20 flex-col items-center justify-center px-2 py-3">
				<img src="icons/avatar.svg" alt="" class="mb-2 h-10 w-10" />
				<span>{user.username}, {user.age}</span>
			</span>
		</Popup>
	</Marker>
{/snippet}

<MapLibre
	center={userLocation.value ?? DEFAULT_LOCATION}
	class="h-[750px] w-full rounded-md"
	interactive={true}
	maxZoom={18}
	minZoom={0}
	standardControls
	style="https://tiles.basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
	zoom={14}
>
	{#if userProfileData?.value}
		{@render marker({
			user: userProfileData.value,
			coordinates: userLocation.value ?? DEFAULT_LOCATION,
			isCurrentUser: true
		})}
	{/if}

	{#each results as user (user.user_id)}
		{@render marker({ user, coordinates: user.location.coordinates, isCurrentUser: false })}
	{/each}
</MapLibre>
