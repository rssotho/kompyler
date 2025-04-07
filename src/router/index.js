import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/create-task',
    name: 'CreateTask',
    component: () => import('@/views/CreateTask.vue')
  },
  {
    path: '/evaluate-task',
    name: 'EvaluateTask',
    component: () => import('@/views/EvaluateTask.vue')
  },
  {
    path: '/view-evaluations',
    name: 'ViewEvaluations',
    component: () => import('@/views/ViewEvaluations.vue')
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

// Add navigation guard to handle component loading errors
router.onError((error) => {
  if (error.message.includes('Failed to fetch dynamically imported module')) {
    window.location.reload();
  }
});

export default router;
