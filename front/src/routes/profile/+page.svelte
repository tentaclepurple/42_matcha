<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userProfileData } from '$lib/stores/user-profile-data';
	import PhotoGallery from './PhotoGallery.svelte';
	import UserDataSection from './UserDataSection.svelte';
	import UserDataForm from './UserDataForm.svelte';
	import { DefaultMarker, MapLibre, Marker, Popup } from 'svelte-maplibre';

	if (!$userProfileData) {
		goto('/login');
	}

	let isProfileComplete = $derived(
		Boolean(
			$userProfileData?.gender && $userProfileData?.sexualPreference && $userProfileData?.biography
		)
	);
</script>

<PageWrapper>
	{#if $userProfileData}
		<div class="mb-12">
			<h1>Profile</h1>
			<p>This is the profile page.</p>
		</div>

		<div class="mb-4 flex w-fit flex-col items-start">
			<PhotoGallery photos={$userProfileData.photos} />

			<div class="mb-6 flex w-full items-baseline justify-between">
				<h2>{$userProfileData.username}, {$userProfileData.age}</h2>
				<div class="rounded-xl bg-teal-400 p-3">
					<span class="text-4xl font-bold">{$userProfileData.fameRating}</span>% fame
				</div>
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
				<MapLibre
					center={$userProfileData.location.coordinates}
					class="h-[250px] w-full rounded-md"
					interactive={false}
					maxZoom={15}
					minZoom={5}
					standardControls
					style="https://tiles.basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
					zoom={8}
				>
					<DefaultMarker lngLat={$userProfileData.location.coordinates} />
				</MapLibre>
			</div>
		</div>
	{/if}
</PageWrapper>
