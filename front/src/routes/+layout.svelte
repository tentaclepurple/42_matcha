<script lang="ts">
	import { isAuthenticated, login, logout } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';

	import '../app.css';
	import { goto } from '$app/navigation';
	let { children } = $props();

	const handleLogOut = () => {
		const accessToken = localStorage.getItem('access_token');

		if (accessToken) {
			const res = fetch(`${SERVER_BASE_URL}/api/users/logout`, {
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

	onMount(() => {
		const accessToken = localStorage.getItem('access_token');

		if (accessToken) {
			login();
		}
	});
</script>

<div class="flex min-h-screen flex-col justify-between">
	<div class="flex items-center justify-center bg-teal-300 p-4">
		<header class="flex w-full max-w-screen-2xl items-baseline justify-between">
			<nav class="flex items-baseline justify-center gap-2">
				<a href="/">Home</a>
			</nav>

			<div>
				{#if $isAuthenticated}
					<a href="/profile">Profile</a>
					<button type="button" onclick={handleLogOut}>Log out</button>
				{:else}
					<a href="/login">Sign in</a>
				{/if}
			</div>
		</header>
	</div>

	{@render children()}
</div>
