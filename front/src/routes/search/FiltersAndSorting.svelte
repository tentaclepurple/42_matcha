<script lang="ts">
	import {
		DEFAULT_ALL_RESULTS_FILTER_ORDER,
		DEFAULT_ALL_RESULTS_FILTER_PROP,
		FILTERS_ORDER
	} from '$lib/constants/filters';

	const { results, setResults } = $props();

	const currentFilter: string = $state(
		`${DEFAULT_ALL_RESULTS_FILTER_PROP};${DEFAULT_ALL_RESULTS_FILTER_ORDER}`
	);

	const handleFilterChange = (event: Event) => {
		const target = event.target as HTMLSelectElement;
		const [prop, order] = target.value.split(';');

		const orderedResults = [...results].sort((a, b) => {
			if (order === FILTERS_ORDER.ASC) {
				return a[prop] - b[prop];
			} else {
				return b[prop] - a[prop];
			}
		});

		setResults(orderedResults);
	};
</script>

<div class="px-6">
	<label class="border-1 rounded-3xl border border-teal-500 bg-white px-4 py-2 text-xs">
		Filter by:
		<select name="filter" onchange={handleFilterChange}>
			<option value="distance;asc" selected={currentFilter === 'distance;asc'}>
				distance (nearest first)
			</option>
			<option value="distance;desc" selected={currentFilter === 'distance;desc'}>
				distance (farthest first)
			</option>
		</select>
	</label>
</div>
