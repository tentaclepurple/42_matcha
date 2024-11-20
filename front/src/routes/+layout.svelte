<script lang="ts">
	export let children;

	import { isAuthenticated, login } from '$lib/stores/auth';
	import { onMount } from 'svelte';

	import '../app.css';
	import { fetchUserData, userData } from '$lib/stores/user-data';
	import type UserData from '$lib/interfaces/user-data.interface';
	import MenuWidget from './MenuWidget.svelte';

	let currentUserData: UserData | null = null;

	userData.subscribe((value) => {
		currentUserData = value;
	});

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
		<header class="flex w-full max-w-screen-2xl items-center justify-between">
			<nav class="flex items-baseline justify-center gap-2">
				<a href="/" aria-label="Home">
					<img src="icons/home.svg" alt="" class="w-6" />
				</a>
			</nav>

			<div class="flex items-center justify-center gap-4">
				{#if $isAuthenticated}
					<MenuWidget {currentUserData} />
				{:else}
					<a href="/login">Sign in</a>
				{/if}
			</div>
		</header>
	</div>

	{@render children()}
</div>
