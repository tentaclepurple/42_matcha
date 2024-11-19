<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import RoundedAvatar from '$lib/components/RoundedAvatar.svelte';
	import getServerAsset from '$lib/utils/get-server-asset';

	interface ProfileData {
		profilePictureUrl: string;
		firstName: string;
		lastName: string;
		username: string;
		email: string;
	}

	let { data }: { data: ProfileData } = $props();
</script>

<PageWrapper>
	<h1>Profile</h1>
	<p class="mb-16">This is where you can complete your profile</p>

	<div>
		<div class="flex items-center gap-4">
			<RoundedAvatar src={getServerAsset(data.profilePictureUrl)} alt="" size="l" />
			<div>
				<p class="mb-3">{data.username}</p>
				<h2>{data.firstName} {data.lastName}</h2>
				<p>{data.email}</p>
			</div>
		</div>
		<Button type="button" level="primary" class="mt-8">Edit password</Button>
	</div>
</PageWrapper>
