// src/lib/services/NotificationService.ts

// src/lib/services/NotificationService.ts
const SERVER_BASE_URL = 'http://localhost:5000';

const NotificationService = {
    checkInvitationInterval: null as NodeJS.Timer | null,

    startCheckingInvitations() {
        this.checkInvitations();
        this.checkInvitationInterval = setInterval(() => {
            this.checkInvitations();
        }, 5000);
    },

    stopCheckingInvitations() {
        if (this.checkInvitationInterval) {
            clearInterval(this.checkInvitationInterval);
            this.checkInvitationInterval = null;
        }
    },

    async checkInvitations() {
        const token = localStorage.getItem('access_token');
        if (!token) return;

        try {
            const response = await fetch(`${SERVER_BASE_URL}/api/notifications/unread`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Error checking notifications');
            }

            const data = await response.json();
            console.log('Notificaciones sin leer:', data);
            
        } catch (error) {
            console.error('Error checking notifications:', error);
        }
    }
};

export default NotificationService;