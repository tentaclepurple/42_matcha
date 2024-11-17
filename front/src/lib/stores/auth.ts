import { writable, type Writable } from 'svelte/store';

export const isAuthenticated: Writable<boolean> = writable(false);

export function login(): void {
	isAuthenticated.set(true);
}

export function logout(): void {
	isAuthenticated.set(false);
}
