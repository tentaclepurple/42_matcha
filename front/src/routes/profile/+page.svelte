<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userProfileData } from '$lib/stores/user-profile-data';
	import PhotoGallery from './PhotoGallery.svelte';
	import UserDataSection from './UserDataSection.svelte';
	import UserDataForm from './UserDataForm.svelte';

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

			<h2 class="mb-6">{$userProfileData.username}, {$userProfileData.age}</h2>
			{#if isProfileComplete}
				<UserDataSection />
			{:else}
				<div class="flex flex-col justify-center rounded-lg bg-teal-100 px-12 py-6">
					<h2 class="mb-6">Complete your profile to find your soulmate</h2>
					<UserDataForm />
				</div>
			{/if}
		</div>
	{/if}
</PageWrapper>
