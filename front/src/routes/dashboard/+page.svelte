<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import * as Tabs from '$lib/components/ui/tabs/index.ts';
	import UsersList from './UsersList.svelte';
	import UsersMap from './UsersMap.svelte';

	const { data } = $props();
</script>

<PageWrapper>
	<header class="mb-6">
		<h1>Dashboard</h1>
		<p>Here is where the magic happens</p>
	</header>

	<div class="mx-auto max-w-5xl">
		<Tabs.Root value="account" class="w-full bg-teal-100 shadow-lg">
			<Tabs.List class="grid w-full grid-cols-2">
				<Tabs.Trigger value="account">Map</Tabs.Trigger>
				<Tabs.Trigger value="password">List</Tabs.Trigger>
			</Tabs.List>
			<Tabs.Content value="account">
				<div class="min-h-[750px]">
					<UsersMap results={data.results} />
				</div>
			</Tabs.Content>
			<Tabs.Content value="password">
				<div class="min-h-[750px]">
					<UsersList results={data.results} />
				</div>
			</Tabs.Content>
		</Tabs.Root>
	</div>
</PageWrapper>
