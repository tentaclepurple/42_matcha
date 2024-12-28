<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import PhotoGallery from './PhotoGallery.svelte';
	import UserDataSection from './UserDataSection.svelte';
	import UserDataForm from './UserDataForm.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import FameRating from '$lib/components/FameRating.svelte';
	import Button from '$lib/components/Button.svelte';
	import Location from './Location.svelte';
	import LikesViewsHistory from './LikesViewsHistory.svelte';
	import { userAuth } from '$lib/state/auth.svelte';
	import BlockedUsersList from './BlockedUsersList.svelte';

	if (!userProfileData.value) {
		userAuth.logout();
		goto('/');
	}

	let showWelcomeModal = $state(true);
</script>

<PageWrapper class="relative">
	{#if userProfileData?.value}
		{#if !userProfileData.isProfileComplete && showWelcomeModal}
			<div class="absolute left-0 top-0 z-50 h-full w-full bg-gray-900 opacity-80"></div>
			<div
				class="fixed left-1/2 top-40 z-50 flex max-w-xl -translate-x-1/2 transform flex-col items-center justify-center rounded-md bg-white px-12 py-6 text-center shadow-xl"
			>
				<h1 class="mb-4">Welcome to your new profile!</h1>
				<p class="mb-6">
					Please complete your info and upload some nice pictures before starting your quest for
					love ❤️‍🔥
				</p>
				<Button level="primary" onclick={() => (showWelcomeModal = false)}>Got it!</Button>
			</div>
		{/if}
		<div>
			<div class="mb-12">
				<h1>Profile</h1>
				<p class="max-w-lg">This is where you can update your public profile.</p>
				<p>If you're looking for your account info, click <a href="/account">here</a>.</p>
			</div>

			<div class="m-auto mb-4 flex w-fit flex-col items-start justify-center gap-6">
				<PhotoGallery photos={userProfileData.value.photos} />

				<div class="flex w-full items-baseline justify-between">
					<h2>{userProfileData.value.username}, {userProfileData.value.age}</h2>
					<FameRating fameRating={userProfileData.value.fameRating} />
				</div>

				<div class="flex w-full">
					{#if userProfileData.isProfileComplete}
						<UserDataSection />
					{:else}
						<div
							class="flex w-full flex-col justify-center rounded-lg bg-teal-100 px-6 py-6 sm:px-12"
						>
							<h2 class="mb-6">Complete your profile to find your soulmate</h2>
							<UserDataForm />
						</div>
					{/if}
				</div>

				<LikesViewsHistory />

				<BlockedUsersList />

				<Location />
			</div>
		</div>
	{/if}
</PageWrapper>
