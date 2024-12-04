import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { SERVER_BASE_URL } from '$lib/constants/api';

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
		return redirect(302, '/login');
	}

	const { results: searchResults } = await searchRes.json();
	const sortedSearchResults = searchResults.sort((a, b) => {
		return a.distance - b.distance;
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
		return redirect(302, '/login');
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
