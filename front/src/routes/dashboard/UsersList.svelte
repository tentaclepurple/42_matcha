<script lang="ts">
	import FameRating from '$lib/components/FameRating.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';
	import { DefaultMarker, MapLibre } from 'svelte-maplibre';

	const { results } = $props();

	let selectedUser = $state<null | UserProfileData>(null);

	const handleOpenUser = async (event) => {
		const token = localStorage.getItem('access_token');
		if (!token) {
			return;
		}

		const button = event.currentTarget as HTMLButtonElement;
		const username = button.dataset.username;

		if (!username) {
			return;
		}

		const res = await fetch(`${SERVER_BASE_URL}/api/profile/profile_info/${username}`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			}
		});

		if (!res.ok) {
			console.error('Failed to fetch user data');
			return;
		}

		const data = await res.json();
		console.log('data', data);
		selectedUser = {
			...data,
			fameRating: data.fame_rating,
			sexualPreference: data.sexual_preferences
		};
	};
</script>

<div class="flex justify-between gap-2">
	<ul class="grid w-full grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-3 p-8">
		{#each results as user (user.user_id)}
			<li class="flex h-[150px] w-[150px] items-center justify-center bg-teal-50 p-3">
				<button
					type="button"
					data-username={user.username}
					onclick={handleOpenUser}
					class="h-[150px] w-[150px]"
				>
					<img src={user.profile_photo} alt="" />
					<span>{user.username}, {user.age}</span>
				</button>
			</li>
		{/each}
	</ul>
	<div class="m-8 flex w-3/5 flex-col items-between justify-between bg-teal-200 p-3">
		{#if selectedUser}
			{$inspect(selectedUser)}
			<div>
				<div class="flex items-center justify-between">
					<img
						class="shadow-mg h-24 w-24 bg-white object-cover"
						src={selectedUser.photos.filter((photo) => photo.is_profile)[0].url ||
							'icons/avatar.svg'}
						alt=""
					/>

					<FameRating fameRating={selectedUser.fameRating} />
				</div>
				<h2>{selectedUser.username}, {selectedUser.age}</h2>

				<div class="description-list mb-6 flex flex-col gap-3">
					<dl>
						<dt>Gender:</dt>
						<dd>{selectedUser.gender} <GenderSymbol gender={selectedUser.gender} /></dd>
					</dl>

					<dl>
						<dt>Interested in:</dt>
						<dd>
							{selectedUser.sexualPreference}
							<PreferenceSymbol preference={selectedUser.sexualPreference} />
						</dd>
					</dl>

					<dl>
						<dt>Bio:</dt>
						<dd>{selectedUser.biography}</dd>
					</dl>
				</div>
			</div>

			<MapLibre
				center={selectedUser.location.coordinates}
				class="h-[250px] w-full rounded-md"
				interactive={false}
				maxZoom={18}
				minZoom={11}
				standardControls
				style="https://tiles.basemaps.cartocdn.com/gl/voyager-gl-style/style.json"
				zoom={14}
			>
				<DefaultMarker lngLat={selectedUser.location.coordinates} />
			</MapLibre>
		{/if}
	</div>
</div>

<style>
	.description-list {
		dt {
			font-weight: bold;
		}
	}
</style>
