<script lang="ts">
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import GenderSymbol from './GenderSymbol.svelte';
	import PreferenceSymbol from './PreferenceSymbol.svelte';
	import UserDataForm from './UserDataForm.svelte';

	let isEditing: boolean = $state(false);
</script>

{#if userProfileData?.value}
	<div class="relative flex min-w-full flex-col justify-center rounded-lg bg-teal-100 px-12 py-6">
		{#if !isEditing}
			<button
				type="button"
				aria-label="Edit"
				onclick={() => (isEditing = !isEditing)}
				class="absolute right-6 top-6 h-9 w-9 rounded-md bg-teal-600 p-2 hover:bg-teal-700 disabled:cursor-not-allowed disabled:bg-gray-300"
			>
				<img src="/icons/edit.svg" alt="" class="w-full" />
			</button>
		{/if}
		{#if isEditing}
			<UserDataForm
				onSuccess={() => {
					isEditing = false;
				}}
				onCancel={() => {
					isEditing = false;
				}}
			/>
		{:else}
			<dl class="flex flex-col gap-3">
				<div>
					<dt class="font-bold">About me</dt>
					<dd class="max-w-xl">{userProfileData.value.biography}</dd>
				</div>

				<div class="flex items-baseline gap-2">
					<dt class="font-bold">Gender:</dt>
					<dd>
						{userProfileData.value.gender}
						<GenderSymbol gender={userProfileData.value.gender} />
					</dd>
				</div>

				<div class="flex items-baseline gap-2">
					<dt class="font-bold">Interested in:</dt>
					<dd>
						{userProfileData.value.sexualPreference}
						<PreferenceSymbol preference={userProfileData.value.sexualPreference} />
					</dd>
				</div>
			</dl>
		{/if}
	</div>
{/if}
