<template>
  <div class="auth-container">
    <!-- Image Carousel Section -->
    <div class="carousel-section" v-show="!isMobile">
      <div class="logo">
        <img src="@/assets/Kompyler.png" alt="Logo" />
      </div>
      <div class="back-link" @click="$router.push('/landing-page')">
        <span>Visit website</span>
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
        <!-- OTP Verification Section -->
        <div class="otp-section" v-if="showOTPSection">
          <h1>Verify Your Email</h1>
          <p class="otp-instructions">
            We've sent a 6-digit code to example@email.com
          </p>

          <div class="otp-input-container">
            <input
              v-for="index in 6"
              :key="index"
              type="text"
              maxlength="1"
              class="otp-input"
            />
          </div>

          <button class="submit-button">Verify</button>

          <p class="resend-otp">
            Didn't receive a code?
            <span class="resend-link">Resend</span>
          </p>
        </div>

        <!-- Signup Form -->
        <div v-else>
          <h1>Create an account</h1>
          <p class="toggle-text">
            Already have an account?
            <span class="toggle-link" @click="$router.push('/login')"
              >Log in</span
            >
          </p>

          <form @submit.prevent>
            <div class="name-fields">
              <div class="form-group">
                <input
                  type="text"
                  id="firstName"
                  placeholder="First name"
                  v-model="sign_up_data.first_name"
                  @input="validateFirstName"
                />
                <span class="error-text" v-if="firstNameError">{{ firstNameError }}</span>
              </div>
              <div class="form-group">
                <input
                  type="text"
                  id="lastName"
                  placeholder="Last name"
                  v-model="sign_up_data.last_name"
                  @input="validateLastName"
                />
                <span class="error-text" v-if="lastNameError">{{ lastNameError }}</span>
              </div>
            </div>
            <div class="form-group">
              <input 
                type="tel" 
                id="phone_number" 
                placeholder="Phone number" 
                v-model="sign_up_data.phone_number"
                pattern="^0[0-9]{9}$"
                maxlength="10"
                @input="validatePhoneNumber"
              />
              <span class="error-text" v-if="phoneError">{{ phoneError }}</span>
            </div>
            <div class="form-group">
              <input 
                type="email"
                id="email"
                v-model="sign_up_data.email"
                placeholder="Email"
                @input="validateEmail"
              />
              <span class="error-text" v-if="emailError">{{ emailError }}</span>
            </div>

            <div class="form-group password-field">
              <input
                type="password"
                id="password"
                placeholder="Enter your password"
                v-model="sign_up_data.password"
                @input="validatePassword"
              />
              <button type="button" class="password-toggle" @click="togglePassword('password')">
                <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
              </button>
              <span class="error-text" v-if="passwordError">{{ passwordError }}</span>
            </div>

            <div class="form-group password-field">
              <input
                type="password"
                id="confirm_password"
                placeholder="Confirm your password"
                v-model="sign_up_data.confirm_password"
                @input="validateConfirmPassword"
              />
              <button type="button" class="password-toggle" @click="togglePassword('confirm_password')">
                <i :class="['fas', showConfirmPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
              </button>
              <span class="error-text" v-if="confirmPasswordError">{{ confirmPasswordError }}</span>
            </div>

            <div class="form-group checkbox-group">
              <label class="checkbox-container">
                <input type="checkbox" v-model="termsAccepted" @change="validateTerms"/>
                <span class="checkmark"></span>
                <span class="checkbox-text">
                  I agree to the
                  <a href="#" class="terms-link" @click.prevent="showTermsModal = true">Terms & Conditions</a>
                </span>
              </label>
              <span class="error-text" v-if="termsError">{{ termsError }}</span>
            </div>

            <button
              type="submit"
              class="submit-button"
              :disabled="!isValid || !termsAccepted"
              @click="sign_up">
              Create account
            </button>

            <!-- Add error message display -->
            <div v-if="show_error_message" class="error-message">
              {{ error_message }}
            </div>
          </form>

          <!-- Terms and Conditions Modal -->
          <div class="modal" v-if="showTermsModal">
            <div class="modal-content">
              <div class="modal-header">
                <h2>Terms and Conditions</h2>
                <button class="close-btn" @click="showTermsModal = false">&times;</button>
              </div>
              <div class="modal-body">
                <p>1. By using our service, you agree to these terms and conditions.</p>
                <p>2. We respect your privacy and protect your personal information.</p>
                <p>3. You must provide accurate and complete information when creating an account.</p>
                <p>4. You are responsible for maintaining the security of your account.</p>
                <!-- Add more terms as needed -->
              </div>
              <div class="modal-footer">
                <button class="modal-btn" @click="acceptTerms">Accept</button>
                <button class="modal-btn cancel" @click="showTermsModal = false">Close</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
