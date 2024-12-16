<script lang="ts">
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import * as Tabs from '$lib/components/ui/tabs';
	import FiltersAndSorting from './FiltersAndSorting.svelte';
	import UsersList from './UsersList.svelte';
	import UsersMap from './UsersMap.svelte';

	const { data } = $props();

	const viewParam = $page.url.searchParams.get('view') ?? 'map';

	let results = $state(data.searchResults);
	let unfilteredResults = $state(data.searchResults);

	const setResults = (newResults) => {
		results = newResults;
	};
</script>

<PageWrapper>
	<header class="mb-6 flex flex-col items-center">
		<h1>Find true love</h1>
		<p>Use the Map or List below to search for your next soulmate.</p>
	</header>

	<div class="mx-auto w-full max-w-5xl px-12">
		<Tabs.Root value={viewParam} class="w-full bg-teal-100 shadow-lg">
			<Tabs.List class="grid w-full grid-cols-3">
				<Tabs.Trigger value="map">Map</Tabs.Trigger>
				<Tabs.Trigger value="list">All users</Tabs.Trigger>
				<Tabs.Trigger value="recommended">Recommended for you</Tabs.Trigger>
			</Tabs.List>
			<Tabs.Content value="map">
				<div class="flex min-h-[750px] flex-col">
					<UsersMap results={data.searchResults} />
				</div>
			</Tabs.Content>
			<Tabs.Content value="list">
				<FiltersAndSorting {results} {setResults} {unfilteredResults} />
				<div class="flex min-h-[750px] flex-col">
					<UsersList {results} />
				</div>
			</Tabs.Content>
			<Tabs.Content value="recommended">
				<div class="flex min-h-[750px] flex-col">
					<UsersList results={data.suggestionsResults} />
				</div>
			</Tabs.Content>
		</Tabs.Root>
	</div>
</PageWrapper>
