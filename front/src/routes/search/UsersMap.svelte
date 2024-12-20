<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import { DEFAULT_LOCATION } from '$lib/constants/geolocation';
	import { userLocation } from '$lib/state/geolocation.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import { MapLibre, Marker, Popup } from 'svelte-maplibre';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { userSearchData } from '$lib/state/user-search.svelte';

	const results = $derived(userSearchData.value ?? []);
</script>

{#snippet marker({
	profilePicture,
	user,
	coordinates,
	isCurrentUser
}: {
	profilePicture: string;
	user: any;
	coordinates: [number, number];
	isCurrentUser: boolean;
})}
	<Marker lngLat={coordinates}>
		<div
			class={`rounded-full ${isCurrentUser ? 'h-9 w-9 bg-yellow-500' : 'h-5 w-5 bg-teal-500'} shadow-lg`}
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
				profilePicture: userProfileData.value.photos.filter((photo) => photo.isProfile)[0].url,
				user: userProfileData.value,
				coordinates: userLocation.value ?? DEFAULT_LOCATION,
				isCurrentUser: true
			})}
		{/if}

		{#each results as user (user.userId)}
			{@render marker({
				profilePicture: user.profilePhoto,
				user,
				coordinates: user.location.coordinates,
				isCurrentUser: false
			})}
		{/each}
	</MapLibre>
</div>
