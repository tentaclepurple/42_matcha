<script lang="ts">
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userProfileData } from '$lib/stores/user-profile-data';
	import PhotoGallery from './PhotoGallery.svelte';

	const currentProfileData = $userProfileData;

	const avatarUrl = $derived(
		$userProfileData?.photos.filter((photo) => photo.is_profile)[0]?.url ?? ''
	);
	const photos = $derived($userProfileData?.photos.filter((photo) => !photo.is_profile) ?? []);
</script>

<PageWrapper>
	<div class="mb-12">
		<h1>Profile</h1>
		<p>This is the profile page.</p>
	</div>

	<div class="mb-4 flex w-fit flex-col items-start">
		<PhotoGallery {avatarUrl} {photos} />
		<div class="flex w-56 items-baseline justify-between">
			<p class="text-3xl">{currentProfileData?.username}</p>
			<p class="text-2xl">{currentProfileData?.age}</p>
		</div>
	</div>
</PageWrapper>
