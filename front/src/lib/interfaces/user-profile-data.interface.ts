export default interface UserProfileData {
	age: number;
	photos: {
		is_profile: boolean;
		uploaded_at: string;
		url: string;
	}[];
	username: string;
}
