<script lang="ts">
	import { goto } from '$app/navigation';
	import RoundedAvatar from '$lib/components/RoundedAvatar.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import { AVATAR_MAX_SIZE } from '$lib/constants/files';
	import type UserData from '$lib/interfaces/user-data.interface';
	import getServerAsset from '$lib/utils/get-server-asset';

	export let currentUserData: UserData;
	let error = '';

	const handleEditAvatar = async (e) => {
		error = '';

		const { files } = e.target;
		const file = files[0];

		if (!file) {
			error = 'Something went wrong. Please try again.';
			return;
		}

		if (file.size > AVATAR_MAX_SIZE) {
			error = 'File is too large. Try again with a smaller file.';
			return;
		}

		const formData = new FormData();
		formData.append('photo', file);

		const token = localStorage.getItem('access_token');
		if (!token) {
			goto('/login', { replaceState: true });
		}

		try {
			const res = await fetch(`${SERVER_BASE_URL}/api/profile/update_photo/1`, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${localStorage.getItem('token')}`,
					'Content-Type': 'multipart/form-data'
				},
				body: formData
			});

			console.log('ciao', res);

			const data = await res.json();
			console.log(data);
		} catch (err) {
			console.error(err);
			error = 'An error occurred. Please try again later.';
		}
	};
</script>

<h2>Avatar</h2>
<div class="gap-42 flex max-w-sm items-center gap-4">
	<RoundedAvatar src={getServerAsset(currentUserData.profilePhoto)} alt="" size="l" />
	<div>
		<fieldset class="flex flex-col items-start gap-4">
			<label
				class="cursor-pointer rounded border border-teal-500 bg-transparent px-4 py-2 font-semibold text-teal-700 hover:border-transparent hover:bg-teal-500 hover:text-white"
			>
				Change avatar
				<input
					type="file"
					id="photo"
					name="photo"
					accept="image/png, image/jpeg"
					class="sr-only"
					onchange={handleEditAvatar}
				/>
			</label>
			<p class="text-sm">
				Double-check that the image is in PNG or JPG format and that it does not exceed 5 MB.
			</p>
		</fieldset>
	</div>
</div>
{#if error}
	<p class="mt-4 text-red-500">{error}</p>
{/if}
