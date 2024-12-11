<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';

	import { page } from '$app/stores';
	import VisitedUserProfile from './VisitedUserProfile.svelte';

	const username = $page.params.username;
	const origin = $page.url.searchParams.get('origin');
</script>

<PageWrapper>
	<div class="flex flex-col items-center justify-center">
		<h1>Profile of {username}</h1>
		<VisitedUserProfile {origin} />
	</div>
</PageWrapper>
