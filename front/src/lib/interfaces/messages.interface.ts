export default interface Messages {
	messages: {
		content: string;
		createdAt: string;
		fromMe: boolean;
	}[];
	otherUser: {
		lastConnection: string;
		online: boolean;
		userId: string;
		username: string;
		profilePhoto: string;
	};
}
