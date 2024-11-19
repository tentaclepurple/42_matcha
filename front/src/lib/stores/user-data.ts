import { SERVER_BASE_URL } from '$lib/constants/api';
import type UserData from '$lib/interfaces/user-data.interface';

export async function fetchUserData(): Promise<UserData | undefined> {
	try {
		const accessToken = localStorage.getItem('access_token');

		const res = await fetch(`${SERVER_BASE_URL}/api/users/my_user_info`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		const { email, first_name, last_name, profile_photo, username } = await res.json();

		return {
			email,
			firstName: first_name,
			lastName: last_name,
			profilePhoto: profile_photo,
			username: username
		};
	} catch (error: unknown) {
		if (error instanceof Error) throw new Error('Error fetching user data: ', error);
	}
}
