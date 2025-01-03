import type { Gender } from './gender.type';
import type { Interest } from './interest.type';
import type Location from './location.interface';
import type Photo from './photo.interface';
import type { SexualPreference } from './sexual-preference.type';

export interface Like {
	createdAt: string;
	userId: string;
	username: string;
}

export interface View {
	lastView: string;
	userId: string;
	username: string;
	viewCount: number;
}

export interface BlockedUser {
	profilePhoto: string;
	userId: string;
	username: string;
}

export default interface UserProfileData {
	age: number;
	biography: string;
	blockedUsers: BlockedUser[];
	fameRating: number;
	location: Location;
	gender: Gender;
	interests: Interest[];
	likesReceived: Like[];
	photos: Photo[];
	profileViews: View[];
	sexualPreferences: SexualPreference;
	username: string;
}
