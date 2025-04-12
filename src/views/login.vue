<template>
  <div class="auth-container">
    <!-- Image Carousel Section -->
    <div class="carousel-section" v-show="!isMobile">
      <div class="logo">
        <img src="@/assets/Kompyler.png" alt="Logo" />
      </div>
      <div class="back-link" @click="goBack">
        <span>Back to website</span>
        <i class="fas fa-arrow-right"></i>
      </div>
      <div class="carousel">
        <transition-group name="fade" tag="div" class="slides">
          <div
            v-for="(slide, index) in slides"
            :key="slide.id"
            v-show="currentSlide === index"
            class="slide"
            :style="{ backgroundImage: `url(${slide.image})` }"
          ></div>
        </transition-group>
        <div class="carousel-content">
          <h2>{{ slides[currentSlide].title }}</h2>
          <p>{{ slides[currentSlide].description }}</p>
        </div>
        <div class="carousel-dots">
          <span
            v-for="(slide, index) in slides"
            :key="`dot-${slide.id}`"
            :class="['dot', { active: currentSlide === index }]"
            @click="setSlide(index)"
          ></span>
        </div>
      </div>
    </div>

    <!-- Form Section -->
    <div class="form-section">
      <div class="form-container">
        <h1>{{ isLogin ? "Log in to your account" : "Create an account" }}</h1>
        <p class="toggle-text">
          {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
          <span class="toggle-link" @click="toggleAuthMode">{{
            isLogin ? "Sign up" : "Log in"
          }}</span>
        </p>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <form @submit.prevent="submit_form">
          <div class="name-fields" v-if="!isLogin">
            <div class="form-group">
              <input
                type="text"
                id="first_name"
                v-model="user_sign_up.first_name"
                placeholder="First name"
                required
              />
            </div>
            <div class="form-group">
              <input
                type="text"
                id="last_name"
                v-model="user_sign_up.last_name"
                placeholder="Last name"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <input
              type="email"
              id="email"
              v-model="user_sign_up.email"
              placeholder="Email"
              required
            />
          </div>

          <div class="form-group" v-if="!isLogin">
            <input
              type="text"
              id="first_name"
              v-model="user_sign_up.phone_number"
              placeholder="Phone Number"
              maxlength="10"
              required
            />
          </div>

          <div class="form-group password-field">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="user_sign_up.password"
              placeholder="Enter your password"
              required
            />
            <button
              type="button"
              class="password-toggle"
              @click="showPassword = !showPassword"
            >
              <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
            </button>
          </div>

          <div class="form-group password-field" v-if="!isLogin">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="confirm_password"
              v-model="user_sign_up.confirm_password"
              placeholder="Confirm your password"
              required
            />
            <button
              type="button"
              class="password-toggle"
              @click="showPassword = !showPassword"
            >
              <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
            </button>
          </div>

          <div class="form-group checkbox-group" v-if="!isLogin">
            <label class="checkbox-container">
              <input
                type="checkbox"
                v-model="user_sign_up.agree_to_terms"
                required
              />
              <span class="checkmark"></span>
              <span class="checkbox-text">
                I agree to the
                <a href="#" class="terms-link">Terms & Conditions</a>
              </span>
            </label>
          </div>

          <button type="submit" class="submit-button" :disabled="!isFormValid">
            {{ isLogin ? "Log in" : "Create account" }}
          </button>
        </form>

        <div class="social-auth">
          <p class="divider">Or register with</p>
          <div class="social-buttons">
            <button class="social-button google">
              <i class="fab fa-google"></i>
              <span>Google</span>
            </button>
            <button class="social-button apple">
              <i class="fab fa-apple"></i>
              <span>Apple</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { set_token, set_user_details } from "@/router";
import Swal from "sweetalert2";

const GLOBAL_URL = process.env.VUE_APP_GLOBAL_URL;

export default {
  name: "AuthComponent",
  data() {
    return {
      isLogin: false,
      showPassword: false,
      isMobile: false,

      user_sign_up: {
        email: "",
        password: "",
        last_name: "",
        first_name: "",
        phone_number: "",
        confirm_password: "",
        agree_to_terms: false,
      },

      currentSlide: 0,
      slides: [
        {
          id: 1,
          image: require("@/assets/login_1.png"),
          title: "Spend Less Time on Admin.",
          description: "More Time Getting Things Done.",
        },
        {
          id: 2,
          image: require("@/assets/login_2.png"),
          title: "Tired of messy task reviews?",
          description: "Kompyler cleaned it up.",
        },
        {
          id: 3,
          image: require("@/assets/login_3.png"),
          title: "Real task evaluations.",
          description: "Real stakeholder insights.",
        },
      ],
      slideInterval: null,
      users: [],
      currentUser: null,
      successMessage: "",
      errorMessage: "",
    };
  },

  mounted() {
    this.isLogin = true;
    this.checkScreenSize();
    window.addEventListener("resize", this.checkScreenSize);
    this.startCarousel();
    this.loadUsers();
    this.checkAuth();
  },

  methods: {
    async sign_up() {
      if (this.user_sign_up.password.length < 8) {
        Swal.fire({
          icon: "info",
          title: "Invalid Password",
          text: "Password must be at least 8 characters long.",
          showConfirmButton: false,
          timer: 2000,
        });
        return;
      }

      if (!/[A-Z]/.test(this.user_sign_up.password)) {
        Swal.fire({
          icon: "info",
          title: "Invalid Password",
          text: "Password must contain at least one uppercase letter.",
          showConfirmButton: false,
          timer: 2000,
        });
        return;
      }

      if (!/[a-z]/.test(this.user_sign_up.password)) {
        Swal.fire({
          icon: "info",
          title: "Invalid Password",
          text: "Password must contain at least one lowercase letter.",
          showConfirmButton: false,
          timer: 2000,
        });
        return;
      }

      if (!/\d/.test(this.user_sign_up.password)) {
        Swal.fire({
          icon: "info",
          title: "Invalid Password",
          text: "Password must contain at least one number.",
          showConfirmButton: false,
          timer: 2000,
        });
        return;
      }

      if (!/[@$!%*?&]/.test(this.user_sign_up.password)) {
        Swal.fire({
          icon: "info",
          title: "Invalid Password",
          text: "Password must contain at least one special character (e.g., @$!%*?&).",
          showConfirmButton: true,
        });
        return;
      }

      if (this.user_sign_up.password !== this.user_sign_up.confirm_password) {
        Swal.fire({
          icon: "info",
          title: "Password Mismatch",
          text: "Password and Confirm Password do not match.",
          showConfirmButton: true,
        });
        return;
      }

      var sign_up_url = `${GLOBAL_URL}/system_management/sign_up/`;
      var header = {
        "Content-Type": "application/json",
      };

      try {
        var response = await axios.post(sign_up_url, this.user_sign_up, {
          headers: header,
        });

        var response_data = JSON.parse(response.data);
        if (response_data.status === "success") {
          Swal.fire({
            icon: "success",
            title: "Success",
            text: response_data.message,
            showConfirmButton: false,
            timer: 2000,
          }).then(() => {
            this.user_sign_up = {
              email: "",
              password: "",
              last_name: "",
              first_name: "",
              confirm_password: "",
              agree_to_terms: false,
            };
            this.toggleAuthMode();
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Error",
            text: response_data.message,
            showConfirmButton: false,
            timer: 2000,
          });
        }
      } catch (error) {
        if (error.response && error.response.data) {
          var error_message = JSON.parse(error.response.data).message;
          Swal.fire({
            icon: "info",
            title: "Validation Error",
            text: error_message,
            showConfirmButton: false,
            timer: 2000,
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Error",
            text: "An error occurred during sign up.",
            showConfirmButton: false,
            timer: 2000,
          });
        }
      }
    },

    async user_login() {
      var login_url = `${GLOBAL_URL}/system_management/user_login/`;
      var header = {
        "Content-Type": "application/json",
      };

      var data = {
        email: this.user_sign_up.email,
        password: this.user_sign_up.password,
      };

      try {
        var response = await axios.post(login_url, data, { headers: header });

        var response_data = JSON.parse(response.data);
        if (response_data.status === 'success') {
          Swal.fire({
            icon: "success",
            title: "Login Successful",
            text: response_data.message,
            showConfirmButton: false,
            timer: 2000,
          }).then(() => {
            set_token(response_data.token);
            set_user_details(response_data.data.user_details);
            window.location.href = "dashboard/";
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Login Failed",
            text: "Invalid credentials.",
            showConfirmButton: false,
            timer: 2000,
          });
        }
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "An error occurred during login.",
          showConfirmButton: false,
          timer: 2000,
        });
      }
    },

    loadUsers() {
      const storedUsers = localStorage.getItem("kompyler_users");
      this.users = storedUsers ? JSON.parse(storedUsers) : [];
    },

    saveUsers() {
      localStorage.setItem("kompyler_users", JSON.stringify(this.users));
    },

    toggleAuthMode() {
      this.isLogin = !this.isLogin;
      this.resetMessages();
      this.user_sign_up = {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        agree_to_terms: false,
      };
    },

    resetMessages() {
      this.successMessage = "";
      this.errorMessage = "";
    },

    checkScreenSize() {
      this.isMobile = window.innerWidth < 768;
    },

    submit_form() {
      if (!this.isFormValid) return;
      this.resetMessages();

      if (this.isLogin) {
        this.user_login();
      } else {
        this.sign_up();
      }
    },

    checkAuth() {
      const user = localStorage.getItem("kompyler_currentUser");
      if (user) {
        this.currentUser = JSON.parse(user);
      }
    },

    goBack() {
      this.$router.push("/");
    },

    setSlide(index) {
      this.currentSlide = index;
      this.resetCarouselTimer();
    },

    nextSlide() {
      this.currentSlide = (this.currentSlide + 1) % this.slides.length;
    },

    startCarousel() {
      this.slideInterval = setInterval(this.nextSlide, 5000);
    },

    stopCarousel() {
      clearInterval(this.slideInterval);
    },

    resetCarouselTimer() {
      this.stopCarousel();
      this.startCarousel();
    },
  },

  computed: {
    isFormValid() {
      if (this.isLogin) {
        return this.user_sign_up.email && this.user_sign_up.password;
      } else {
        return (
          this.user_sign_up.first_name &&
          this.user_sign_up.last_name &&
          this.user_sign_up.email &&
          this.user_sign_up.password &&
          this.user_sign_up.agree_to_terms
        );
      }
    },
  },

  beforeDestroy() {
    window.removeEventListener("resize", this.checkScreenSize);
    this.stopCarousel();
  },
};
</script>