import axios from "axios";

const GLOBAL_URL = process.env.VUE_APP_GLOBAL_URL;

export default {
  name: "SignupView",
  data() {
    return {
      isMobile: false,
      showOTPSection: false,
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

      // Integration Variables
      sign_up_data: {
        email: "",
        password: "",
        last_name: "",
        first_name: "",
        phone_number: "",
      },
      phoneError: '',
      passwordError: '',
      confirmPasswordError: '',
      termsAccepted: false,
      termsError: '',
      showPassword: false,
      showConfirmPassword: false,
      showTermsModal: false,
      isValid: false,

      // New validation error messages
      firstNameError: '',
      lastNameError: '',
      emailError: '',
      error_message: '',
      show_error_message: false,
    }
  },
  mounted() {
    this.checkScreenSize();
    window.addEventListener("resize", this.checkScreenSize);
    this.startCarousel();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.checkScreenSize);
    this.stopCarousel();
  },
  methods: {
    // Integration Functions

    validateFirstName() {
      if (!this.sign_up_data.first_name) {
        this.firstNameError = 'First name is required';
      } else if (this.sign_up_data.first_name.length < 2) {
        this.firstNameError = 'First name must be at least 2 characters';
      } else {
        this.firstNameError = '';
      }
      this.checkFormValidity();
    },

    validateLastName() {
      if (!this.sign_up_data.last_name) {
        this.lastNameError = 'Last name is required';
      } else if (this.sign_up_data.last_name.length < 2) {
        this.lastNameError = 'Last name must be at least 2 characters';
      } else {
        this.lastNameError = '';
      }
      this.checkFormValidity();
    },

    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.sign_up_data.email) {
        this.emailError = 'Email is required';
      } else if (!emailRegex.test(this.sign_up_data.email)) {
        this.emailError = 'Please enter a valid email address';
      } else {
        this.emailError = '';
      }
      this.checkFormValidity();
    },

    validatePhoneNumber() {
      const phoneRegex = /^0[0-9]{9}$/;
      if (!this.sign_up_data.phone_number) {
        this.phoneError = 'Phone number is required';
      } else if (!phoneRegex.test(this.sign_up_data.phone_number)) {
        this.phoneError = 'Phone number must start with 0 and have 10 digits';
      } else {
        this.phoneError = '';
      }
      this.checkFormValidity();
    },

    validatePassword() {
      const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
      if (!this.sign_up_data.password) {
        this.passwordError = 'Password is required';
      } else if (!passwordRegex.test(this.sign_up_data.password)) {
        this.passwordError = 'Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character';
      } else {
        this.passwordError = '';
      }
      this.validateConfirmPassword();
      this.checkFormValidity();
    },

    validateConfirmPassword() {
      if (!this.sign_up_data.confirm_password) {
        this.confirmPasswordError = 'Please confirm your password';
      } else if (this.sign_up_data.password !== this.sign_up_data.confirm_password) {
        this.confirmPasswordError = 'Passwords do not match';
      } else {
        this.confirmPasswordError = '';
      }
      this.checkFormValidity();
    },

    validateTerms() {
      if (!this.termsAccepted) {
        this.termsError = 'You must accept the terms and conditions';
      } else {
        this.termsError = '';
      }
      this.checkFormValidity();
    },

    acceptTerms() {
      this.termsAccepted = true;
      this.termsError = '';
      this.showTermsModal = false;
      this.checkFormValidity();
    },

    checkFormValidity() {
      this.isValid = !this.firstNameError && !this.lastNameError && 
                    !this.emailError && !this.phoneError && 
                    !this.passwordError && !this.confirmPasswordError && 
                    this.termsAccepted;
    },

    togglePassword(field) {
      if (field === 'password') {
        this.showPassword = !this.showPassword;
        const input = document.getElementById('password');
        input.type = this.showPassword ? 'text' : 'password';
      } else {
        this.showConfirmPassword = !this.showConfirmPassword;
        const input = document.getElementById('confirm_password');
        input.type = this.showConfirmPassword ? 'text' : 'password';
      }
    },

    async sign_up() {
      // Validate all fields
      this.validateFirstName();
      this.validateLastName();
      this.validateEmail();
      this.validatePhoneNumber();
      this.validatePassword();
      this.validateConfirmPassword();
      this.validateTerms();

      if (!this.isValid) {
        this.error_message = "Please fix all errors before submitting";
        this.show_error_message = true;
        return;
      }

      var sign_up_url = `${GLOBAL_URL}/system_management/sign_up/`;
      var headers = {
        "Content-Type": "application/json",
      };

      try {
        var response = await axios.post(sign_up_url, this.sign_up_data, {
          headers: headers,
        });
        var response_data = JSON.parse(response.data);

        if (response_data.status === "success") {
          this.$router.push("/");
          this.success_message = response_data.message;
        } else {
          this.error_message = response_data.message;
          this.show_error_message = true;
        }
      } catch (error) {
        if (error.response) {
          try {
            const errorData = JSON.parse(error.response.data);
            this.error_message = errorData.message || 'An error occurred during sign up';
          } catch (e) {
            this.error_message = error.response.data || error.message;
          }
        } else if (error.request) {
          // The request was made but no response was received
          this.error_message = 'No response received from server';
        } else {
          // Something happened in setting up the request
          this.error_message = error.message;
        }
        this.show_error_message = true;
      }
    },

    // End Integration Functions
    checkScreenSize() {
      this.isMobile = window.innerWidth < 768;
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
};
</script>

