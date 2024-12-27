<script lang="ts">
	import type { FullAutoFill } from 'svelte/elements';

	interface PasswordInputProps {
		id: string;
		name: string;
		value?: string;
		required?: boolean;
		autocomplete?: FullAutoFill;
		class?: string;
		placeholder?: string;
	}

	let {
		id,
		name,
		value,
		required,
		autocomplete,
		class: CLASS,
		placeholder,
		...restProps
	}: PasswordInputProps = $props();

	let showPassword = $state(false);

	const handleShowPassword = () => {
		showPassword = !showPassword;
	};
</script>

<div class={`flex items-baseline justify-center gap-4 ${CLASS}`}>
	<input
		type={showPassword ? 'text' : 'password'}
		{id}
		{name}
		{required}
		{value}
		{autocomplete}
		{placeholder}
		class={CLASS}
		{...restProps}
	/>
	<button
		type="button"
		onclick={handleShowPassword}
		aria-label={showPassword ? 'Hide password' : 'Show password'}
	>
		{showPassword ? '🔒' : '👁️'}
	</button>
</div>
