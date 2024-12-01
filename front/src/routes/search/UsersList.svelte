<script lang="ts">
	import { goto } from '$app/navigation';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import type UserProfileData from '$lib/interfaces/user-profile-data.interface';

	const { results } = $props();

	const handleOpenUser = async (event) => {
		const button = event.currentTarget as HTMLButtonElement;
		const username = button.dataset.username;

		goto(`/search/${username}?origin=list`);
	};
</script>

<ul class="grid w-full grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-3 p-8">
	{#each results as user (user.user_id)}
		<li class="flex items-center justify-center rounded-md bg-teal-50 p-3 shadow-md">
			<button type="button" data-username={user.username} onclick={handleOpenUser}>
				<img src="/icons/avatar.svg" alt="" class="mb-2" />
				<span>{user.username}, {user.age}</span>
			</button>
		</li>
	{/each}
</ul>
