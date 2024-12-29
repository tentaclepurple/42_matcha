import { SERVER_BASE_URL } from '$lib/constants/api';

class PopularTagsClass {
	#value = $state<null | string[]>(null);

	get value(): null | string[] {
		return this.#value;
	}

	fetch = async () => {
		try {
			const accessToken = localStorage.getItem('access_token');

			const res = await fetch(`${SERVER_BASE_URL}/api/tags/popular`, {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${accessToken}`
				}
			});

			if (!res.ok) {
				throw new Error('Failed to fetch user data');
			}

			const { tags } = await res.json();

			this.#value = tags;
		} catch (error: unknown) {
			console.error(error);
			throw new Error('Failed to fetch user data');
		}
	};
}

export const popularTagsData = new PopularTagsClass();
