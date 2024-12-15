<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import PhotoGallery from './PhotoGallery.svelte';
	import UserDataSection from './UserDataSection.svelte';
	import UserDataForm from './UserDataForm.svelte';
	import { DefaultMarker, MapLibre } from 'svelte-maplibre';
	import { userLocation } from '$lib/state/geolocation.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import FameRating from '$lib/components/FameRating.svelte';

	if (!userProfileData.value) {
		goto('/login');
	}

	let isProfileComplete = $derived(
		Boolean(
			userProfileData?.value?.gender &&
				userProfileData?.value?.sexualPreferences &&
				userProfileData?.value?.biography
		)
	);
</script>

<PageWrapper>
	{#if userProfileData?.value}
		<div class="mb-12">
			<h1>Profile</h1>
			<p class="max-w-lg">This is where you can update your public profile.</p>
			<p>If you're looking for your account info, click <a href="/account">here</a>.</p>
		</div>

		<div class="m-auto mb-4 flex w-fit flex-col items-start justify-center">
			<PhotoGallery photos={userProfileData.value.photos} />

			<div class="mb-6 flex w-full items-baseline justify-between">
				<h2>{userProfileData.value.username}, {userProfileData.value.age}</h2>
				<FameRating fameRating={userProfileData.value.fameRating} />
			</div>

			{#if isProfileComplete}
				<UserDataSection />
			{:else}
				<div class="flex flex-col justify-center rounded-lg bg-teal-100 px-12 py-6">
					<h2 class="mb-6">Complete your profile to find your soulmate</h2>
					<UserDataForm />
				</div>
			{/if}

			<div class="mt-6 w-full rounded-lg shadow-md">
				<h2>Your location</h2>
				<MapLibre
					center={userLocation?.value ?? userProfileData.value.location.coordinates}
					class="h-[250px] w-full rounded-md"
					interactive={false}
					maxZoom={18}
					minZoom={10}
					standardControls
					style="https://tiles.basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
					zoom={11}
				>
					<DefaultMarker
						lngLat={userLocation?.value ?? userProfileData.value.location.coordinates}
					/>
				</MapLibre>
			</div>
		</div>
	{/if}
</PageWrapper>
