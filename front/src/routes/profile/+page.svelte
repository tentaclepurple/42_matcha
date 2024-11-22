<script lang="ts">
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';
	import PhotoGallery from './PhotoGallery.svelte';

	let {
		data
	}: {
		data: {
			profileData: UserProfileData;
		};
	} = $props();

	const avatarUrl = data.profileData.photos.filter((photo) => photo.is_profile)[0]?.url;
	const photos = data.profileData.photos.filter((photo) => !photo.is_profile);
</script>

<PageWrapper>
	<div class="mb-12">
		<h1>Profile</h1>
		<p>This is the profile page.</p>
	</div>

	<div class="mb-4 flex w-fit flex-col items-start">
		<PhotoGallery {avatarUrl} {photos} />
		<div class="flex w-56 items-baseline justify-between">
			<p class="text-3xl">{data.profileData.username}</p>
			<p class="text-2xl">{data.profileData.age}</p>
		</div>
	</div>
</PageWrapper>
