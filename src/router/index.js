import { createRouter, createWebHistory } from "vue-router";
import CryptoJS from "crypto-js";


const routes = [
  {
    path: "/",
    name: "Login",
    component: () => import("@/views/login.vue"),
  },

  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("@/views/Dashboard.vue"),
  },

  {
    path: "/create-task",
    name: "CreateTask",
    component: () => import("@/views/CreateTask.vue"),
  },

  {
    path: "/evaluate-task",
    name: "EvaluateTask",
    component: () => import("@/views/EvaluateTask.vue"),
  },

  {
    path: "/view-evaluations",
    name: "ViewEvaluations",
    component: () => import("@/views/ViewEvaluations.vue"),
  },

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Add navigation guard to handle component loading errors
router.onError((error) => {
  if (error.message.includes("Failed to fetch dynamically imported module")) {
    window.location.reload();
  }
});

// Setting up the router guard to check for authentication
const encryption_key = process.env.VUE_APP_ENCRYPTION_KEY;

export function set_token(token) {
  var encrypted_token = CryptoJS.AES.encrypt(
    token,
    encryption_key
  ).toString();
  localStorage.setItem("encrypted_token", encrypted_token);
}

export function get_token() {
  var encrypted_token = localStorage.getItem("encrypted_token");

  if (encrypted_token) {
    var decrypted_bytes = CryptoJS.AES.decrypt(encrypted_token, encryption_key);
    return decrypted_bytes.toString(CryptoJS.enc.Utf8);
  }

  return null;
}

export function clear_token() {
  localStorage.removeItem("encrypted_token");
}

export function set_user_details(user_details) {
  var email = user_details.email;
  var user_id = user_details.user_id;
  var last_name = user_details.last_name;
  var user_role = user_details.role.role;
  var first_name = user_details.first_name;
  var phone_number = user_details.phone_number;
  var first_time_login = user_details.first_time_login;

  localStorage.setItem("email", email);
  localStorage.setItem("user_id", user_id);
  localStorage.setItem("user_role", user_role);
  localStorage.setItem("last_name", last_name);
  localStorage.setItem("first_name", first_name);
  localStorage.setItem("phone_number", phone_number);
  localStorage.setItem("first_time_login", first_time_login);
}

export function get_user_details(user_details) {
  var email = localStorage.getItem("email");
  var user_id = localStorage.getItem("user_id");
  var user_role = localStorage.getItem("user_role");
  var last_name = localStorage.getItem("last_name");
  var first_name = localStorage.getItem("first_name");
  var phone_number = localStorage.getItem("phone_number");

  var user_details = {
    user_role: user_role,
    first_name: first_name,
    last_name: last_name,
    user_id: user_id,
    phone_number: phone_number,
    email: email,
  };

  return user_details;
}

export default router;
