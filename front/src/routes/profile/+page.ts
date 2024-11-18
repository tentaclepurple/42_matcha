import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { isAuthenticated } from '$lib/stores/auth';
import { get } from 'svelte/store';

export const ssr = false;

export const load: PageLoad = async () => {
	if (!get(isAuthenticated)) {
		throw redirect(302, '/');
	}
	return {};
};
