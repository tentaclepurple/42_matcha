export default interface UserProfileData {
	age: number;
	biography: string;
	gender: 'male' | 'female' | 'other';
	photos: {
		is_profile: boolean;
		uploaded_at: string;
		url: string;
	}[];
	sexualPreference: 'male' | 'female' | 'bisexual';
	username: string;
}
