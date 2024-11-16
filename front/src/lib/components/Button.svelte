<script lang="ts">
	type ButtonType = 'button' | 'submit' | 'reset';
	type ButtonLevel = 'primary' | 'secondary';

	let {
		children,
		level = 'primary' as ButtonLevel,
		type = 'button' as ButtonType,
		...restProps
	} = $props();

	let styles =
		level === 'primary'
			? 'rounded bg-green-500 px-4 py-2 font-bold text-white hover:bg-green-700'
			: 'bg-transparent hover:bg-green-500 text-green-700 font-semibold hover:text-white py-2 px-4 border border-green-500 hover:border-transparent rounded';
</script>

<button {type} {...restProps} class={styles}>
	{@render children()}
</button>
