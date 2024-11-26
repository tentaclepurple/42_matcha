import { writable, type Writable } from 'svelte/store';

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
		this.#isAuthenticated = false;
	}
}

export const userAuth = new UserAuth();
