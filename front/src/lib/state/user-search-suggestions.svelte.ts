import { goto } from '$app/navigation';
import { SERVER_BASE_URL } from '$lib/constants/api';
import {
	DEFAULT_ALL_RESULTS_SORTING_ORDER,
	DEFAULT_ALL_RESULTS_SORTING_PROP
} from '$lib/constants/sorting';
import type UserFromList from '$lib/interfaces/user-from-list.interface';
import deserialize from '$lib/utils/deserialize';
import { userAuth } from './auth.svelte';

class UserSearchSuggestionsClass {
	#value = $state<null | UserFromList[]>(null);

	get value(): null | UserFromList[] {
		return this.#value;
	}

	set value(value: null | UserFromList[]) {
		this.#value = value;
	}

	fetch = async ({ params }: { params?: URLSearchParams }) => {
		const token = localStorage.getItem('access_token');

		if (!token) {
			userAuth.logout();
			goto('/login');
		}

		const defaultParams = new URLSearchParams({
			sort_by: DEFAULT_ALL_RESULTS_SORTING_PROP,
			sort_order: DEFAULT_ALL_RESULTS_SORTING_ORDER
		});

		const suggestionsRes = await fetch(
			`${SERVER_BASE_URL}/api/match/suggestions?${params ? params : defaultParams}`,
			{
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			}
		);

		if (!suggestionsRes.ok) {
			throw new Error('An error occurred while fetching search results');
		}

		const { matches: searchSuggestionsResults } = await suggestionsRes.json();

		const deserializedSuggestionsResults: UserFromList[] = searchSuggestionsResults.map(
			(result: UserFromList) => deserialize(result)
		);

		this.value = deserializedSuggestionsResults;
	};
}

export const userSearchSuggestionsData = new UserSearchSuggestionsClass();
