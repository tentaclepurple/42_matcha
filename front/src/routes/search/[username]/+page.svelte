<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';

	import { page } from '$app/stores';
	import VisitedUserProfile from './VisitedUserProfile.svelte';
	import { notificationsData } from '$lib/state/notifications.svelte';
	import { visitedProfileData } from '$lib/state/visited-profile-data.svelte';
	import { beforeNavigate } from '$app/navigation';

	const username = $page.params.username;
	const origin = $page.url.searchParams.get('origin');

	$effect(() => {
		if (notificationsData.value) {
			visitedProfileData.fetch(username);
		}
	});

	beforeNavigate(() => {
		visitedProfileData.value = null;
	});
</script>

<PageWrapper>
	<div class="flex flex-col items-center justify-center">
		<h1 class="sr-only">Profile of {username}</h1>
		<VisitedUserProfile {origin} />
	</div>
</PageWrapper>
