<script lang="ts">
	const { children } = $props();

	import { onDestroy, onMount } from 'svelte';

	import '../app.css';
	import MenuWidget from './MenuWidget.svelte';
	import { userAuth } from '$lib/state/auth.svelte';
	import { userLocation } from '$lib/state/geolocation.svelte';
	import { userData } from '$lib/state/user-data.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import { notificationsData } from '$lib/state/notifications.svelte';
	import { NOTIFICATIONS_POLLING_INTERVAL } from '$lib/constants/notifications';
	import NotificationsWidget from './NotificationsWidget.svelte';
	import { goto } from '$app/navigation';
	import MessagesWidget from './MessagesWidget.svelte';

	let isTabHidden = $state(false);

	const handleVisibilityChange = () => {
		isTabHidden = document.hidden;
	};

	const handleBeforeUnload = () => {
		// logout user if tab is closed
		if (isTabHidden) {
			userAuth.logout();
		}
	};

	onMount(async (): Promise<void> => {
		window.addEventListener('beforeunload', handleBeforeUnload);
		window.addEventListener('visibilitychange', handleVisibilityChange);

		//cleanup
		onDestroy(() => {
			window.removeEventListener('beforeunload', handleBeforeUnload);
			window.removeEventListener('visibilitychange', handleVisibilityChange);
		});

		let interval: number;

		const accessToken = localStorage.getItem('access_token');

		if (accessToken) {
			try {
				userAuth.login();
				await userData.fetch();
				await userProfileData.fetch();
				await userLocation.getUserLocation();

				if (userAuth.isAuthenticated) {
					notificationsData.fetch();
				}
			} catch (e) {
				console.error(e);
				userAuth.logout();
				goto('/login');
			}
		} else {
			userAuth.logout();
		}
	});

	$effect(() => {
		if (userAuth.isAuthenticated) {
			const interval = setInterval(() => {
				notificationsData.fetch();
			}, NOTIFICATIONS_POLLING_INTERVAL);

			return () => {
				clearInterval(interval);
			};
		}
	});
</script>

<div class="flex min-h-screen flex-col justify-between">
	<div class="flex items-center justify-center bg-teal-300 px-4 py-0">
		<header class="flex min-h-[68px] w-full max-w-screen-2xl items-center justify-between">
			<nav class="flex items-baseline justify-center gap-2">
				<a href="/" aria-label="Home">
					<img src="/icons/home.svg" alt="" class="w-5" />
				</a>
			</nav>

			<div class="flex items-center justify-center gap-5">
				{#if userAuth.isAuthenticated}
					<MessagesWidget />
					<NotificationsWidget />
					<MenuWidget />
				{:else}
					<a href="/login" class="flex items-center justify-center gap-1 no-underline">
						Sign in
						<img src="/icons/login.svg" alt="" class="w-5" />
					</a>
				{/if}
			</div>
		</header>
	</div>

	{@render children()}
</div>
