<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/Button.svelte';
	import { SERVER_BASE_URL } from '$lib/constants/api';
	import Modal from './Modal.svelte';

	const { selectedUser } = $props();

	let showReportModal = $state(false);
	let showBlockModal = $state(false);

	const handleOpenReportModal = () => {
		showReportModal = true;
	};

	const handleOpenBlockModal = () => {
		showBlockModal = true;
	};

	const handleBlock = async () => {
		if (!selectedUser) return;

		const token = localStorage.getItem('access_token');

		try {
			const res = await fetch(
				`${SERVER_BASE_URL}/api/interactions/block/${selectedUser.username}`,
				{
					method: 'POST',
					headers: {
						Authorization: `Bearer ${token}`,
						'Content-Type': 'application/json'
					}
				}
			);

			if (!res.ok) {
				throw new Error('Failed to block user');
			}

			goto('/search');
		} catch (error) {
			console.error(error);
		}
	};

	const handleReport = async () => {
		if (!selectedUser) return;

		const token = localStorage.getItem('access_token');

		try {
			const blockRes = await fetch(
				`${SERVER_BASE_URL}/api/interactions/block/${selectedUser.username}`,
				{
					method: 'POST',
					headers: {
						Authorization: `Bearer ${token}`,
						'Content-Type': 'application/json'
					}
				}
			);

			if (!blockRes.ok) {
				throw new Error('Failed to block user');
			}

			const reportRes = await fetch(
				`${SERVER_BASE_URL}/api/interactions/report/${selectedUser.username}`,
				{
					method: 'POST',
					headers: {
						Authorization: `Bearer ${token}`,
						'Content-Type': 'application/json'
					}
				}
			);

			if (!reportRes.ok) {
				throw new Error('Failed to report user');
			}

			goto('/search');
		} catch (error) {
			console.error(error);
		}
	};
</script>

<div>
	<h2 class="title-3 mb-2">Having issue with this user?</h2>
	<p class="mb-1 text-sm">
		Matcha is a safe place for everyone. If you have any issue with this user, block them to prevent
		any further interaction.
	</p>
	<p class="mb-8 text-sm">
		If you noticed any inappropriate or harmful behavior, please report this user to our team.
	</p>
	<div class="flex items-center justify-center sm:justify-end gap-2">
		<Button level="danger" type="button" onclick={handleOpenReportModal}>Report user</Button>
		<Button level="secondary" type="button" onclick={handleOpenBlockModal}>Block user</Button>
	</div>
</div>

{#snippet Reason({
	label,
	value,
	checked = false
}: {
	label: string;
	value: string;
	checked?: boolean;
})}
	<label class="flex items-center gap-2 text-sm">
		<input name="reason" type="radio" {value} {checked} />
		{label}
	</label>
{/snippet}

{#if showReportModal}
	<Modal
		confirmLabel="Report user"
		onClose={() => (showReportModal = false)}
		onConfirm={handleReport}
		title="Are you sure you want to report this user?"
	>
		<p class="mb-1">Our team will review your report and take appropriate action if necessary.</p>
		<p class="mb-4">
			Also, the user will be blocked from your profile to prevent any further interaction.
		</p>

		<fieldset>
			<legend class="mb-2">Select a reason to report this user:</legend>

			<div class="flex flex-col gap-1">
				{@render Reason({ label: 'Harmful behavior', value: 'harmful' })}

				{@render Reason({ label: 'Inappropriate content', value: 'inappropriate' })}

				{@render Reason({ label: 'Pretending to be someone else', value: 'pretending' })}

				{@render Reason({ label: 'Other', value: 'other', checked: true })}
			</div>
		</fieldset>
	</Modal>
{/if}

{#if showBlockModal}
	<Modal
		confirmLabel="Block user"
		onClose={() => (showBlockModal = false)}
		onConfirm={handleBlock}
		title="Are you sure you want to block this user?"
	>
		<p class="mb-1">
			You will no longer see their profile and you will not be able to interact with them.
		</p>
		<p>
			If you want to unblock them, you will be able to do so in your profile settings at any time.
		</p>
	</Modal>
{/if}
