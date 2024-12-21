import { error, redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { SERVER_BASE_URL } from '$lib/constants/api';
import deserialize from '$lib/utils/deserialize';
import type UserFromSuggestion from '$lib/interfaces/user-from-suggestion.interface';
import { userSearchData } from '$lib/state/user-search.svelte';

export const ssr = false;

export const load: PageLoad = async () => {
	try {
		await userSearchData.fetch({});
	} catch (error) {
		console.error(error);
	}
	const token = localStorage.getItem('access_token');

	if (!token) {
		return redirect(302, '/login');
	}

	const suggestionsRes = await fetch(`${SERVER_BASE_URL}/api/match/suggestions`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	if (!suggestionsRes.ok) {
		return error(suggestionsRes.status, 'An error occurred while fetching suggestions results');
	}

	const { matches: suggestionsResults } = await suggestionsRes.json();
	const deserializedSuggestionsResults: UserFromSuggestion[] = suggestionsResults.map(
		(result: UserFromSuggestion) => deserialize(result)
	);
	const sortedSuggestionsResults = deserializedSuggestionsResults.sort((a, b) => {
		return a.distance - b.distance;
	});

	return {
		suggestionsResults: sortedSuggestionsResults
	};
};
