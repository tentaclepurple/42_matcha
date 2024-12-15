<script lang="ts">
	import ButtonSelector from '$lib/components/ButtonSelector.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import {
		DEFAULT_ALL_RESULTS_SORTING_ORDER,
		DEFAULT_ALL_RESULTS_SORTING_PROP,
		SORTING_LS_KEY,
		SORTING_ORDER
	} from '$lib/constants/sorting';
	import { GENDER_OPTIONS, PREFERENCES_OPTIONS } from '$lib/constants/user-profile-data';
	import { onMount } from 'svelte';

	const { results, setResults, setUnfilteredResults, unfilteredResults } = $props();

	let currentFilter = $state(
		`${DEFAULT_ALL_RESULTS_SORTING_PROP};${DEFAULT_ALL_RESULTS_SORTING_ORDER}`
	);

	onMount(() => {
		const storedSortingCriteria = localStorage?.getItem(SORTING_LS_KEY);

		if (storedSortingCriteria) {
			currentFilter = storedSortingCriteria;
		}
	});

	const handleSortingChange = (event: Event) => {
		const target = event.target as HTMLSelectElement;
		const [prop, order] = target.value.split(';');

		const orderedResults = [...results].sort((a, b) => {
			if (order === SORTING_ORDER.ASC) {
				return a[prop] - b[prop];
			} else {
				return b[prop] - a[prop];
			}
		});

		setUnfilteredResults(orderedResults);
		setResults(unfilteredResults);
		localStorage.setItem(SORTING_LS_KEY, target.value);
	};

	const handleFilterChange = (event: Event, prop: string) => {
		const target = event.target as HTMLSelectElement;
		const filter = target.value;

		const filteredResults = [...unfilteredResults].filter((result) => result[prop] === filter);

		setResults(filteredResults);
	};
</script>

<div class="flex items-center gap-2 px-4">
	<ButtonSelector>
		<label>
			Sort by:
			<select onchange={handleSortingChange}>
				<option value="distance;asc" selected={currentFilter === 'distance;asc'}>
					distance (nearest)
				</option>
				<option value="distance;desc" selected={currentFilter === 'distance;desc'}>
					distance (farthest)
				</option>
				<option value="age;asc" selected={currentFilter === 'age;asc'}>age (youngest)</option>
				<option value="age;desc" selected={currentFilter === 'age;desc'}>age (oldest)</option>
				<option value="fameRating;asc" selected={currentFilter === 'fameRating;asc'}>
					popularity (lowest)
				</option>
				<option value="fameRating;desc" selected={currentFilter === 'fameRating;desc'}>
					popularity (highest)
				</option>
			</select>
		</label>
	</ButtonSelector>

	<ButtonSelector>
		<label>
			Gender:
			<select onchange={(e) => handleFilterChange(e, 'gender')}>
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
			<select onchange={(e) => handleFilterChange(e, 'sexualPreferences')}>
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
</div>
