<script lang="ts">
	export let id: string;
	export let name: string;
	export let value: string | undefined;
	export let required: boolean;

	let showPassword = false;

	const handleShowPassword = () => {
		showPassword = !showPassword;
	};
</script>

<div class="flex items-baseline justify-center gap-4">
	<input type={showPassword ? 'text' : 'password'} {id} {name} {required} {value} />
	<button
		type="button"
		onclick={handleShowPassword}
		aria-label={showPassword ? 'Hide password' : 'Show password'}
	>
		{showPassword ? '🔒' : '👁️'}
	</button>
</div>
