<script lang="ts">
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import * as Tabs from '$lib/components/ui/tabs';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import { userSearchSuggestionsData } from '$lib/state/user-search-suggestions.svelte';
	import { userSearchData } from '$lib/state/user-search.svelte';
	import SearchFiltersAndSorting from './SearchFiltersAndSorting.svelte';
	import SuggestionsFiltersAndSorting from './SuggestionsFiltersAndSorting.svelte';
	import UsersList from './UsersList.svelte';
	import UsersMap from './UsersMap.svelte';

	const viewParam = $page.url.searchParams.get('view') ?? 'map';
</script>

<PageWrapper>
	<header class="mb-6 hidden flex-col items-center sm:flex">
		<h1>Find true love</h1>
		<p>Use the Map or List below to search for your next soulmate.</p>
	</header>

	{#if userSearchData.value}
		{#if !userProfileData.isProfileComplete}
			<div class="mx-auto mb-6 flex w-fit max-w-5xl gap-6 rounded-md bg-teal-200 px-12 py-6">
				<span aria-hidden="true" class="text-xl">ℹ️</span>
				<div>
					<p>Please complete your profile to start searching for your soulmate.</p>
					<p>Go to your <a href="/profile">Profile</a> page to fill out the missing data.</p>
				</div>
			</div>
		{/if}
		<div
			class={`w-5xl mx-auto h-full w-full sm:h-auto sm:px-12 ${userProfileData.isProfileComplete ? '' : 'pointer-events-none cursor-not-allowed opacity-50'}`}
			aria-hidden={!userProfileData.isProfileComplete}
		>
			<Tabs.Root value={viewParam} class="h-full w-full bg-teal-100 shadow-lg">
				<Tabs.List class="grid w-full grid-cols-3">
					<Tabs.Trigger value="map">Map</Tabs.Trigger>
					<Tabs.Trigger value="list">All users</Tabs.Trigger>
					<Tabs.Trigger value="recommended">
						<span class="sm:sr-only">Recommended</span>
						<span class="sr-only sm:not-sr-only">Recommended for you</span>
					</Tabs.Trigger>
				</Tabs.List>
				<Tabs.Content value="map">
					<div class="flex h-full flex-col">
						<UsersMap />
					</div>
				</Tabs.Content>
				<Tabs.Content value="list">
					<SearchFiltersAndSorting />
					<div class="flex min-h-[750px] flex-col">
						<UsersList results={userSearchData.value ? userSearchData.value : []} />
					</div>
				</Tabs.Content>
				<Tabs.Content value="recommended">
					<div class="flex min-h-[750px] flex-col">
						<SuggestionsFiltersAndSorting />
						<UsersList
							results={userSearchSuggestionsData.value ? userSearchSuggestionsData.value : []}
						/>
					</div>
				</Tabs.Content>
			</Tabs.Root>
		</div>
	{/if}
</PageWrapper>
