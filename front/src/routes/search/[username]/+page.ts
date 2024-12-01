import { error } from '@sveltejs/kit';
import type { PageLoad } from '../$types';
import { SERVER_BASE_URL } from '$lib/constants/api';
import deserialize from '$lib/utils/deserialize';

export const ssr = false;

export const load: PageLoad = async ({ params }) => {
	const username = params.username;

	if (!username) {
		error(404, 'User not found');
	}

	const token = localStorage.getItem('access_token');
	if (!token) {
		error(401, 'Unauthorized');
	}

	const res = await fetch(`${SERVER_BASE_URL}/api/profile/profile_info/${username}`, {
		method: 'GET',
		headers: {
			Authorization: `Bearer ${token}`,
			'Content-Type': 'application/json'
		}
	});

	if (!res.ok) {
		console.error('Failed to fetch user data');
		error(500, 'Failed to fetch user data');
	}

	const data = await res.json();
	const selectedUser = deserialize(data);

	if (!selectedUser) {
		error(404, 'User not found');
	}

	return {
		selectedUser
	};
};
