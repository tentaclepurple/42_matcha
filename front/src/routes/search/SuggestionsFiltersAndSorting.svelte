<script lang="ts">
	import ButtonSelector from '$lib/components/ButtonSelector.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import {
		DEFAULT_ALL_RESULTS_SORTING_ORDER,
		DEFAULT_ALL_RESULTS_SORTING_PROP,
		SORTING_LS_KEY,
		SUGGESTIONS_SORTING_LS_KEY
	} from '$lib/constants/sorting';
	import { calcQueryParams } from './calc-query-params.util';
	import { userSearchSuggestionsData } from '$lib/state/user-search-suggestions.svelte';
	import { onMount } from 'svelte';
	import Tooltip from '$lib/components/Tooltip.svelte';

	let currentSorting = $state(
		`${DEFAULT_ALL_RESULTS_SORTING_PROP};${DEFAULT_ALL_RESULTS_SORTING_ORDER}`
	);

	onMount(async () => {
		const storedSortingCriteria = localStorage?.getItem(SUGGESTIONS_SORTING_LS_KEY);

		if (storedSortingCriteria) {
			currentSorting = storedSortingCriteria;
		}

		const queryParams = calcQueryParams({ currentSorting });
		await userSearchSuggestionsData.fetch({ params: queryParams });
	});

	$effect(() => {
		if (currentSorting) {
			const params = calcQueryParams({ currentSorting });
			userSearchSuggestionsData.fetch({ params });
		}
	});

	const handleSortingChange = (event: Event) => {
		const target = event.target as HTMLSelectElement;

		currentSorting = target.value;
		localStorage.setItem(SUGGESTIONS_SORTING_LS_KEY, currentSorting);
	};
</script>

{#if userProfileData.value}
	<div class="mb-2 flex flex-wrap items-center gap-2 px-4">
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

		<Tooltip
			message="Recommended results cannot be filtered. If you need the filters, go to the All users tab."
			class="left-0 top-9"
		>
			<ButtonSelector class="cursor-not-allowed opacity-75">
				<label>
					Gender:
					<select disabled class="cursor-not-allowed">
						<option selected>
							{userProfileData.value.gender}
							<GenderSymbol gender={userProfileData.value.gender} />
						</option>
					</select>
				</label>
			</ButtonSelector>
		</Tooltip>

		<Tooltip
			message="Recommended results cannot be filtered. If you need the filters, go to the All users tab."
			class="left-0 top-9"
		>
			<ButtonSelector class="cursor-not-allowed opacity-75">
				<label>
					Likes:
					<select disabled class="cursor-not-allowed">
						<option selected>
							{userProfileData.value.sexualPreferences}
							<PreferenceSymbol preference={userProfileData.value.sexualPreferences} />
						</option>
					</select>
				</label>
			</ButtonSelector>
		</Tooltip>
	</div>
{/if}
