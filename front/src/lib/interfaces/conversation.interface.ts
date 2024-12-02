export default interface Conversation {
	lastMessage: {
		content: string;
		createdAt: string;
		fromMe: boolean;
		read: boolean;
		type: 'text';
	};
	unreadCount: 0;
	user: {
		lastConnection: string;
		online: boolean;
		profilePhoto: string;
		userId: string;
		username: string;
	};
}
