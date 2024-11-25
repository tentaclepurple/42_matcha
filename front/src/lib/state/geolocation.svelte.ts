class UserLocation {
	private _location = $state<null | [number, number]>(null);

	get value(): null | [number, number] {
		return this._location;
	}

	set value(newValue: null | [number, number]) {
		this._location = newValue;
	}

	getUserLocation = async () => {
		if (navigator.geolocation) {
			console.log('Locating user…');
			navigator.geolocation.getCurrentPosition((position) => {
				this._location = [position.coords.latitude, position.coords.longitude];
				console.log('User located', this._location);
			});
		}
	};
}
export const userLocation = new UserLocation();