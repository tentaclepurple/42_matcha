class UserLocation {
	#location = $state<null | [number, number]>(null);

	get value(): null | [number, number] {
		return this.#location;
	}

	set value(newValue: null | [number, number]) {
		this.#location = newValue;
	}

	getUserLocation = async () => {
		if (navigator.geolocation) {
			console.log('Locating user…');
			navigator.geolocation.getCurrentPosition((position) => {
				this.#location = [position.coords.longitude, position.coords.latitude];
				console.log('User located', this.#location);
			});
		}
	};
}
export const userLocation = new UserLocation();
