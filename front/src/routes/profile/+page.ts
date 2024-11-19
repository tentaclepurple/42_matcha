import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { SERVER_BASE_URL } from '$lib/constants/api';

export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {
	const accessToken = localStorage.getItem('access_token');

	if (!accessToken) {
		throw redirect(302, '/');
	}

	const res = await fetch(`${SERVER_BASE_URL}/api/users/my_user_info`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${accessToken}`
		}
	});

	if (!res.ok) {
		throw redirect(302, '/');
	}

	const profileData = await res.json();
	const { email, first_name, last_name, profile_photo, username } = profileData;

	return {
		email,
		firstName: first_name,
		lastName: last_name,
		profilePictureUrl: profile_photo,
		username
	};
};