<style scoped>
.success-message {
  padding: 10px;
  margin-bottom: 20px;
  background-color: #4caf50;
  color: white;
  border-radius: 4px;
  text-align: center;
}

.error-message {
  padding: 10px;
  margin-bottom: 20px;
  background-color: #f44336;
  color: white;
  border-radius: 4px;
  text-align: center;
}

/* Rest of your existing styles... */
.logo {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
}

.logo img {
  height: 140px;
  width: auto;
  max-width: auto;
}

.auth-container {
  display: flex;
  min-height: 100vh;
  background-color: #1a1a1a;
  color: #ffffff;
  font-family: "Arial", sans-serif;
}

.logo {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
}

.logo img {
  height: 140px; /* Adjust this value to make bigger/smaller */
  width: auto; /* Maintains aspect ratio */
  max-width: auto; /* Prevents it from getting too wide */
}

.auth-container {
  display: flex;
  min-height: 100vh;
  background-color: #1a1a1a;
  color: #ffffff;
  font-family: "Arial", sans-serif;
}

/* Carousel Section */
.carousel-section {
  position: relative;
  flex: 1;
  background-color: #000000;
  overflow: hidden;
  border-radius: 10px;
}

.logo {
  position: absolute;
  top: 20px;
  left: 30px;
  z-index: 10;
  font-size: 24px;
  font-weight: bold;
  color: white;
}

