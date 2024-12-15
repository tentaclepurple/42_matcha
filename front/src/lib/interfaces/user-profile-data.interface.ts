import type { Gender } from './gender.type';
import type { Interest } from './interest.type';
import type Location from './location.interface';
import type { SexualPreference } from './sexual-preference.type';

export default interface UserProfileData {
	age: number;
	biography: string;
	fameRating: number;
	location: Location;
	gender: Gender;
	interests: Interest[];
	photos: {
		is_profile: boolean;
		uploaded_at: string;
		url: string;
	}[];
	sexualPreference: SexualPreference;
	username: string;
}
