import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import notificationMixin from './mixins/notificationMixin';

// Import DataTables
import "datatables.net-dt/css/dataTables.dataTables.css";

import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';

// Import Bootstrap
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

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
