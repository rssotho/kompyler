import mitt from 'mitt';

const emitter = mitt();

emitter.on('task-updated', (task) => {
  notificationStore.addNotification({
    id: Date.now(),
    type: 'info',
    title: 'Task Updated',
    message: `Task "${task?.title || 'Unknown'}" has been updated`
  });
});

emitter.on('member-deleted', (data) => {
  notificationStore.addNotification({
    id: Date.now(),
    type: 'warning',
    title: 'Team Member Removed',
    message: `Team member and ${data.taskCount} tasks have been removed`
  });
});

emitter.on('activity-created', (activity) => {
  notificationStore.addNotification({
    id: Date.now(),
    type: determineNotificationType(activity.type),
    title: getActivityTitle(activity.type),
    message: activity.title
  });
});

emitter.on('system-activity', (activity) => {
  notificationStore.addNotification({
    id: Date.now(),
    type: activity.type || 'info',
    title: getSystemActivityTitle(activity.type),
    message: activity.title
  });
});

function determineNotificationType(activityType) {
  const types = {
    task: 'info',
    member: 'success',
    comment: 'info',
    alert: 'warning',
    tip: 'info',
    update: 'success',
    evaluation: 'info',
    info: 'info',
    system: 'info'
  };
  return types[activityType] || 'info';
}

function getActivityTitle(activityType) {
  const titles = {
    task: 'Task Activity',
    member: 'Team Update',
    comment: 'New Comment',
    alert: 'System Alert',
    tip: 'Pro Tip',
    update: 'System Update',
    evaluation: 'Evaluation Update',
    info: 'System Info'
  };
  return titles[activityType] || 'New Activity';
}

function getSystemActivityTitle(type) {
  const titles = {
    info: 'System Information',
    tip: 'Productivity Tip',
    alert: 'Important Alert',
    update: 'System Update'
  };
  return titles[type] || 'System Notification';
}

function getDefaultMessage(type) {
  const messages = {
    task: 'Task status has been updated',
    member: 'Team member information has changed',
    alert: 'System alert has been triggered',
    tip: 'New system tip available',
    update: 'System has been updated',
    info: 'New system information available'
  };
  return messages[type] || 'New activity has been recorded';
}

export default emitter;
