// src/lib/stores/notificationStore.ts
import { writable } from 'svelte/store';

type Notification = {
    type: string;
    id: number;
    message: string;
};

export const notifications = writable<Notification[]>([]);
export const isCheckingInvitations = writable<boolean>(false);