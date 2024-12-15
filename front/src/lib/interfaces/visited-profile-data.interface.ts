import type { Interest } from './interest.type';
import type Location from './location.interface';
import type Photo from './photo.interface';

export default interface VisitedProfileData {
	age: number;
	biography: string;
	blockedUsers: string[];
	createdAt: string;
	fameRating: number;
	firstName: string;
	gender: string;
	interests: Interest[];
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
	location: Location;
	online: boolean;
	photos: Photo[];
	profileCompleted: boolean;
	reported: boolean;
	sexualPreferences: string;
	userId: string;
	username: string;
	verified: boolean;
}
