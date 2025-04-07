import { reactive } from 'vue'

export const notificationStore = reactive({
  notifications: [],
  lastNotificationTime: 0,
  
  addNotification(notification) {
    const now = Date.now();
    
    // Check if enough time has passed since last notification (2 minutes)
    if (now - this.lastNotificationTime < 120000) {
      return;
    }

    const notificationWithTime = {
      ...notification,
      timestamp: now
    }
    
    this.notifications.unshift(notificationWithTime);
    this.lastNotificationTime = now;
    
    // Keep only last 5 notifications
    if (this.notifications.length > 5) {
      this.notifications.pop();
    }

    // Auto-remove after 8 seconds to give more time to read
    setTimeout(() => {
      this.removeNotification(notification.id);
    }, 8000);
  },

  removeNotification(id) {
    const index = this.notifications.findIndex(n => n.id === id)
    if (index > -1) {
      this.notifications.splice(index, 1)
    }
  }
})
