import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { fetchUserProfileData, userProfileData } from '$lib/stores/user-profile-data';
import { get } from 'svelte/store';

export const ssr = false;

export const load: PageLoad = async () => {
	try {
		await fetchUserProfileData();

		const currentUserProfileData = get(userProfileData);

		if (!currentUserProfileData) {
			throw new Error('Failed to fetch user profile data');
		}
	} catch (error: unknown) {
		redirect(302, '/login');
	}
};
