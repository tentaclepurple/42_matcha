<script lang="ts">
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { fetchUserProfileData } from '$lib/stores/user-profile-data';
	import { writable } from 'svelte/store';
	import { DEFAULT_TIMEOUT } from '$lib/constants/timeout';
	import { GENDER_OPTIONS, PREFERENCES_OPTIONS } from '$lib/constants/user-profile-data';
	import Button from '$lib/components/Button.svelte';

	export let successMessage;

	const error = writable('');

	$: errorTimeoutId = null as number | null;
	error.subscribe((value) => {
		if (errorTimeoutId) {
			clearTimeout(errorTimeoutId);
		}

		if (value) {
			const timeoutId = setTimeout(() => {
				error.set('');
				errorTimeoutId = null;
			}, DEFAULT_TIMEOUT);
			errorTimeoutId = timeoutId;
		}
	});

	$: textAreaLength = 0;
	const handleTextareaUpdate = (event: Event) => {
		const textArea = event.target as HTMLTextAreaElement;
		textAreaLength = textArea.value.length;
	};

	const handleFormSubmit = async (event: Event) => {
		event.preventDefault();
		error.set('');
		successMessage.set('');

		try {
			const token = localStorage.getItem('access_token');
			const form = event.target as HTMLFormElement;
			const formData = new FormData(form);

			const gender = formData.get('gender') as string;

			if (!gender) {
				error.set('Please provide your gender');
				return;
			}

			const sexualPreferences = formData.get('sexual_preferences') as string;
			if (!sexualPreferences) {
				error.set('Please provide your dating preferences');
				return;
			}

			const bio = formData.get('biography') as string;
			if (!bio.length) {
				error.set('Please provide a bio');
				return;
			}

			const payload = Object.fromEntries(formData);

			const res = await fetch(`${SERVER_BASE_URL}/api/profile/update_profile`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ ...payload, interests: [] }) // TODO add logic for interests
			});

			if (!res.ok) {
				error.set('There was an error updating your profile.');
				return;
			}

			successMessage.set('Profile updated successfully');

			await fetchUserProfileData();
		} catch (e) {
			console.error(e);
			error.set('There was an error updating your profile.');
		}
	};
</script>

<div class="flex flex-col justify-center rounded-lg bg-teal-100 px-12 py-6">
	<h2 class="mb-6">Complete your profile to find your soulmate</h2>
	<form onsubmit={handleFormSubmit}>
		<fieldset class="mb-8 flex flex-col gap-5">
			<label class="flex justify-between gap-2">
				<span class="font-bold">Gender:</span>
				<select name="gender" id="gender">
					<option value={null} disabled selected>Choose an option</option>
					<option value={GENDER_OPTIONS.MALE}>Male</option>
					<option value={GENDER_OPTIONS.FEMALE}>Female</option>
					<option value={GENDER_OPTIONS.OTHER}>Other</option>
				</select>
			</label>

			<label class="flex justify-between gap-2">
				<span class="font-bold">Interested in:</span>
				<select name="sexual_preferences" id="sexual_preferences">
					<option value={null} disabled selected>Choose an option</option>
					<option value={PREFERENCES_OPTIONS.MALE}>Boys</option>
					<option value={PREFERENCES_OPTIONS.FEMALE}>Girls</option>
					<option value={PREFERENCES_OPTIONS.BISEXUAL}>Both</option>
				</select>
			</label>

			<label class="flex justify-between gap-2">
				<span class="font-bold">Bio:</span>
				<div class="flex w-2/3 flex-col items-end">
					<textarea
						id="biography"
						name="biography"
						placeholder="Tell us more about yourself"
						class="mb-1 w-full"
						required
						minlength="1"
						maxlength="500"
						oninput={handleTextareaUpdate}
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

		<Button type="submit" level="primary">Save</Button>
	</form>
	{#if $error}
		<p class="mt-4 text-red-500">{$error}</p>
	{/if}
</div>
