<script lang="ts">
	import { goto } from '$app/navigation';
	import RoundAvatar from '$lib/components/RoundAvatar.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { logout } from '$lib/stores/auth';
	import { onDestroy, onMount } from 'svelte';
	import { userData } from '$lib/stores/user-data';

	let showMenu: boolean = $state(false);

	const avatarUrl: string = $derived(
		$userData?.profilePhoto ? getServerAsset($userData.profilePhoto) : '/icons/avatar.svg'
	);

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

	const handleShowMenu = () => {
		showMenu = !showMenu;
	};

	const handleClickOutside = (e: Event) => {
		const target = e.target as HTMLElement;

		if (showMenu && !target.closest('#wrapper')) {
			showMenu = false;
		}
	};

	onMount(async () => {
		window.addEventListener('click', handleClickOutside);
	});

	onDestroy(() => {
		window.removeEventListener('click', handleClickOutside);
	});
</script>

<div class="relative" id="wrapper">
	<button type="button" onclick={handleShowMenu} class="cursor-pointer rounded-full shadow-md">
		<RoundAvatar src={avatarUrl} alt="" size="s" />
	</button>
	{#if showMenu}
		<div
			class="absolute right-0 top-full mt-2 flex min-h-32 min-w-48 justify-end rounded-md bg-teal-200 p-6 shadow-xl"
		>
			<nav class="flex flex-col items-end gap-3">
				<a href="/dashboard" onclick={handleShowMenu} class="flex items-center gap-1">
					<img src="/icons/home.svg" alt="" class="w-4" />
					Dashboard
				</a>
				<a href="/account" onclick={handleShowMenu} class="flex items-center gap-1">
					<img src="/icons/settings.svg" alt="" class="w-5" />
					Account
				</a>
				<a href="/profile" onclick={handleShowMenu} class="flex items-center gap-1">
					<img src="/icons/avatar.svg" alt="" class="w-5" />
					Profile
				</a>
				<button type="button" onclick={handleLogOut} class="mt-6 flex items-center gap-1">
					<img src="/icons/exit.svg" alt="" class="w-6" />
					Log out
				</button>
			</nav>
		</div>
	{/if}
</div>
