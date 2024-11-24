<script lang="ts">
	import { GENDER_OPTIONS } from '$lib/constants/user-profile-data';

	type Gender = (typeof GENDER_OPTIONS)[keyof typeof GENDER_OPTIONS];

	export let gender: Gender;

	const getGenderSymbol = (gender: Gender): string => {
		switch (gender) {
			case GENDER_OPTIONS.MALE:
				return '♂';
			case GENDER_OPTIONS.FEMALE:
				return '♀';
			case GENDER_OPTIONS.OTHER:
			default:
				return '⚧';
		}
	};
</script>

<span>{getGenderSymbol(gender)}</span>
