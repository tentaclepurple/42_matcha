<script lang="ts">
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';

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
		selectedUser = data;
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
	<div class="m-8 flex w-3/5 flex-col items-center bg-teal-200 p-3">
		{#if selectedUser}
			<h2>{selectedUser.username}, {selectedUser.age}</h2>

			<dl>
				<dt>Bio</dt>
				<dd>{selectedUser.biography}</dd>
			</dl>
		{/if}
	</div>
</div>
