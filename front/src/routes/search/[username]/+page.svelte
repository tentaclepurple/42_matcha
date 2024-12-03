<script>
	import PageWrapper from '$lib/components/PageWrapper.svelte';

	import { page } from '$app/stores';
	import SelectUserProfile from './SelectUserProfile.svelte';

	const username = $page.params.username;
	const origin = $page.url.searchParams.get('origin');

	const { selectedUser } = $page.data;
</script>

<PageWrapper>
	<div class="flex flex-col justify-center items-center">
		<h1>Profile of {username}</h1>
		<SelectUserProfile {selectedUser} {origin} />
	</div>
</PageWrapper>
