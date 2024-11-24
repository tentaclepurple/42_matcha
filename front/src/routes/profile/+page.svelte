<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userProfileData } from '$lib/stores/user-profile-data';
	import PhotoGallery from './PhotoGallery.svelte';
	import MissingDataForm from './MissingDataForm.svelte';
	import { writable } from 'svelte/store';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import { GENDER_OPTIONS, PREFERENCES_OPTIONS } from '$lib/constants/user-profile-data';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';

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

	const getGenderIcon = (userProfileData: UserProfileData): string => {
		switch (userProfileData.gender) {
			case GENDER_OPTIONS.MALE:
				return 'icons/gender/male.svg';
			case GENDER_OPTIONS.FEMALE:
				return 'icons/gender/female.svg';
			case GENDER_OPTIONS.OTHER:
			default:
				return 'icons/gender/male-female.svg';
		}
	};

	const getPreferencesIcon = (userProfileData: UserProfileData): string => {
		switch (userProfileData.sexualPreference) {
			case PREFERENCES_OPTIONS.MALE:
				return 'icons/gender/male.svg';
			case PREFERENCES_OPTIONS.FEMALE:
				return 'icons/gender/female.svg';
			case PREFERENCES_OPTIONS.BISEXUAL:
			default:
				return 'icons/gender/male-female.svg';
		}
	};
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
							<dd class="max-w-xl">{$userProfileData.biography}</dd>
						</div>

						<div class="flex items-baseline gap-2">
							<dt class="font-bold">Gender:</dt>
							<dd class="flex items-center gap-1">
								{$userProfileData.gender}
								<img src={getGenderIcon($userProfileData)} alt="" class="w-5" />
							</dd>
						</div>

						<div class="flex items-baseline gap-2">
							<dt class="font-bold">Interested in:</dt>
							<dd class="flex items-center gap-1">
								{$userProfileData.sexualPreference}
								<img src={getPreferencesIcon($userProfileData)} alt="" class="w-5" />
							</dd>
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
