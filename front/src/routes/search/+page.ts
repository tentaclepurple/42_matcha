import type { PageLoad } from './$types';
import { userSearchData } from '$lib/state/user-search.svelte';
import { userSearchSuggestionsData } from '$lib/state/user-search-suggestions.svelte';

export const ssr = false;

export const load: PageLoad = async () => {
	try {
		await userSearchData.fetch({});
		await userSearchSuggestionsData.fetch({});
	} catch (error) {
		console.error(error);
	}
};
