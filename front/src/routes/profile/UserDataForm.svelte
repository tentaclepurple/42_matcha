<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { GENDER_OPTIONS, PREFERENCES_OPTIONS } from '$lib/constants/user-profile-data';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import { INTERESTS } from '$lib/constants/interests';
	import serialize from '$lib/utils/serialize';
	import InterestsList from '$lib/components/InterestsList.svelte';
	import { popularTagsData } from '$lib/state/popular-tags.svelte';

	const MAX_INTERESTS = 10;

	const userGender = userProfileData.value ? userProfileData.value.gender : null;
	const userSexualPreferences = userProfileData.value
		? userProfileData.value.sexualPreferences
		: null;
	const userInterests = userProfileData.value ? userProfileData.value.interests : [];
	const userBio = userProfileData.value ? userProfileData.value.biography : '';

	const {
		onSuccess = undefined,
		onCancel = undefined
	}: {
		onSuccess?: () => void;
		onCancel?: () => void;
	} = $props();

	let success: string = $state('');
	$effect(() => {
		if (success) {
			const timeout = setTimeout(() => {
				success = '';
			}, DEFAULT_TIMEOUT);

			return () => {
				clearTimeout(timeout);
			};
		}
	});

	let error: string = $state('');
	let errorTimeoutId: null | number = $state(null);
	$effect(() => {
		if (error) {
			const timeout = setTimeout(() => {
				error = '';
			}, DEFAULT_TIMEOUT);
			errorTimeoutId = timeout;
		}

		return () => {
			if (errorTimeoutId) {
				clearTimeout(errorTimeoutId);
			}
		};
	});

	let textAreaLength = $state(0);
	const handleTextareaUpdate = (event: Event) => {
		const textArea = event.target as HTMLTextAreaElement;
		textAreaLength = textArea.value.length;
	};

	let interestsList = $state<string[]>(userInterests.length ? userInterests : []);

	const handleInterestsUpdate = (event: Event) => {
		const select = event.target as HTMLSelectElement;
		const newInterests = Array.from(select.selectedOptions)
			.map((option) => option.value)
			.sort();

		if (newInterests.length > MAX_INTERESTS) {
			interestsList = newInterests.slice(0, MAX_INTERESTS);
			error = 'You can only select up to 10 interests';
			return;
		}

		interestsList = newInterests;
	};

	const handleFormSubmit = async (event: Event) => {
		event.preventDefault();
		error = '';
		success = '';

		try {
			const token = localStorage.getItem('access_token');
			const form = event.target as HTMLFormElement;
			const formData = new FormData(form);

			const gender = formData.get('gender') as string;

			if (!gender) {
				error = 'Please provide your gender';
				return;
			}

			const sexualPreferences = formData.get('sexualPreferences') as string;
			if (!sexualPreferences) {
				error = 'Please provide your sexual preferences';
				return;
			}

			const bio = formData.get('biography') as string;
			if (!bio.length) {
				error = 'Please provide a bio';
				return;
			}

			const payload = Object.fromEntries(formData);
			const serializedPayload = serialize(payload);

			const res = await fetch(`${SERVER_BASE_URL}/api/profile/update_profile`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ ...serializedPayload, interests: interestsList })
			});

			if (!res.ok) {
				error = 'An error occurred. Please try again later.';
				return;
			}

			success = 'Profile updated successfully';

			await userProfileData.fetch();
			onSuccess?.();
		} catch (e) {
			console.error(e);
			error = 'An error occurred. Please try again later.';
		}
	};
</script>

<form onsubmit={handleFormSubmit}>
	<fieldset class="mb-6 flex min-w-[500px] flex-col gap-6">
		<label class="flex justify-between gap-2">
			<span class="font-bold">Gender:</span>
			<select name="gender" id="gender" value={userGender}>
				<option value={null} disabled selected>Choose an option</option>
				<option value={GENDER_OPTIONS.MALE}>
					{GENDER_OPTIONS.MALE}
					<GenderSymbol gender={GENDER_OPTIONS.MALE} />
				</option>
				<option value={GENDER_OPTIONS.FEMALE}>
					{GENDER_OPTIONS.FEMALE}
					<GenderSymbol gender={GENDER_OPTIONS.FEMALE} />
				</option>
				<option value={GENDER_OPTIONS.OTHER}>
					{GENDER_OPTIONS.OTHER}
					<GenderSymbol gender={GENDER_OPTIONS.OTHER} />
				</option>
			</select>
		</label>

		<label class="flex justify-between gap-2">
			<span class="font-bold">Preference:</span>
			<select
				name="sexualPreferences"
				id="sexualPreferences"
				value={userSexualPreferences ?? PREFERENCES_OPTIONS.BISEXUAL}
			>
				<option value={PREFERENCES_OPTIONS.MALE}>
					{PREFERENCES_OPTIONS.MALE}
					<PreferenceSymbol preference={PREFERENCES_OPTIONS.MALE} />
				</option>
				<option value={PREFERENCES_OPTIONS.FEMALE}>
					{PREFERENCES_OPTIONS.FEMALE}
					<PreferenceSymbol preference={PREFERENCES_OPTIONS.FEMALE} />
				</option>
				<option value={PREFERENCES_OPTIONS.BISEXUAL}>
					{PREFERENCES_OPTIONS.BISEXUAL}
					<PreferenceSymbol preference={PREFERENCES_OPTIONS.BISEXUAL} />
				</option>
			</select>
		</label>

		<label class="flex justify-between gap-2">
			<span class="font-bold">Interests:</span>
			<select
				name="interests"
				id="interests"
				multiple
				class="min-h-[150px] min-w-[150px] text-right text-sm"
				onchange={handleInterestsUpdate}
				value={interestsList}
			>
				{#if popularTagsData.value && popularTagsData.value.length > 0}
					<optgroup label="Popular interests" class="text-left font-bold mb-3">
						{#each popularTagsData.value as interest}
							<option value={interest} class="text-right text-sm">#{interest}</option>
						{/each}
					</optgroup>
				{/if}
				<optgroup label="All interests" class="text-left font-bold">
					{#each INTERESTS.sort() as interest}
						<option value={interest} class="text-right text-sm">#{interest}</option>
					{/each}
				</optgroup>
			</select>
		</label>
		{#if interestsList.length > 0}
			<InterestsList
				interests={interestsList}
				class="flex max-w-[500px] flex-wrap items-baseline gap-1"
			/>
		{/if}

		<label class="flex justify-between gap-2">
			<span class="font-bold">Bio:</span>
			<div class="flex w-2/3 flex-col items-end">
				<textarea
					id="biography"
					name="biography"
					placeholder="Tell us more about yourself"
					class="mb-1 w-full text-sm"
					required
					rows="4"
					minlength="1"
					maxlength="500"
					oninput={handleTextareaUpdate}
					value={userBio}
				></textarea>
				<p class="flex w-full items-baseline justify-between gap-6 text-xs text-gray-500">
					Describe yourself in less than 500 characters
					<span>
						{textAreaLength}/500
					</span>
				</p>
			</div>
		</label>
	</fieldset>

	<div class="flex w-full items-baseline justify-between gap-6">
		{#if success}
			<p class="text-green-500">{success}</p>
		{:else if error}
			<p class="mt-4 text-red-500">{error}</p>
		{/if}

		<div class="ml-auto flex w-fit items-baseline justify-between gap-2">
			{#if onCancel}
				<Button type="button" level="secondary" onclick={onCancel}>Cancel</Button>
			{/if}
			<Button type="submit" level="primary">Save</Button>
		</div>
	</div>
</form>
