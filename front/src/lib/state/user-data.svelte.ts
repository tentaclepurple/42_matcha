import { SERVER_BASE_URL } from '$lib/constants/api';
import type UserData from '$lib/interfaces/user-data.interface';

class UserDataClass {
	#value = $state<null | UserData>(null);

	get value(): null | UserData {
		return this.#value;
	}

	fetch = async () => {
		try {
			const accessToken = localStorage.getItem('access_token');

			const res = await fetch(`${SERVER_BASE_URL}/api/users/my_user_info`, {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${accessToken}`
				}
			});

			if (!res.ok) {
				throw new Error('Failed to fetch user data');
			}

			const { email, first_name, last_name, profile_photo, username } = await res.json();

			this.#value = {
				email,
				firstName: first_name,
				lastName: last_name,
				profilePhoto: profile_photo,
				username: username
			};
		} catch (error: unknown) {
			console.error(error);
			throw new Error('Failed to fetch user data');
		}
	};
}

export const userData = new UserDataClass();
