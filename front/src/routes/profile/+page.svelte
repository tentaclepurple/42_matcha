<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import RoundedAvatar from '$lib/components/RoundedAvatar.svelte';
	import type UserData from '$lib/interfaces/user-data.interface';
	import { userData } from '$lib/stores/user-data';
	import getServerAsset from '$lib/utils/get-server-asset';

	let currentUserData: UserData;

	userData.subscribe((value) => {
		if (!value) {
			return goto('/', { replaceState: true });
		} else {
			currentUserData = value;
		}
	});
</script>

<PageWrapper>
	<h1>Profile</h1>
	<p class="mb-16">This is where you can complete your profile</p>

	<div>
		<div class="flex items-center gap-4">
			<RoundedAvatar src={getServerAsset(currentUserData.profilePhoto)} alt="" size="l" />
			<div>
				<p class="mb-3">{currentUserData.username}</p>
				<h2>{currentUserData.firstName} {currentUserData.lastName}</h2>
				<p>{currentUserData.email}</p>
			</div>
		</div>
		<Button type="button" level="primary" class="mt-8">Edit password</Button>
	</div>
</PageWrapper>
