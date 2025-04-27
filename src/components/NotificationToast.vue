<template>
</template>

<script>
export default {
  name: 'NotificationToast',
  props: {
    type: {
      type: String,
      default: 'info'
    },
    title: {
      type: String,
      required: true
    },
    message: {
      type: String,
      required: true
    }
  },
  computed: {
    icon() {
      const icons = {
        task: 'fas fa-tasks',
        member: 'fas fa-user',
        delete: 'fas fa-trash',
        success: 'fas fa-check-circle',
        error: 'fas fa-times-circle',
        warning: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
      };
      return icons[this.type] || icons.info;
    }
  }
};
</script>

<style scoped>
.notification {
  pointer-events: auto;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: #1a1a1a;
  border: 1px solid rgba(141, 0, 0, 0.519);
  border-left: 4px solid #ff0000;
  padding: 16px;
  border-radius: 8px;
  min-width: 300px;
  max-width: 400px;
  margin-bottom: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.notification.task { border-left-color: #ff0000; }
.notification.member { border-left-color: #10b981; }
.notification.delete { border-left-color: #ef4444; }
.notification.success { border-left-color: #10b981; }
.notification.error { border-left-color: #ef4444; }
.notification.warning { border-left-color: #f59e0b; }
.notification.info { border-left-color: #3b82f6; }

.notification-icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-content {
  flex-grow: 1;
}

.notification-title {
  font-weight: 600;
  margin: 0 0 4px 0;
  color: #ffffff;
}

.notification-message {
  margin: 0;
  font-size: 0.875rem;
  color: #9ca3af;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.notification-toast {
  background: #333;
  color: #fff;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}
</style>
