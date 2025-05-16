import { createRouter, createWebHistory } from 'vue-router';
import CryptoJS from "crypto-js";

// System imports
import LoginView from '@/views/LoginView.vue';
import SignupView from '@/views/SignupView.vue';
import OTPVerificationView from '@/views/OTPVerificationView.vue';
import TeamSelection from '@/views/TeamSelection.vue';


const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('@/views/LoginView.vue')
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
  },
  {
    path: '/SignupView',
    name: 'SignupView',
    component: SignupView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView
  },
  {
    path: '/verify-otp',
    name: 'verify-otp',
    component: OTPVerificationView
  },
  { 
    path: '/team-selection',
    name: 'team-selection',
    component: TeamSelection
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

const encryption_key = process.env.VUE_APP_ENCRYPTION_KEY;

export function set_token(token) {
  var encrypted_token = CryptoJS.AES.encrypt(token, encryption_key).toString();
  localStorage.setItem("encrypted_token", encrypted_token);
}

export function get_token() {
  var encrypted_token = localStorage.getItem("encrypted_token");

  if (encrypted_token) {
    var descrypted_token = CryptoJS.AES.decrypt(
      encrypted_token,
      encryption_key
    );

    return descrypted_token.toString(CryptoJS.enc.Utf8);
  }

  return null;
}

router.beforeEach((to, from, next) => {
  var token = localStorage.getItem("encrypted_token");

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (token) {
      next();
    } else {
      next("/");
    }
  } else {
    next();
  }
});

export function clear_token() {
  localStorage.removeItem("encrypted_token");
}

export function set_user_details(user_details) {
  var role = user_details.role;
  var user_id = user_details.id;
  var last_name = user_details.last_name;
  var first_name = user_details.first_name;

  localStorage.setItem("role", role);
  localStorage.setItem("user_id", user_id);
  localStorage.setItem("last_name", last_name);
  localStorage.setItem("first_name", first_name);
}

export function get_user_details() {
  var role = localStorage.getItem("role");
  var user_id = localStorage.getItem("user_id");
  var last_name = localStorage.getItem("last_name");
  var first_name = localStorage.getItem("first_name");

  var user_details = {
    role: role,
    user_id: user_id,
    last_name: last_name,
    first_name: first_name,
  };

  return user_details;
}


// Add navigation guard to handle component loading errors
router.onError((error) => {
  if (error.message.includes('Failed to fetch dynamically imported module')) {
    window.location.reload();
  }
});

export default router;
