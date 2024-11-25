import { writable, type Writable } from 'svelte/store';

export const userLocation: Writable<null | [number, number]> = writable(null);

userLocation.subscribe((value) => {
	if (value) {
		console.log('User location updated', value);
	}
});

export const getUserLocation = async () => {
	if (navigator.geolocation) {
		console.log('Locating user…');
		navigator.geolocation.getCurrentPosition((position) => {
			userLocation.set([position.coords.latitude, position.coords.longitude]);
			console.log('User located', userLocation);
		});
	}
};
