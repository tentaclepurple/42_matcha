<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import { DEFAULT_LOCATION } from '$lib/constants/geolocation';
	import { userLocation } from '$lib/state/geolocation.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import { MapLibre, Marker, Popup } from 'svelte-maplibre';
	import getServerAsset from '$lib/utils/get-server-asset';

	const { results } = $props();
</script>

{#snippet marker({ profilePicture, user, coordinates, isCurrentUser })}
	<Marker lngLat={coordinates}>
		<div
			class={`h-6 w-6 rounded-full ${isCurrentUser ? 'bg-yellow-500' : 'bg-teal-500'} shadow-lg`}
			aria-label="User marker"
		></div>

		<Popup openOn="click" offset={[0, 0]}>
			<div class="flex flex-col items-center justify-center gap-2 px-2">
				<img
					src={profilePicture ? getServerAsset(profilePicture) : '/icons/avatar.svg'}
					alt=""
					class="aspect-square w-24"
				/>
				<span class="font-xs font-bold">{user.username}</span>
				<span>{user.age}, {user.gender} <GenderSymbol gender={user.gender} /></span>
				<Button
					type="button"
					level="primary"
					onclick={() => {
						goto(`/search/${user.username}?origin=map`);
					}}
				>
					View profile
				</Button>
			</div>
		</Popup>
	</Marker>
{/snippet}

<div class="flex h-[65vh] w-full items-center justify-center">
	<MapLibre
		center={userLocation.value ?? DEFAULT_LOCATION}
		class="h-full w-full rounded-md"
		interactive={true}
		maxZoom={18}
		minZoom={6}
		standardControls
		style="https://tiles.basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
		zoom={14}
	>
		{#if userProfileData?.value}
			{@render marker({
				profilePicture: userProfileData.value.photos.filter((photo) => photo.is_profile)[0].url,
				user: userProfileData.value,
				coordinates: userLocation.value ?? DEFAULT_LOCATION,
				isCurrentUser: true
			})}
		{/if}

		{#each results as user (user.user_id)}
			{@render marker({
				profilePicture: user.profile_photo,
				user,
				coordinates: user.location.coordinates,
				isCurrentUser: false
			})}
		{/each}
	</MapLibre>
</div>
