import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { userProfileData } from '$lib/state/user-profile-data.svelte';

export const ssr = false;

export const load: PageLoad = async () => {
	try {
		await userProfileData.fetch();

		if (!userProfileData?.value) {
			throw new Error('Failed to fetch user profile data');
		}
	} catch (error) {
		redirect(302, '/login');
	}
};
