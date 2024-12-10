export default interface Notification {
	_id: string;
	createdAt: string;
	fromUser: {
		_id: string;
		username: string;
	};
	read: boolean;
	type: string;
}
