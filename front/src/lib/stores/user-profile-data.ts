import { SERVER_BASE_URL } from '$lib/constants/api';
import type UserProfileData from '$lib/interfaces/user-profile-data.interface';
import { writable, type Writable } from 'svelte/store';

export const userProfileData: Writable<UserProfileData | null> = writable(null);

export async function fetchUserProfileData(): Promise<void> {
	try {
		const accessToken = localStorage.getItem('access_token');

		const response = await fetch(`${SERVER_BASE_URL}/api/profile/my_profile_info`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		if (!response.ok) {
			throw new Error('Failed to fetch user profile data');
		}

		const { age, biography, fame_rating, gender, location, photos, sexual_preferences, username } =
			await response.json();

		userProfileData.set({
			age,
			biography,
			fameRating: fame_rating,
			gender,
			location,
			photos,
			sexualPreference: sexual_preferences,
			username
		});
	} catch (error: unknown) {
		console.error(error);
		throw new Error('Failed to fetch user profile data');
	}
}
