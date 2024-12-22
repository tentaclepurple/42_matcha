<script lang="ts">
	import { goto } from '$app/navigation';
	import RoundAvatar from '$lib/components/RoundAvatar.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { onDestroy, onMount } from 'svelte';
	import { userAuth } from '$lib/state/auth.svelte';
	import { userData } from '$lib/state/user-data.svelte';

	let showMenu: boolean = $state(false);

	const avatarUrl: string = $derived(
		userData.value?.profilePhoto ? getServerAsset(userData.value.profilePhoto) : '/icons/avatar.svg'
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

		userAuth.logout();
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
			class="absolute right-0 top-full z-50 mt-2 flex min-h-32 min-w-48 justify-end rounded-md bg-teal-100 p-6 shadow-xl"
			style="z-index: 99"
		>
			<nav class="flex flex-col items-end gap-3">
				<a href="/search" onclick={handleShowMenu} class="flex items-center gap-1">
					<img src="/icons/search.svg" alt="" class="w-4" />
					Search
				</a>
				<a href="/chat" onclick={handleShowMenu} class="mb-4 flex items-center gap-1">
					<img src="/icons/messages.svg" alt="" class="w-5" />
					Messages
				</a>
				<a href="/account" onclick={handleShowMenu} class="flex items-center gap-1">
					<img src="/icons/settings.svg" alt="" class="w-5" />
					Account
				</a>
				<a href="/profile" onclick={handleShowMenu} class="mb-6 flex items-center gap-1">
					<img src="/icons/avatar.svg" alt="" class="w-5" />
					Profile
				</a>
				<button type="button" onclick={handleLogOut} class="flex items-center gap-1">
					<img src="/icons/exit.svg" alt="" class="w-6" />
					Log out
				</button>
			</nav>
		</div>
	{/if}
</div>
