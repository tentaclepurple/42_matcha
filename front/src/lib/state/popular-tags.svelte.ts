import { SERVER_BASE_URL } from '$lib/constants/api';

export interface PopularTag {
	count: number;
	name: string;
}

class PopularTagsClass {
	#value = $state<null | PopularTag[]>(null);

	get value(): null | PopularTag[] {
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

			const sortedTags = tags.sort((a: PopularTag, b: PopularTag) => {
				if (a.count === b.count) {
					return a.name.localeCompare(b.name);
				}

				return b.count - a.count;
			});

			this.#value = sortedTags;
		} catch (error: unknown) {
			console.error(error);
			throw new Error('Failed to fetch user data');
		}
	};
}

export const popularTagsData = new PopularTagsClass();
