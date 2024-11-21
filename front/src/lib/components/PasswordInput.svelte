<script lang="ts">
	import type { FullAutoFill } from 'svelte/elements';

	interface PasswordInputProps {
		id: string;
		name: string;
		value?: string;
		required?: boolean;
		autocomplete?: FullAutoFill;
	}

	let { id, name, value, required, autocomplete }: PasswordInputProps = $props();

	let showPassword = $state(false);

	const handleShowPassword = () => {
		showPassword = !showPassword;
	};
</script>

<div class="flex items-baseline justify-center gap-4">
	<input type={showPassword ? 'text' : 'password'} {id} {name} {required} {value} {autocomplete} />
	<button
		type="button"
		onclick={handleShowPassword}
		aria-label={showPassword ? 'Hide password' : 'Show password'}
	>
		{showPassword ? '🔒' : '👁️'}
	</button>
</div>
