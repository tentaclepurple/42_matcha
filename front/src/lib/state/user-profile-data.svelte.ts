import { SERVER_BASE_URL } from '$lib/constants/api';
import type UserProfileData from '$lib/interfaces/user-profile-data.interface';
import deserialize from '$lib/utils/deserialize';

class UserProfileDataClass {
	#value = $state<null | UserProfileData>(null);

	get value(): null | UserProfileData {
		return this.#value;
	}

	set value(value: null | UserProfileData) {
		this.#value = value;
	}

	fetch = async (): Promise<void> => {
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

			const data = await response.json();

			const {
				age,
				biography,
				fameRating,
				gender,
				interests,
				location,
				photos,
				sexualPreferences,
				username
			} = deserialize(data);

			this.#value = {
				age,
				biography,
				fameRating,
				gender,
				interests,
				location,
				photos,
				sexualPreferences,
				username
			};
		} catch (error: unknown) {
			console.error(error);
			throw new Error('Failed to fetch user profile data');
		}
	};
}

export const userProfileData = new UserProfileDataClass();
