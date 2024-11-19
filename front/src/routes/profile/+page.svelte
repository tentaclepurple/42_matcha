<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
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
			<div class="rounded-full border-2 border-teal-500 p-4">
				<img src={getServerAsset(data.profilePictureUrl)} alt="" class="w-16" />
			</div>
			<div>
				<h2>{data.firstName} {data.lastName}</h2>
				<p>{data.username}</p>
				<p>{data.email}</p>
			</div>
		</div>
		<Button type="button" level="primary" class="mt-8">Edit password</Button>
	</div>
</PageWrapper>
