<script lang="ts">
	interface RoundAvatarProps {
		alt?: string;
		size?: 's' | 'm' | 'l';
		src: string;
	}

	const { alt = '', size, src }: RoundAvatarProps = $props();

	let wrapperStyles = $state('');
	let pictureStyles = $state('');

	switch (size) {
		case 's':
			wrapperStyles = 'p-0';
			pictureStyles = 'min-w-12 w-12';
			break;
		case 'm':
			wrapperStyles = 'p-0';
			pictureStyles = 'min-w-20 w-20';
			break;
		case 'l':
			wrapperStyles = 'p-0';
			pictureStyles = 'min-w-36 w-36';
			break;
	}
</script>

<div
	class={`flex items-center justify-center rounded-full border-2 border-teal-500 bg-gray-200 ${wrapperStyles} shrink-0 overflow-hidden`}
>
	<img {src} {alt} class={`${pictureStyles} aspect-square`} />
</div>
