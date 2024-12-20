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
	import Button from '$lib/components/Button.svelte';

	const { data } = $props();

	if (!userProfileData.value) {
		goto('/login');
	}

	let showWelcomeModal = $state(data.isNewUser);

	let isProfileComplete = $derived(
		Boolean(
			userProfileData?.value?.gender &&
				userProfileData?.value?.sexualPreferences &&
				userProfileData?.value?.biography
		)
	);
</script>

<PageWrapper class="relative">
	{#if userProfileData?.value}
		{#if showWelcomeModal}
			<div class="absolute left-0 top-0 z-50 h-full w-full bg-gray-900 opacity-80"></div>
			<div
				class="max-w-xl text-center absolute left-1/2 top-40 z-50 flex -translate-x-1/2 transform flex-col items-center justify-center rounded-md bg-white px-12 py-6 shadow-xl"
			>
				<h1 class="mb-4">Welcome to your new profile!</h1>
				<p class="mb-6">
					Please complete your info and upload some nice picture before starting your quest for
					love.
				</p>
				<Button level="primary" onclick={() => (showWelcomeModal = false)}>Got it!</Button>
			</div>
		{/if}
		<div aria-hidden={showWelcomeModal}>
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
		</div>
	{/if}
</PageWrapper>
