import type { Gender } from './gender.type';
import type { Interest } from './interest.type';
import type Location from './location.interface';
import type { SexualPreference } from './sexual-preference.type';

export default interface UserFromList {
	age: number;
	distance: number;
	fameRating: number;
	gender: Gender;
	interests: Interest[];
	location: Location;
	profilePhoto: string;
	sexualPreferences: SexualPreference;
	userId: string;
	username: string;
}
