import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { fetchUserData } from '$lib/stores/user-data';

export const ssr = false;

export const load: PageLoad = async () => {
	try {
		const res = await fetchUserData();

		if (!res) {
			throw new Error('Error fetching user data');
		}

		const { email, firstName, lastName, profilePhoto, username } = res;

		return {
			email,
			firstName,
			lastName,
			profilePictureUrl: profilePhoto,
			username
		};
	} catch (e: unknown) {
		console.error('Error fetching user data: ', e);
		throw redirect(302, '/');
	}
};
