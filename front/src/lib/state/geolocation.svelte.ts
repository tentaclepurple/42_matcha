import { SERVER_BASE_URL } from '$lib/constants/api';

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
			navigator.geolocation.getCurrentPosition(async (position) => {
				this.#location = [position.coords.longitude, position.coords.latitude];
				console.log('User located', this.#location);

				const token = localStorage.getItem('access_token');

				const body = {
					location: {
						type: 'Point',
						coordinates: this.#location
					}
				};

				const res = await fetch(`${SERVER_BASE_URL}/api/profile/update_location`, {
					method: 'PUT',
					headers: {
						Authorization: `Bearer ${token}`,
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(body)
				});

				if (!res.ok) {
					console.error('Failed to update user location');
				}
			});
		}
	};
}
export const userLocation = new UserLocation();
