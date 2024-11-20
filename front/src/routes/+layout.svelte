<script lang="ts">
	export let profilePhoto: string | null = null;
	export let children;

	import { isAuthenticated, login, logout } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';

	import '../app.css';
	import { goto } from '$app/navigation';
	import RoundedAvatar from '$lib/components/RoundedAvatar.svelte';
	import { fetchUserData, userData } from '$lib/stores/user-data';
	import getServerAsset from '$lib/utils/get-server-asset';
	import type UserData from '$lib/interfaces/user-data.interface';

	let currentUserData: UserData | null = null;

	userData.subscribe((value) => {
		currentUserData = value;
	});

	const handleLogOut = () => {
		const accessToken = localStorage.getItem('access_token');

		if (accessToken) {
			fetch(`${SERVER_BASE_URL}/api/users/logout`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('access_token')}`
				}
			});

			localStorage.removeItem('access_token');
		}

		logout();
		goto('/');
	};

	onMount(async () => {
		const accessToken = localStorage.getItem('access_token');

		if (accessToken) {
			login();
		}

		await fetchUserData();
	});
</script>

<div class="flex min-h-screen flex-col justify-between">
	<div class="flex items-center justify-center bg-teal-300 p-4">
		<header class="flex w-full max-w-screen-2xl items-baseline justify-between">
			<nav class="flex items-baseline justify-center gap-2">
				<a href="/">Home</a>
			</nav>

			<div class="flex items-center justify-center gap-4">
				{#if $isAuthenticated}
					<button
						onclick={() => {
							goto('/account');
						}}
						aria-label="Settings"
					>
						<RoundedAvatar
							src={currentUserData?.profilePhoto
								? getServerAsset(currentUserData.profilePhoto)
								: '/icons/avatar.svg'}
							alt=""
							size="s"
						/>
					</button>
					<button type="button" onclick={handleLogOut}>Log out</button>
				{:else}
					<a href="/login">Sign in</a>
				{/if}
			</div>
		</header>
	</div>

	{@render children()}
</div>
