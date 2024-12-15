<script lang="ts">
	import {
		DEFAULT_ALL_RESULTS_SORTING_ORDER,
		DEFAULT_ALL_RESULTS_SORTING_PROP,
		SORTING_LS_KEY,
		SORTING_ORDER
	} from '$lib/constants/filters';
	import { onMount } from 'svelte';

	const { results, setResults } = $props();

	let currentFilter = $state(
		`${DEFAULT_ALL_RESULTS_SORTING_PROP};${DEFAULT_ALL_RESULTS_SORTING_ORDER}`
	);

	onMount(() => {
		const storedSortingCriteria = localStorage?.getItem(SORTING_LS_KEY);

		if (storedSortingCriteria) {
			currentFilter = storedSortingCriteria;
		}
	});

	const handleFilterChange = (event: Event) => {
		const target = event.target as HTMLSelectElement;
		const [prop, order] = target.value.split(';');

		const orderedResults = [...results].sort((a, b) => {
			if (order === SORTING_ORDER.ASC) {
				return a[prop] - b[prop];
			} else {
				return b[prop] - a[prop];
			}
		});

		setResults(orderedResults);
		localStorage.setItem(SORTING_LS_KEY, target.value);
	};
</script>

<div class="px-6">
	<label class="border-1 rounded-3xl border border-teal-500 bg-white px-4 py-2 text-xs">
		Sort by:
		<select name="filter" onchange={handleFilterChange}>
			<option value="distance;asc" selected={currentFilter === 'distance;asc'}>
				distance (nearest)
			</option>
			<option value="distance;desc" selected={currentFilter === 'distance;desc'}>
				distance (farthest)
			</option>
			<option value="age;asc" selected={currentFilter === 'age;asc'}>age (youngest)</option>
			<option value="age;desc" selected={currentFilter === 'age;desc'}>age (oldest)</option>
			<option value="fame_rating;asc" selected={currentFilter === 'fame_rating;asc'}>
				popularity (lowest)
			</option>
			<option value="fame_rating;desc" selected={currentFilter === 'fame_rating;desc'}>
				popularity (highest)
			</option>
		</select>
	</label>
</div>