<style scoped>
.auth-container {
  display: flex;
  min-height: 100vh;
  background-color: #1a1a1a;
  color: #ffffff;
}

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

/* Carousel Section */
.carousel-section {
  position: relative;
  flex: 1;
  background-color: #000000;
  overflow: hidden;
  border-radius: 10px;
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

input[type="tel"],
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

/* Message Styles */
.success-message {
  padding: 10px;
  margin-bottom: 20px;
  background-color: #4caf50;
  color: white;
  border-radius: 4px;
  text-align: center;
}

.error-message {
  margin: 10px 0;
  padding: 10px;
  background-color: rgba(255, 51, 51, 0.1);
  border: 1px solid #ff3333;
  border-radius: 4px;
  color: #ff3333;
  font-size: 14px;
  text-align: center;
}

/* OTP Section Styles */
.otp-section {
  text-align: center;
}

.otp-instructions {
  color: #cccccc;
  margin-bottom: 30px;
}

.otp-input-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
}

.otp-input {
  width: 40px;
  height: 50px;
  text-align: center;
  font-size: 20px;
  border-radius: 8px;
  border: 1px solid #333333;
  background-color: #2a2a2a;
  color: #ffffff;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.otp-input:focus {
  outline: none;
  border-color: #ff3333;
  box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.2);
}

.resend-otp {
  color: #888888;
  margin-top: 20px;
}

.resend-link {
  color: #ff3333;
  cursor: pointer;
  text-decoration: none;
}

.resend-link:hover {
  text-decoration: underline;
}

.change-email {
  color: #888888;
  margin-top: 10px;
  cursor: pointer;
  text-decoration: underline;
}

.change-email:hover {
  color: #cccccc;
}

.error-text {
  color: #ff3333;
  font-size: 12px;
  margin-top: 5px;
  display: block;
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

  /* Adjust OTP inputs for mobile */
  .otp-input {
    width: 35px;
    height: 45px;
    font-size: 18px;
  }
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #2a2a2a;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #333333;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
}

.close-btn {
  background: none;
  border: none;
  color: #888888;
  font-size: 24px;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
  color: #cccccc;
  line-height: 1.6;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #333333;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.modal-btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.modal-btn:not(.cancel) {
  background-color: #ff3333;
  color: white;
}

.modal-btn.cancel {
  background-color: #333333;
  color: white;
}
</style>
