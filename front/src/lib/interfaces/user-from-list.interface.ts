export default interface UserFromList {
	age: number;
	distance: number;
	fameRating: number;
	interests: string[];
	location: {
		type: 'Point';
		coordinates: [number, number];
	};
	profilePhoto: string;
	userId: string;
	username: string;
}
