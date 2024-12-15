import { error, redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { SERVER_BASE_URL } from '$lib/constants/api';
import {
	DEFAULT_ALL_RESULTS_SORTING_ORDER,
	DEFAULT_ALL_RESULTS_SORTING_PROP,
	SORTING_ORDER
} from '$lib/constants/filters';

export const ssr = false;

export const load: PageLoad = async () => {
	const token = localStorage.getItem('access_token');

	if (!token) {
		return redirect(302, '/login');
	}

	const searchRes = await fetch(`${SERVER_BASE_URL}/api/match/search`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	if (!searchRes.ok) {
		return error(searchRes.status, 'An error occurred while fetching search results');
	}

	const { results: searchResults } = await searchRes.json();
	const sortedSearchResults = searchResults.sort((a, b) => {
		if (!a[DEFAULT_ALL_RESULTS_SORTING_PROP] || !b[DEFAULT_ALL_RESULTS_SORTING_PROP]) {
			return 0;
		}

		if (DEFAULT_ALL_RESULTS_SORTING_ORDER === SORTING_ORDER.ASC) {
			return a[DEFAULT_ALL_RESULTS_SORTING_PROP] - b[DEFAULT_ALL_RESULTS_SORTING_PROP];
		} else if (DEFAULT_ALL_RESULTS_SORTING_ORDER === SORTING_ORDER.DESC) {
			return b[DEFAULT_ALL_RESULTS_SORTING_PROP] - a[DEFAULT_ALL_RESULTS_SORTING_PROP];
		}

		return 0;
	});

	const queryParams = new URLSearchParams({
		max_distance: '10'
	}).toString();

	const suggestionsRes = await fetch(`${SERVER_BASE_URL}/api/match/suggestions?${queryParams}`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${token}`
		}
	});

	if (!suggestionsRes.ok) {
		return error(suggestionsRes.status, 'An error occurred while fetching suggestions results');
	}

	const { matches: suggestionsResults } = await suggestionsRes.json();
	const sortedSuggestionsResults = suggestionsResults.sort((a, b) => {
		return a.distance - b.distance;
	});

	return {
		searchResults: sortedSearchResults,
		suggestionsResults: sortedSuggestionsResults
	};
};
