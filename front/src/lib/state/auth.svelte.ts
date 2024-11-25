import { writable, type Writable } from 'svelte/store';

export const isAuthenticated: Writable<boolean> = writable(false);

class UserAuth {
	private _isAuthenticated = $state<boolean>(false);

	get isAuthenticated(): boolean {
		return this._isAuthenticated;
	}

	login(): void {
		this._isAuthenticated = true;
	}

	logout(): void {
		this._isAuthenticated = false;
	}
}

export const userAuth = new UserAuth();
