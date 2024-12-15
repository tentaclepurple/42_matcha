import type { Interest } from './interest.type';
import type Location from './location.interface';

export default interface UserFromList {
	age: number;
	distance: number;
	fameRating: number;
	interests: Interest[];
	location: Location;
	profilePhoto: string;
	userId: string;
	username: string;
}
