import { SERVER_BASE_URL } from '$lib/constants/api';
import { DEFAULT_AVATAR_NAME } from '$lib/constants/avatar';
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

	get isProfileComplete() {
		if (!this.#value) return false;

		return Boolean(this.#value.gender && this.#value.sexualPreferences && this.#value.biography);
	}

	get hasProfilePicture() {
		if (!this.#value) return false;

		const profilePicture = this.#value.photos.find((photo) => photo.isProfile);
		const isDefaultPicture = profilePicture?.url.includes(DEFAULT_AVATAR_NAME);

		return !isDefaultPicture;
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
				likesReceived,
				photos,
				profileViews,
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
				likesReceived,
				photos,
				profileViews,
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
