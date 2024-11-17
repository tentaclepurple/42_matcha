<script lang="ts">
	import { isAuthenticated, login, logout } from '$lib/stores/auth';
	import { onMount } from 'svelte';

	import '../app.css';
	import { goto } from '$app/navigation';
	let { children } = $props();

	const handleLogOut = () => {
		localStorage.removeItem('access_token');
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
	<div class="flex items-center justify-center bg-lime-300 p-4">
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
