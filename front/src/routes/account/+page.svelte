<script lang="ts">
	import { goto } from '$app/navigation';
	import PageWrapper from '$lib/components/PageWrapper.svelte';
	import type UserData from '$lib/interfaces/user-data.interface';
	import { userData } from '$lib/stores/user-data';
	import PersonalInfoForm from './PersonalInfoForm.svelte';
	import ProfileAvatar from './ProfileAvatar.svelte';

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
	<h1>Account</h1>
	<p class="mb-6">This is where you can complete your profile</p>

	<div>
		<div class="flex flex-col items-start gap-4">
			<ProfileAvatar {currentUserData} />
			<div>
				<h2 class="mb-4">Account information</h2>
				<PersonalInfoForm {currentUserData} />
			</div>
		</div>
	</div>
</PageWrapper>
