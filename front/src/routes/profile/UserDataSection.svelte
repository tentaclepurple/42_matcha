<script lang="ts">
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import UserDataForm from './UserDataForm.svelte';
	import InterestsList from '$lib/components/InterestsList.svelte';

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
					<dt class="font-bold">Gender</dt>
					<dd>
						{userProfileData.value.gender}
						<GenderSymbol gender={userProfileData.value.gender} />
					</dd>
				</div>

				<div>
					<dt class="font-bold">Preference</dt>
					<dd>
						{userProfileData.value.sexualPreferences}
						<PreferenceSymbol preference={userProfileData.value.sexualPreferences} />
					</dd>
				</div>

				<div>
					<dt class="mb-1 font-bold">Interests</dt>
					<dd>
						{#if userProfileData.value.interests.length === 0}
							<span>No interests yet</span>
						{:else}
							<InterestsList
								interests={userProfileData.value?.interests}
								class="flex max-w-[500px] flex-wrap items-baseline gap-1"
							/>
						{/if}
					</dd>
				</div>

				<div>
					<dt class="font-bold">About me</dt>
					<dd class="max-w-xl">{userProfileData.value.biography}</dd>
				</div>
			</dl>
		{/if}
	</div>
{/if}
