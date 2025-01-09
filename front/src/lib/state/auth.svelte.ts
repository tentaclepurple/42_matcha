import { writable, type Writable } from 'svelte/store';
import { SERVER_BASE_URL } from '$lib/constants/api';
import { userLocation } from './geolocation.svelte';

export const isAuthenticated: Writable<boolean> = writable(false);

class UserAuth {
	#isAuthenticated = $state<boolean>(false);

	get isAuthenticated(): boolean {
		return this.#isAuthenticated;
	}

	login(): void {
		this.#isAuthenticated = true;
	}

	logout(): void {
		const accessToken = localStorage.getItem('access_token');

		if (accessToken) {
			fetch(`${SERVER_BASE_URL}/api/users/logout`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${localStorage.getItem('access_token')}`
				}
			});

			localStorage.clear();
			userLocation.value = null;
		}

		this.#isAuthenticated = false;
	}
}

export const userAuth = new UserAuth();
