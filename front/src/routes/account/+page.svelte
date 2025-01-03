<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userData } from '$lib/state/user-data.svelte';
	import PersonalInfoForm from './PersonalInfoForm.svelte';
	import ProfileAvatar from './ProfileAvatar.svelte';

	$effect(() => {
		if (!userData.value) {
			goto('/matcha/', { replaceState: true });
		}
	});
</script>

<PageWrapper>
	<header class="mb-6">
		<h1>Account</h1>
		<p>This is where you can handle your account information.</p>
		<p>Looking for your profile info? Go to the <a href="/matcha/profile">Profile page</a>.</p>
	</header>

	<div class="flex flex-col items-start gap-4">
		<ProfileAvatar />
		<div class="w-full sm:w-auto">
			<h2 class="mb-4">Your personal information</h2>
			<PersonalInfoForm />
		</div>
	</div>
</PageWrapper>
