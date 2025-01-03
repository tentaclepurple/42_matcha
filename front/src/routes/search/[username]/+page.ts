import { error } from '@sveltejs/kit';
import type { PageLoad } from '../$types';
import { visitedProfileData } from '$lib/state/visited-profile-data.svelte';

export const ssr = false;

export const load: PageLoad = async ({ params }) => {
	const username = params.username;

	if (!username) {
		error(404, 'User not found');
	}

	try {
		await visitedProfileData.fetch(username);
	} catch (err) {
		error(500, err.message);
	}
};
