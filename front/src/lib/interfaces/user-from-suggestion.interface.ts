export default interface UserFromSuggestion {
	age: number;
	commonTags: number;
	commonTagsList: string[];
	distance: number;
	fameRating: number;
	gender: 'male' | 'female' | 'other';
	interests: string[];
	location: {
		type: 'Point';
		coordinates: [number, number];
	};
	profilePhoto: string;
	sexualPreference: 'male' | 'female' | 'bisexual';
	userId: string;
	username: string;
}
