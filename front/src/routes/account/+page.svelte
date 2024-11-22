<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import { userData } from '$lib/stores/user-data';
	import PersonalInfoForm from './PersonalInfoForm.svelte';
	import ProfileAvatar from './ProfileAvatar.svelte';

	userData.subscribe((value) => {
		if (!value) {
			return goto('/', { replaceState: true });
		}
	});
</script>

<PageWrapper>
	<h1>Account</h1>
	<p class="mb-6">This is where you can complete your profile</p>

	<div>
		<div class="flex flex-col items-start gap-4">
			<ProfileAvatar />
			<div>
				<h2 class="mb-4">Account information</h2>
				<PersonalInfoForm />
			</div>
		</div>
	</div>
</PageWrapper>
