import type { Gender } from '$lib/interfaces/gender.type';

export interface CurrentFilters {
	gender?: Gender | null;
	interests?: string[];
	maxAge?: number;
	maxDistance?: number;
	maxFameRating?: number;
	minAge?: number;
	minDistance?: number;
	minFameRating?: number;
	sexualPreferences?: string | null;
}

export const calcQueryParams = ({
	currentSorting,
	currentFilters
}: {
	currentSorting: string;
	currentFilters: CurrentFilters;
}): URLSearchParams => {
	const queryParams = new URLSearchParams();

	const sortingProp = currentSorting.split(';')[0];
	const sortingOrder = currentSorting.split(';')[1];
	queryParams.set('sort_by', sortingProp);
	queryParams.set('sort_order', sortingOrder);

	// FILTERS
	// Gender
	if (currentFilters.gender) {
		queryParams.set('gender', currentFilters.gender);
	}

	// Interests
	if (currentFilters.interests?.length) {
		currentFilters.interests.forEach((interest) =>
			queryParams.append('interests', interest.toLowerCase())
		);
	}

	// Sexual preference
	if (currentFilters.sexualPreferences) {
		queryParams.set('sexual_preference', currentFilters.sexualPreferences);
	}

	// Min age
	if (currentFilters.minAge) {
		queryParams.set('min_age', currentFilters.minAge.toString());
	}

	// Max age
	if (currentFilters.maxAge) {
		queryParams.set('max_age', currentFilters.maxAge.toString());
	}

	// Max distance
	if (currentFilters.maxDistance) {
		queryParams.set('max_distance', currentFilters.maxDistance.toString());
	}

	// Min popularity
	if (currentFilters.minFameRating) {
		queryParams.set('min_fame', currentFilters.minFameRating.toString());
	}

	// Max popularity
	if (currentFilters.maxFameRating) {
		queryParams.set('max_fame', currentFilters.maxFameRating.toString());
	}

	return queryParams;
};
