<script lang="ts">
	import { goto } from '$app/navigation';
	import { NOTIFICATIONS_TYPES } from '$lib/constants/notifications';
	import type Notification from '$lib/interfaces/notification.interface';
	import { messagesData } from '$lib/state/messages.svelte';
	import { notificationsData } from '$lib/state/notifications.svelte';
	import { visitedProfileData } from '$lib/state/visited-profile-data.svelte';
	import { onDestroy, onMount } from 'svelte';

	let showMenu: boolean = $state(false);

	const handleShowMenu = () => {
		showMenu = !showMenu;
	};

	const handleClickOutside = (e: Event) => {
		const target = e.target as HTMLElement;

		if (showMenu && !target.closest('#notifications-wrapper')) {
			showMenu = false;
		}
	};

	const handleNotificationClick = async (notification: Notification) => {
		const username = notification.fromUser.username;
		switch (notification.type) {
			case NOTIFICATIONS_TYPES.MESSAGE:
				try {
					await messagesData.fetchMessages({ username });
					goto(`/chat/${username}`);
				} catch (error) {
					console.error(error);
				}
				break;
			case NOTIFICATIONS_TYPES.MATCH:
			case NOTIFICATIONS_TYPES.LIKE:
			case NOTIFICATIONS_TYPES.UNLIKE:
			case NOTIFICATIONS_TYPES.PROFILE_VIEW:
				try {
					await visitedProfileData.fetch(username);
					goto(`/search/${username}`);
				} catch (error) {
					console.error(error);
				}
				break;
		}

		notificationsData.markAsRead(notification.id);
		showMenu = false;
	};

	onMount(async () => {
		window.addEventListener('click', handleClickOutside);
	});

	onDestroy(() => {
		window.removeEventListener('click', handleClickOutside);
	});
</script>

<div>
	{$inspect(notificationsData.value)}
	{#if notificationsData.value?.count && notificationsData.value.count > 0 && notificationsData.value?.notifications}
		<div class="relative" id="notifications-wrapper">
			<button
				class="relative flex h-9 w-9 items-center justify-center rounded-full border border-2 border-teal-500 bg-teal-100"
				onclick={handleShowMenu}
			>
				<p class="sr-only">{notificationsData.value?.count} new notifications</p>
				<img src="/icons/notifications/active.svg" alt="" class="w-5" />
				<p
					class="absolute flex h-5 w-5 items-center justify-center rounded-full bg-red-600 text-xs font-bold text-white"
					style="bottom: -8px; left: -8px;"
				>
					{notificationsData.value?.count}
				</p>
			</button>
			{#if showMenu}
				<div
					class="absolute right-0 top-full z-50 mt-2 flex min-h-32 w-max min-w-52 justify-end rounded-md bg-teal-100 p-6 shadow-xl"
				>
					<ul class="flex w-max flex-col gap-2 text-sm">
						{#each notificationsData.value?.notifications as notification}
							<li>
								<button
									class="flex w-full items-center justify-between gap-4 rounded-md bg-teal-200 px-2 py-1"
									onclick={() => {
										handleNotificationClick(notification);
									}}
								>
									<div>
										<span class="text-xs text-gray-600">
											{new Date(notification.createdAt).toLocaleDateString('en-US', {
												month: 'short',
												day: 'numeric',
												hour: 'numeric',
												minute: 'numeric'
											})}
										</span>
										-
										<span>
											{#if notification.type === NOTIFICATIONS_TYPES.MESSAGE}
												New message from <span class="font-bold"
													>{notification.fromUser.username}</span
												>.
											{:else if notification.type === NOTIFICATIONS_TYPES.MATCH}
												<span class="font-bold">{notification.fromUser.username}</span> matched with
												you.
											{:else if notification.type === NOTIFICATIONS_TYPES.LIKE}
												<span class="font-bold">{notification.fromUser.username}</span> liked you.
											{:else if notification.type === NOTIFICATIONS_TYPES.UNLIKE}
												<span class="font-bold">{notification.fromUser.username}</span> unliked you.
											{:else if notification.type === NOTIFICATIONS_TYPES.PROFILE_VIEW}
												<span class="font-bold">{notification.fromUser.username}</span> viewed your profile.
											{/if}
										</span>
									</div>

									{#if !notification.read}
										<div class="mr-2 h-2 w-2 rounded-full bg-green-500">
											<p class="sr-only">Unread</p>
										</div>
									{/if}
								</button>
							</li>
						{/each}
					</ul>
				</div>
			{/if}
		</div>
	{:else}
		<div
			class="flex h-9 w-9 items-center justify-center rounded-full border border-2 border-gray-400 bg-gray-200"
		>
			<p class="sr-only">No new notifications</p>
			<img src="/icons/notifications/off.svg" alt="" class="w-5" />
		</div>
	{/if}
</div>
