export default interface VisitedProfileData {
	age: number;
	biography: string;
	blockedUsers: string[];
	createdAt: string;
	fameRating: number;
	firstName: string;
	gender: string;
	interests: string[];
	isOwnProfile: boolean;
	lastConnection: string;
	lastName: string;
	likeInfo: {
		isMatch: boolean;
		likedByMe: boolean;
		likesMe: boolean;
		unlikedByMe: boolean;
		unlikesMe: boolean;
	};
	location: {
		coordinates: [number, number];
		type: 'Point';
	};
	online: boolean;
	photos: {
		isProfile: boolean;
		uploadedAt: string;
		url: string;
	}[];
	profileCompleted: boolean;
	reported: boolean;
	sexualPreferences: string;
	userId: string;
	username: string;
	verified: boolean;
}
