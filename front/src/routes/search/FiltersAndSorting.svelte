<script lang="ts">
	import ButtonSelector from '$lib/components/ButtonSelector.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import {
		DEFAULT_ALL_RESULTS_SORTING_ORDER,
		DEFAULT_ALL_RESULTS_SORTING_PROP,
		FILTERS_LS_KEY,
		SORTING_LS_KEY
	} from '$lib/constants/sorting';
	import { GENDER_OPTIONS, PREFERENCES_OPTIONS } from '$lib/constants/user-profile-data';
	import { onMount } from 'svelte';
	import RangeFilter from './RangeFilter.svelte';
	import { INTERESTS } from '$lib/constants/interests';
	import { userSearchData } from '$lib/state/user-search.svelte';
	import type { Gender } from '$lib/interfaces/gender.type';

	interface Age {
		age: number;
	}

	interface Distance {
		distance: number;
	}

	const results = userSearchData.value ?? [];

	let currentSorting = $state(
		`${DEFAULT_ALL_RESULTS_SORTING_PROP};${DEFAULT_ALL_RESULTS_SORTING_ORDER}`
	);

	let currentFilters = $state<{
		gender: Gender | null;
		interests: string[];
		minAge: number;
		maxAge: number;
		minDistance: number;
		maxDistance: number;
		minFameRating: number;
		maxFameRating: number;
		sexualPreferences: string | null;
	}>({
		gender: null,
		interests: [],
		minAge:
			results.reduce(
				(acc: number, { age: curr }: Age) => (curr < acc ? curr : acc),
				results[0]?.age
			) ?? 18,
		maxAge:
			results.reduce(
				(acc: number, { age: curr }: Age) => (curr > acc ? curr : acc),
				results[0]?.age
			) ?? 99,
		minDistance:
			results.reduce(
				(acc: number, { distance: curr }: Distance) => (curr < acc ? curr : acc),
				results[0]?.distance
			) ?? 0,
		maxDistance:
			results.reduce(
				(acc: number, { distance: curr }: Distance) => (curr > acc ? curr : acc),
				results[0]?.distance
			) ?? 1_000,
		minFameRating: 0,
		maxFameRating: 100,
		sexualPreferences: null
	});

	$effect(() => {
		if (
			currentSorting ||
			currentFilters.gender ||
			currentFilters.interests ||
			currentFilters.minAge ||
			currentFilters.maxAge ||
			currentFilters.minDistance ||
			currentFilters.maxDistance ||
			currentFilters.sexualPreferences ||
			currentFilters
		) {
			const queryParams = _calcQueryParams();
			userSearchData.fetch({ params: queryParams });
		}
	});

	onMount(async () => {
		const storedSortingCriteria = localStorage?.getItem(SORTING_LS_KEY);

		if (storedSortingCriteria) {
			currentSorting = storedSortingCriteria;
		}

		const storedFiltersCriteria = localStorage?.getItem(FILTERS_LS_KEY);
		if (storedFiltersCriteria) {
			currentFilters = JSON.parse(storedFiltersCriteria);
		}

		const queryParams = _calcQueryParams();
		await userSearchData.fetch({ params: queryParams });
	});

	const _calcQueryParams = (): URLSearchParams => {
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
		if (currentFilters.interests.length) {
			currentFilters.interests.forEach((interest) => queryParams.append('interests', interest));
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

	const handleSortingChange = (event: Event) => {
		const target = event.target as HTMLSelectElement;

		currentSorting = target.value;
		localStorage.setItem(SORTING_LS_KEY, currentSorting);
	};

	const handleFilterChange = (event: Event, prop: 'gender' | 'sexualPreferences') => {
		const target = event.target as HTMLSelectElement;
		const filter = target.value as any;

		currentFilters[prop] = filter.length ? filter : null;
		localStorage.setItem(FILTERS_LS_KEY, JSON.stringify(currentFilters));
	};
</script>

<div class="flex flex-wrap items-center gap-2 px-4">
	<ButtonSelector>
		<label>
			Sort by:
			<select onchange={handleSortingChange} value={currentSorting}>
				<option value="distance;asc"> distance (nearest) </option>
				<option value="distance;desc"> distance (farthest) </option>
				<option value="age;asc">age (youngest)</option>
				<option value="age;desc">age (oldest)</option>
				<option value="fame_rating;asc"> popularity (lowest) </option>
				<option value="fame_rating;desc"> popularity (highest) </option>
			</select>
		</label>
	</ButtonSelector>

	<ButtonSelector>
		<label>
			Gender:
			<select onchange={(e) => handleFilterChange(e, 'gender')} value={currentFilters.gender}>
				<option value={null}>No filter</option>
				<option value={GENDER_OPTIONS.MALE}>
					male <GenderSymbol gender={GENDER_OPTIONS.MALE} />
				</option>
				<option value={GENDER_OPTIONS.FEMALE}>
					female <GenderSymbol gender={GENDER_OPTIONS.FEMALE} />
				</option>
				<option value={GENDER_OPTIONS.OTHER}>
					other <GenderSymbol gender={GENDER_OPTIONS.OTHER} />
				</option>
			</select>
		</label>
	</ButtonSelector>

	<ButtonSelector>
		<label>
			Likes:
			<select
				onchange={(e) => handleFilterChange(e, 'sexualPreferences')}
				value={currentFilters.sexualPreferences}
			>
				<option value={null}>No filter</option>
				<option value={PREFERENCES_OPTIONS.FEMALE}>
					female <PreferenceSymbol preference={PREFERENCES_OPTIONS.FEMALE} />
				</option>
				<option value={PREFERENCES_OPTIONS.MALE}>
					male <PreferenceSymbol preference={PREFERENCES_OPTIONS.MALE} />
				</option>
				<option value={PREFERENCES_OPTIONS.BISEXUAL}>
					both <PreferenceSymbol preference={PREFERENCES_OPTIONS.BISEXUAL} />
				</option>
			</select>
		</label>
	</ButtonSelector>

	<ButtonSelector>
		<RangeFilter
			label="Age"
			minValue={currentFilters.minAge}
			maxValue={currentFilters.maxAge}
			min="18"
			max="99"
			step="1"
			onChangeMin={(value: number) => (currentFilters.minAge = value)}
			onChangeMax={(value: number) => (currentFilters.maxAge = value)}
		/>
	</ButtonSelector>

	<ButtonSelector>
		<RangeFilter
			label="Distance"
			minValue={currentFilters.minDistance}
			maxValue={currentFilters.maxDistance}
			min="0"
			max="2000"
			step="10"
			onChangeMax={(value: number) => (currentFilters.maxDistance = value)}
		/>
	</ButtonSelector>

	<ButtonSelector>
		<RangeFilter
			label="Popularity"
			minValue={currentFilters.minFameRating}
			maxValue={currentFilters.maxFameRating}
			min="0"
			max="100"
			step="1"
			onChangeMin={(value: number) => (currentFilters.minFameRating = value)}
			onChangeMax={(value: number) => (currentFilters.maxFameRating = value)}
		/>
	</ButtonSelector>

	<ButtonSelector>
		<div class="flex gap-1">
			<span>Interests:</span>
			<ul class="flex flex-wrap items-baseline gap-2">
				{#each [...INTERESTS].sort() as interest}
					<li
						class={`text-2xs shrink-0 rounded-md ${currentFilters.interests.includes(interest) ? 'bg-teal-300' : 'bg-slate-300'} px-2 py-1`}
					>
						<button
							onclick={() => {
								if (currentFilters.interests.includes(interest)) {
									currentFilters.interests = currentFilters.interests.filter(
										(currentInterest) => currentInterest !== interest
									);
								} else {
									currentFilters.interests = [...currentFilters.interests, interest];
								}
							}}
						>
							#{interest.toLowerCase()}
						</button>
					</li>
				{/each}
			</ul>
		</div>
	</ButtonSelector>
</div>
