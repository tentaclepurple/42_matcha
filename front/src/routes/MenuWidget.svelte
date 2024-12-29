<script lang="ts">
	import { goto } from '$app/navigation';
	import RoundAvatar from '$lib/components/RoundAvatar.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';
	import { onDestroy, onMount } from 'svelte';
	import { userAuth } from '$lib/state/auth.svelte';
	import { userData } from '$lib/state/user-data.svelte';

	let showMenu: boolean = $state(false);

	const avatarUrl: string = $derived(
		userData.value?.profilePhoto ? getServerAsset(userData.value.profilePhoto) : '/icons/avatar.svg'
	);

	const handleLogOut = () => {
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
	<div class="flex items-center gap-2">
		<button
			type="button"
			onclick={handleShowMenu}
			class="cursor-pointer rounded-full shadow-md hover:shadow-lg"
		>
			<RoundAvatar src={avatarUrl} alt="" size="s" />
		</button>

		<button
			type="button"
			onclick={handleLogOut}
			class="flex items-center justify-center"
			aria-label="Log out"
			title="Log out"
		>
			<img src="/icons/exit.svg" alt="" class="w-7" />
		</button>
	</div>
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
			</nav>
		</div>
	{/if}
</div>
