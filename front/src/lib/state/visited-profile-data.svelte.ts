import { SERVER_BASE_URL } from '$lib/constants/api';
import type VisitedProfileData from '$lib/interfaces/visited-profile-data.interface';
import deserialize from '$lib/utils/deserialize';

class VisitedProfileDataClass {
	#value = $state<VisitedProfileData | null>(null);

	get value(): VisitedProfileData | null {
		return this.#value;
	}

	set value(newValue: VisitedProfileData | null) {
		this.#value = newValue;
	}

	fetch = async (username: string) => {
		const token = localStorage.getItem('access_token');
		if (!token) {
			throw new Error('No token found');
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
			throw new Error('Failed to fetch user data');
		}

		const data = await res.json();
		const selectedUser: VisitedProfileData = deserialize(data);

		if (!selectedUser) {
			throw new Error('Failed to fetch user data');
		}

		this.#value = selectedUser;
	};
}

export const visitedProfileData = new VisitedProfileDataClass();
