<!-- routes/+layout.svelte -->

<script lang="ts">
    export let children;

    import { isAuthenticated, login } from '$lib/stores/auth';
    import { onMount, onDestroy } from 'svelte';
    import '../app.css';
    import { fetchUserData } from '$lib/stores/user-data';
    import MenuWidget from './MenuWidget.svelte';
    import NotificationService from '$lib/services/NotificationService';

    onMount(async () => {
        const accessToken = localStorage.getItem('access_token');

        if (accessToken) {
            login();
            // Iniciamos el polling de notificaciones
            NotificationService.startCheckingInvitations();
        }

        await fetchUserData();
    });

    // Detenemos el polling cuando el componente se destruye
    onDestroy(() => {
        NotificationService.stopCheckingInvitations();
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
                    <MenuWidget />
                {:else}
                    <a href="/login" class="flex items-center justify-center gap-1 no-underline">
                        Sign in
                        <img src="icons/login.svg" alt="" class="w-5" />
                    </a>
                {/if}
            </div>
        </header>
    </div>

    {@render children()}
</div>