.back-link {
  position: absolute;
  top: 20px;
  right: 30px;
  z-index: 10;
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.back-link:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.back-link span {
  margin-right: 8px;
  font-size: 14px;
}

.carousel {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.slides {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
}

.carousel-content {
  position: relative;
  padding: 40px;
  z-index: 5;
  margin-bottom: 60px;
}

.carousel-content h2 {
  font-size: 32px;
  margin-bottom: 10px;
}

.carousel-content p {
  font-size: 20px;
  opacity: 0.8;
}

.carousel-dots {
  display: flex;
  justify-content: center;
  padding: 20px;
  position: relative;
  z-index: 5;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  margin: 0 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.dot.active {
  background-color: #ffffff;
  width: 24px;
  border-radius: 5px;
}

/* Form Section */
.form-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 30px;
  background-color: #1a1a1a;
}

.form-container {
  width: 100%;
  max-width: 400px;
}

h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #ffffff;
}

.toggle-text {
  font-size: 14px;
  margin-bottom: 30px;
  color: #cccccc;
}

.toggle-link {
  color: #ff3333;
  cursor: pointer;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s;
}

.toggle-link:hover {
  color: #ff6666;
  text-decoration: underline;
}

.name-fields {
  display: flex;
  gap: 10px;
}

.form-group {
  margin-bottom: 20px;
  width: 100%;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 12px 15px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #333333;
  background-color: #2a2a2a;
  color: #ffffff;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input::placeholder {
  color: #888888;
}

input:focus {
  outline: none;
  border-color: #ff3333;
  box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.2);
}

