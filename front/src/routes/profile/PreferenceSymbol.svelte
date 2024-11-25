<script lang="ts">
	import { PREFERENCES_OPTIONS } from '$lib/constants/user-profile-data';

	type Preferences = (typeof PREFERENCES_OPTIONS)[keyof typeof PREFERENCES_OPTIONS];

	const { preference }: { preference: Preferences } = $props();

	const getPreferencesSymbol = (preference: Preferences): string => {
		switch (preference) {
			case PREFERENCES_OPTIONS.MALE:
				return '♂';
			case PREFERENCES_OPTIONS.FEMALE:
				return '♀';
			case PREFERENCES_OPTIONS.BISEXUAL:
			default:
				return '⚥';
		}
	};
</script>

<span>{getPreferencesSymbol(preference)}</span>
