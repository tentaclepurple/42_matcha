import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { userProfileData } from '$lib/state/user-profile-data.svelte';
import { userAuth } from '$lib/state/auth.svelte';
import { popularTagsData } from '$lib/state/popular-tags.svelte';

export const ssr = false;

export const load: PageLoad = async () => {
	try {
		await userProfileData.fetch();
		await popularTagsData.fetch();

		if (!userProfileData?.value) {
			throw new Error('Failed to fetch user profile data');
		}
	} catch (error) {
		userAuth.logout();
		redirect(302, '/login');
	}
};
