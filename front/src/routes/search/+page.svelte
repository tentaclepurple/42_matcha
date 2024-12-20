<script lang="ts">
	import { page } from '$app/stores';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import * as Tabs from '$lib/components/ui/tabs';
	import { userSearchData } from '$lib/state/user-search.svelte';
	import FiltersAndSorting from './FiltersAndSorting.svelte';
	import UsersList from './UsersList.svelte';
	import UsersMap from './UsersMap.svelte';

	const viewParam = $page.url.searchParams.get('view') ?? 'map';
</script>

<PageWrapper>
	<header class="mb-6 flex flex-col items-center">
		<h1>Find true love</h1>
		<p>Use the Map or List below to search for your next soulmate.</p>
	</header>

	{#if userSearchData.value}
		<div class="mx-auto w-full max-w-5xl px-12">
			<Tabs.Root value={viewParam} class="w-full bg-teal-100 shadow-lg">
				<Tabs.List class="grid w-full grid-cols-3">
					<Tabs.Trigger value="map">Map</Tabs.Trigger>
					<Tabs.Trigger value="list">All users</Tabs.Trigger>
					<Tabs.Trigger value="recommended">Recommended for you</Tabs.Trigger>
				</Tabs.List>
				<Tabs.Content value="map">
					<div class="flex min-h-[750px] flex-col">
						<UsersMap />
					</div>
				</Tabs.Content>
				<Tabs.Content value="list">
					<FiltersAndSorting />
					<div class="flex min-h-[750px] flex-col">
						<UsersList />
					</div>
				</Tabs.Content>
				<Tabs.Content value="recommended">
					<div class="flex min-h-[750px] flex-col">
						<UsersList />
					</div>
				</Tabs.Content>
			</Tabs.Root>
		</div>
	{/if}
</PageWrapper>
