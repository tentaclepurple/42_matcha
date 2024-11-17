<script lang="ts">
	import { page } from '$app/stores';
	const error = $page.url.searchParams.get('error');

	let title = '';
	let message = '';

	switch (error) {
		case 'invalid-verification-link':
			title = 'Verification link is invalid or expired';
			message =
				'If you already verified your email, you can login now. Otherwise, please request a new verification link.';
			break;
		default:
			title = 'Ops! Something went wrong';
			message = 'An error occurred. Please try again later.';
	}
</script>

<div class="error-page">
	<h1>{title}</h1>
	<p>{message}</p>
</div>
