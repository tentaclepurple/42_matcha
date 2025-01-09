<script lang="ts">
	import ButtonSelector from '$lib/components/ButtonSelector.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import {
		DEFAULT_ALL_RESULTS_SORTING_ORDER,
		DEFAULT_ALL_RESULTS_SORTING_PROP,
		SUGGESTIONS_COMMON_INTERESTS,
		SUGGESTIONS_MAX_DISTANCE,
		SUGGESTIONS_MIN_POPULARITY,
		SUGGESTIONS_SORTING_LS_KEY
	} from '$lib/constants/sorting';
	import { calcQueryParams } from './calc-query-params.util';
	import { userSearchSuggestionsData } from '$lib/state/user-search-suggestions.svelte';
	import { onMount } from 'svelte';
	import TooltipButtonSelector from './SuggestionsFiltersAndSorting/TooltipButtonSelector.svelte';
	import RangeFilter from './RangeFilter.svelte';

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

		<TooltipButtonSelector>
			<label>
				Gender:
				<select disabled class="cursor-not-allowed">
					<option selected>
						{userProfileData.value.gender}
						<GenderSymbol gender={userProfileData.value.gender} />
					</option>
				</select>
			</label>
		</TooltipButtonSelector>

		<TooltipButtonSelector>
			<label>
				Likes:
				<select disabled class="cursor-not-allowed">
					<option selected>
						{userProfileData.value.sexualPreferences}
						<PreferenceSymbol preference={userProfileData.value.sexualPreferences} />
					</option>
				</select>
			</label>
		</TooltipButtonSelector>

		<TooltipButtonSelector>
			<RangeFilter
				label="Distance (km)"
				minValue="0"
				maxValue={SUGGESTIONS_MAX_DISTANCE}
				min="0"
				max={SUGGESTIONS_MAX_DISTANCE}
				step="1"
				onChangeMax={() => {}}
			/>
		</TooltipButtonSelector>

		<TooltipButtonSelector>
			<label>
				Common interests:
				<input type="text" disabled value={SUGGESTIONS_COMMON_INTERESTS} class="w-[10px]" />
			</label>
		</TooltipButtonSelector>

		<TooltipButtonSelector>
			<label>
				Min popularity:
				<input type="text" disabled value={SUGGESTIONS_MIN_POPULARITY} class="w-[26px]" />
			</label>
		</TooltipButtonSelector>
	</div>
{/if}
