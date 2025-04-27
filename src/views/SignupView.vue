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
          <p class="otp-instructions">We've sent a 6-digit code to example@email.com</p>
          
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
            <span class="toggle-link" @click="$router.push('/login')">Log in</span>
          </p>

          <form @submit.prevent>
            <div class="name-fields">
              <div class="form-group">
                <input type="text" id="firstName" placeholder="First name" required />
              </div>
              <div class="form-group">
                <input type="text" id="lastName" placeholder="Last name" required />
              </div>
            </div>

            <div class="form-group">
              <input type="email" id="email" placeholder="Email" required />
            </div>

            <div class="form-group password-field">
              <input type="password" id="password" placeholder="Enter your password" required minlength="6" />
              <button type="button" class="password-toggle">
                <i class="fas fa-eye"></i>
              </button>
            </div>

            <div class="form-group checkbox-group">
              <label class="checkbox-container">
                <input type="checkbox" required />
                <span class="checkmark"></span>
                <span class="checkbox-text">
                  I agree to the <a href="#" class="terms-link">Terms & Conditions</a>
                </span>
              </label>
            </div>

            <button type="submit" class="submit-button" @click="$router.push('/verify-otp')">Create account</button>
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
  </div>
</template>

<script>
export default {
  name: 'SignupView',
  data() {
    return {
      isMobile: false,
      showOTPSection: false,
      currentSlide: 0,
      slides: [
        {
          id: 1,
          image: require('@/assets/login_1.png'),
          title: 'Spend Less Time on Admin.',
          description: 'More Time Getting Things Done.'
        },
        {
          id: 2,
          image: require('@/assets/login_2.png'),
          title: 'Tired of messy task reviews?',
          description: 'Kompyler cleaned it up.'
        },
        {
          id: 3,
          image: require('@/assets/login_3.png'),
          title: 'Real task evaluations.',
          description: 'Real stakeholder insights.'
        }
      ],
      slideInterval: null
    }
  },
  mounted() {
    this.checkScreenSize();
    window.addEventListener('resize', this.checkScreenSize);
    this.startCarousel();
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkScreenSize);
    this.stopCarousel();
  },
  methods: {
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
    }
  }
}
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
  background-color: #4CAF50;
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

/* Animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
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
</style>
