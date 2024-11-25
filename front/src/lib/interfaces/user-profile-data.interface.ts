export default interface UserProfileData {
	age: number;
	biography: string;
	fameRating: number;
	location: {
		type: 'Point';
		coordinates: [number, number];
	};
	gender: 'male' | 'female' | 'other';
	photos: {
		is_profile: boolean;
		uploaded_at: string;
		url: string;
	}[];
	sexualPreference: 'male' | 'female' | 'bisexual';
	username: string;
}
