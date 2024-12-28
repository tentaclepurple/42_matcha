<script lang="ts">
	import ButtonSelector from '$lib/components/ButtonSelector.svelte';
	import GenderSymbol from '$lib/components/GenderSymbol.svelte';
	import PreferenceSymbol from '$lib/components/PreferenceSymbol.svelte';
	import { userProfileData } from '$lib/state/user-profile-data.svelte';
</script>

{#if userProfileData.value}
	<div class="mb-2 flex flex-wrap items-center gap-2 px-4">
		<ButtonSelector class="cursor-not-allowed opacity-75">
			<label>
				Gender:
				<select disabled class="cursor-not-allowed">
					<option selected>
						{userProfileData.value.gender}
						<GenderSymbol gender={userProfileData.value.gender} />
					</option>
				</select>
			</label>
		</ButtonSelector>

		<ButtonSelector class="cursor-not-allowed opacity-75">
			<label>
				Likes:
				<select disabled class="cursor-not-allowed">
					<option selected>
						{userProfileData.value.sexualPreferences}
						<PreferenceSymbol preference={userProfileData.value.sexualPreferences} />
					</option>
				</select>
			</label>
		</ButtonSelector>
	</div>
{/if}
