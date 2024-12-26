import type { Gender } from './gender.type';
import type { Interest } from './interest.type';
import type Location from './location.interface';
import type Photo from './photo.interface';
import type { SexualPreference } from './sexual-preference.type';

interface Like {
	createdAt: string;
	userId: string;
	username: string;
}
export default interface UserProfileData {
	age: number;
	biography: string;
	fameRating: number;
	location: Location;
	gender: Gender;
	interests: Interest[];
	likesReceived: Like[];
	photos: Photo[];
	sexualPreferences: SexualPreference;
	username: string;
}
