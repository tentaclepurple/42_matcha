<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import * as Tabs from '$lib/components/ui/tabs/index.ts';
	import { DefaultMarker, MapLibre } from 'svelte-maplibre';

	const { data } = $props();
</script>

<PageWrapper>
	<header class="mb-6">
		<h1>Dashboard</h1>
		<p>Here is where the magic happens</p>
	</header>

	<div class="max-w-5xl mx-auto">
		<Tabs.Root value="account" class="w-full bg-teal-100 shadow-lg">
			<Tabs.List class="grid w-full grid-cols-2">
				<Tabs.Trigger value="account">List</Tabs.Trigger>
				<Tabs.Trigger value="password">Map</Tabs.Trigger>
			</Tabs.List>
			<Tabs.Content value="account">
				<div class="min-h-[750px]">
					<ul class="grid w-full grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-2 p-8">
						{#each data.results as user}
							{$inspect(user)}
							<li class="flex h-[150px] w-[150px] items-center justify-center bg-teal-50 p-3">
								<img src={user.profile_photo} alt="" />
								<span>{user.username}, {user.age}</span>
							</li>
						{/each}
					</ul>
				</div>
			</Tabs.Content>
			<Tabs.Content value="password">
				<div class="min-h-[750px]">
					<MapLibre
						center={[-2.9913001, 43.3010342]}
						class="h-[750px] w-full rounded-md"
						interactive={true}
						maxZoom={18}
						minZoom={13}
						standardControls
						style="https://tiles.basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
						zoom={14}
					>
						<DefaultMarker lngLat={[-2.9913001, 43.3010342]} />
					</MapLibre>
				</div>
			</Tabs.Content>
		</Tabs.Root>
	</div>
</PageWrapper>