.password-field {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #888888;
  cursor: pointer;
  padding: 0;
}

.checkbox-group {
  margin-top: 20px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  position: relative;
  cursor: pointer;
  font-size: 14px;
  user-select: none;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  height: 20px;
  width: 20px;
  background-color: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 4px;
  margin-right: 10px;
  position: relative;
}

.checkbox-container:hover input ~ .checkmark {
  background-color: #3a3a3a;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #ff3333;
  border-color: #ff3333;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
  left: 7px;
  top: 3px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-text {
  color: #cccccc;
}

.terms-link {
  color: #ff3333;
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}

.submit-button {
  width: 100%;
  padding: 14px;
  background-color: #ff3333;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #ff4444;
}

.submit-button:disabled {
  background-color: #882222;
  cursor: not-allowed;
}

.social-auth {
  margin-top: 30px;
}

.divider {
  display: flex;
  align-items: center;
  color: #888888;
  font-size: 14px;
  margin: 20px 0;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background-color: #333333;
}

.divider::before {
  margin-right: 10px;
}

.divider::after {
  margin-left: 10px;
}

.social-buttons {
  display: flex;
  gap: 10px;
}

.social-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background-color: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 8px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.social-button i {
  margin-right: 8px;
  font-size: 16px;
}

.social-button:hover {
  background-color: #3a3a3a;
}

/* Animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* Mobile Responsive Styles */
@media (max-width: 767px) {
  .auth-container {
    flex-direction: column;
  }

  .form-section {
    padding: 20px;
  }

  .form-container {
    max-width: 100%;
  }

  .name-fields {
    flex-direction: column;
    gap: 0;
  }

  h1 {
    font-size: 24px;
    text-align: center;
  }

  .toggle-text {
    text-align: center;
  }

  /* Add a simple mobile carousel at the top */
  .carousel-mobile {
    height: 200px;
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
  }
}
</style>
