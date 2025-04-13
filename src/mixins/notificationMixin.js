

export default {
  mounted() {
    // Only show route change notification if coming from a different route
    const previousRoute = sessionStorage.getItem('currentRoute');
    const currentRoute = this.$route.name;
    
    if (previousRoute !== currentRoute) {
      notificationStore.addNotification({
        id: Date.now(),
        type: 'info',
        title: 'Navigation',
        message: `Viewing ${currentRoute}`
      });
      
      sessionStorage.setItem('currentRoute', currentRoute);
    }
  }
}
