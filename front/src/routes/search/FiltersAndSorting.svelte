<script lang="ts">
	import ButtonSelector from '$lib/components/ButtonSelector.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import {
		DEFAULT_ALL_RESULTS_SORTING_ORDER,
		DEFAULT_ALL_RESULTS_SORTING_PROP,
		FILTERS_LS_KEY,
		SORTING_LS_KEY,
		SORTING_ORDER
	} from '$lib/constants/sorting';
	import { GENDER_OPTIONS, PREFERENCES_OPTIONS } from '$lib/constants/user-profile-data';
	import { onMount } from 'svelte';

	interface Age {
		age: number;
	}

	interface Distance {
		distance: number;
	}

	const { results, setResults, unfilteredResults } = $props();

	let currentSorting = $state(
		`${DEFAULT_ALL_RESULTS_SORTING_PROP};${DEFAULT_ALL_RESULTS_SORTING_ORDER}`
	);

	let currentFilters = $state<{
		gender: string | null;
		minAge: number;
		maxAge: number;
		minDistance: number;
		maxDistance: number;
		sexualPreferences: string | null;
	}>({
		gender: null,
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
		sexualPreferences: null
	});

	$effect(() => {
		if (
			currentSorting ||
			currentFilters.gender ||
			currentFilters.minAge ||
			currentFilters.maxAge ||
			currentFilters.minDistance ||
			currentFilters.maxDistance ||
			currentFilters.sexualPreferences ||
			currentFilters
		) {
			const newResults = _sortAndFilterResults(unfilteredResults);
			setResults(newResults);
		}
	});

	onMount(() => {
		const storedSortingCriteria = localStorage?.getItem(SORTING_LS_KEY);

		if (storedSortingCriteria) {
			currentSorting = storedSortingCriteria;
		}

		const storedFiltersCriteria = localStorage?.getItem(FILTERS_LS_KEY);
		if (storedFiltersCriteria) {
			currentFilters = JSON.parse(storedFiltersCriteria);
		}

		const newResults = _sortAndFilterResults(unfilteredResults);
		setResults(newResults);
	});

	const _sortAndFilterResults = (results) => {
		// Sorting
		let sortedResults = [...results].sort((a, b) => {
			const [prop, order] = currentSorting.split(';');
			if (order === SORTING_ORDER.ASC) {
				return a[prop] - b[prop];
			} else {
				return b[prop] - a[prop];
			}
		});

		let filteredResults = sortedResults;
		// Filters - gender
		if (currentFilters['gender']) {
			filteredResults = filteredResults.filter(
				(result) => result['gender'] === currentFilters['gender']
			);
		}

		// Sexual preferences
		if (currentFilters['sexualPreferences']) {
			filteredResults = filteredResults.filter(
				(result) => result['sexualPreferences'] === currentFilters['sexualPreferences']
			);
		}

		// Min age
		if (currentFilters['minAge']) {
			filteredResults = filteredResults.filter(
				(result) => result['age'] >= currentFilters['minAge']
			);
		}

		// Max age
		if (currentFilters['maxAge']) {
			filteredResults = filteredResults.filter(
				(result) => result['age'] <= currentFilters['maxAge']
			);
		}

		return filteredResults;
	};

	const handleSortingChange = (event: Event) => {
		const target = event.target as HTMLSelectElement;

		currentSorting = target.value;
		localStorage.setItem(SORTING_LS_KEY, currentSorting);
	};

	const handleFilterChange = (event: Event, prop: 'gender' | 'sexualPreferences') => {
		const target = event.target as HTMLSelectElement;
		const filter = target.value;

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
				<option value="fameRating;asc"> popularity (lowest) </option>
				<option value="fameRating;desc"> popularity (highest) </option>
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
				<option value={PREFERENCES_OPTIONS.FEMALE}>
					female <PreferenceSymbol preference={PREFERENCES_OPTIONS.FEMALE} />
				</option>
				<option value={PREFERENCES_OPTIONS.MALE}>
					male <PreferenceSymbol preference={PREFERENCES_OPTIONS.MALE} />
				</option>
				<option value={PREFERENCES_OPTIONS.BISEXUAL}>
					both <PreferenceSymbol preference={PREFERENCES_OPTIONS.BISEXUAL} />
				</option>
				<option value={null}>No filter</option>
			</select>
		</label>
	</ButtonSelector>

	<ButtonSelector>
		<div class="flex items-center gap-1">
			<p aria-hidden="true">Age:</p>
			<label class="flex items-center gap-1">
				<span class="sr-only">Age (min): {currentFilters.minAge}</span>
				<p aria-hidden="true">{currentFilters.minAge}</p>
				<input
					type="range"
					min="18"
					max="65"
					value={currentFilters.minAge}
					step="1"
					oninput={(e) => (currentFilters.minAge = e.target?.value)}
					class="w-20"
				/>
			</label>

			<label class="flex items-center gap-1">
				<span class="sr-only">Age (max): {currentFilters.maxAge}</span>
				<input
					type="range"
					min="18"
					max="65"
					value={currentFilters.maxAge}
					step="1"
					oninput={(e) => (currentFilters.maxAge = e.target?.value)}
					class="w-20"
				/>
				<p aria-hidden="true">{currentFilters.maxAge}</p>
			</label>
		</div>
	</ButtonSelector>

	<ButtonSelector>
		<div class="flex items-center gap-1">
			<p aria-hidden="true">Distance:</p>
			<label class="flex items-center gap-1">
				<span class="sr-only">Distance (min): {currentFilters.minDistance}</span>
				<p aria-hidden="true">{currentFilters.minDistance}</p>
				<input
					type="range"
					min="0"
					max="1000"
					value={currentFilters.minDistance}
					step="1"
					oninput={(e) => (currentFilters.minDistance = e.target?.value)}
					class="w-20"
				/>
			</label>

			<label class="flex items-center gap-1">
				<span class="sr-only">Distance (max): {currentFilters.maxDistance}</span>
				<input
					type="range"
					min="0"
					max="1000"
					value={currentFilters.maxDistance}
					step="1"
					oninput={(e) => (currentFilters.maxDistance = e.target?.value)}
					class="w-20"
				/>
				<p aria-hidden="true">{currentFilters.maxDistance}</p>
			</label>
		</div>
	</ButtonSelector>
</div>
