import { SERVER_BASE_URL } from '$lib/constants/api';
import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {
	const token = localStorage.getItem('access_token');
	if (!token) {
		redirect(302, '/login');
	}

	const response = await fetch(`${SERVER_BASE_URL}/api/profile/my_profile_info`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	if (!response.ok) {
		redirect(302, '/login');
	}

	const profileData = await response.json();

	return {
		profileData: {
			username: profileData.username,
			photos: profileData.photos
		}
	};
};
