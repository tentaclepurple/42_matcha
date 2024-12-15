import type { Gender } from './gender.type';
import type { Interest } from './interest.type';
import type Location from './location.interface';
import type { SexualPreference } from './sexual-preference.type';

export default interface UserFromSuggestion {
	age: number;
	commonTags: number;
	commonTagsList: string[];
	distance: number;
	fameRating: number;
	gender: Gender;
	interests: Interest[];
	location: Location;
	profilePhoto: string;
	sexualPreference: SexualPreference;
	userId: string;
	username: string;
}
