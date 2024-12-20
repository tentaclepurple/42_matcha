import { goto } from '$app/navigation';
import { SERVER_BASE_URL } from '$lib/constants/api';
import {
	DEFAULT_ALL_RESULTS_SORTING_ORDER,
	DEFAULT_ALL_RESULTS_SORTING_PROP
} from '$lib/constants/sorting';
import type UserFromList from '$lib/interfaces/user-from-list.interface';
import deserialize from '$lib/utils/deserialize';

class UserSearchClass {
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
			goto('/login');
		}

		const defaultParams = new URLSearchParams({
			sort_by: DEFAULT_ALL_RESULTS_SORTING_PROP,
			sort_order: DEFAULT_ALL_RESULTS_SORTING_ORDER
		});

		const searchRes = await fetch(
			`${SERVER_BASE_URL}/api/match/search?${params ? params : defaultParams}`,
			{
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			}
		);

		if (!searchRes.ok) {
			throw new Error('An error occurred while fetching search results');
		}

		const { results: searchResults } = await searchRes.json();

		const deserializedSearchResults: UserFromList[] = searchResults.map((result: UserFromList) =>
			deserialize(result)
		);

		this.value = deserializedSearchResults;
	};
}

export const userSearchData = new UserSearchClass();
