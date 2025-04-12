import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('@/views/login.vue')
  },
  {
    path: '/dashboard',
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
  },
  {
    path: '/landing-page',
    name: 'landingPage',
    component: () => import('@/views/landingPage.vue')
  },
  {
    path: '/Profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue')
  },
  {
    path: '/ManageUsers',
    name: 'ManageUsers',
    component: () => import('@/views/ManageUsers.vue')
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
