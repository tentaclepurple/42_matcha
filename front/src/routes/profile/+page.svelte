<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userProfileData } from '$lib/stores/user-profile-data';
	import PhotoGallery from './PhotoGallery.svelte';
	import MissingDataForm from './MissingDataForm.svelte';
	import { writable } from 'svelte/store';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';

	if (!$userProfileData) {
		goto('/login');
	}

	let isProfileComplete = $derived(
		Boolean(
			$userProfileData?.gender && $userProfileData?.sexualPreference && $userProfileData?.biography
		)
	);

	const success = writable('');
	success.subscribe((value) => {
		if (value) {
			setTimeout(() => {
				success.set('');
			}, DEFAULT_TIMEOUT);
		}
	});
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
				<div>
					<dl class="flex flex-col gap-3">
						<div>
							<dt class="font-bold">About me</dt>
							<dd>{$userProfileData.biography}</dd>
						</div>

						<div class="flex items-baseline gap-2">
							<dt class="font-bold">Gender:</dt>
							<dd>{$userProfileData.gender}</dd>
						</div>

						<div class="flex items-baseline gap-2">
							<dt class="font-bold">Interested in:</dt>
							<dd>{$userProfileData.sexualPreference}</dd>
						</div>
					</dl>
				</div>
			{:else}
				<MissingDataForm successMessage={success} />
			{/if}
			{#if $success}
				<p class="text-green-500">{$success}</p>
			{/if}
		</div>
	{/if}
</PageWrapper>
