<script lang="ts">
	interface RoundedAvatarProps {
		alt?: string;
		size?: 's' | 'm' | 'l';
		src: string;
	}

	const { alt = '', size, src }: RoundedAvatarProps = $props();

	let wrapperStyles = $state('');
	let pictureStyles = $state('');

	switch (size) {
		case 's':
			wrapperStyles = 'p-3';
			pictureStyles = 'w-6';
			break;
		case 'm':
			wrapperStyles = 'p-4';
			pictureStyles = 'w-12';
			break;
		case 'l':
			wrapperStyles = 'p-4';
			pictureStyles = 'w-16';
			break;
	}
</script>

<div
	class={`flex items-center justify-center rounded-full border-2 border-teal-500 bg-gray-200 ${wrapperStyles}`}
>
	<img {src} {alt} class={pictureStyles} />
</div>
