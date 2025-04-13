import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import notificationMixin from './mixins/notificationMixin';

const app = createApp(App);

// Add error handler
app.config.errorHandler = (err, vm, info) => {
  console.error('Global error:', err);
  console.error('Component:', vm);
  console.error('Info:', info);
};

// Add the notification mixin globally
app.mixin(notificationMixin);

app.use(router);
app.mount('#app');
