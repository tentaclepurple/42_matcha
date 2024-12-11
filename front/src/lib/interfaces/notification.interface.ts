export default interface Notification {
	id: string;
	createdAt: string;
	fromUser: {
		id: string;
		username: string;
	};
	read: boolean;
	type: string;
}
