
<template>
  <div>
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-container">
        <div class="spinner">
          <div class="spinner1"></div>
        </div>
        <div class="loading-text">
          <span class="typing-text">{{ displayedText }}</span>
          <span class="cursor">|</span>
        </div>
      </div>
    </div>

    <router-view />
    <NotificationToast />
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import NotificationToast from './components/NotificationToast.vue';

export default {
  name: 'App',
  components: {
    NotificationToast
  },
  setup() {
    const isLoading = ref(false);
    const displayedText = ref('');
    const typingInterval = ref(null);
    const typingIndex = ref(0);
    const currentPath = ref('');
    const router = useRouter();

    const startTypingAnimation = () => {
      const fullText = `Loading ${currentPath.value}`;
      typingIndex.value = 0;
      displayedText.value = '';
      
      if (typingInterval.value) {
        clearInterval(typingInterval.value);
      }
      
      typingInterval.value = setInterval(() => {
        if (typingIndex.value < fullText.length) {
          displayedText.value += fullText.charAt(typingIndex.value);
          typingIndex.value++;
        } else {
          // Add ellipsis effect
          if (displayedText.value.endsWith('...')) {
            displayedText.value = displayedText.value.slice(0, -3);
          } else {
            displayedText.value += '.';
          }
        }
      }, 100);
    };

    const stopTypingAnimation = () => {
      if (typingInterval.value) {
        clearInterval(typingInterval.value);
        typingInterval.value = null;
      }
    };

    router.beforeEach((to, from, next) => {
      isLoading.value = true;
      // Extract and format the path for display
      currentPath.value = to.path === '/' ? 'home' : to.path.replace(/^\//, '').replace(/\//g, ' > ');
      startTypingAnimation();
      next();
    });

    router.afterEach(() => {
      // Add a small delay to ensure the component has time to render
      setTimeout(() => {
        isLoading.value = false;
        stopTypingAnimation();
      }, 500);
    });

    watch(isLoading, (newValue) => {
      if (newValue === true) {
        startTypingAnimation();
      } else {
        stopTypingAnimation();
      }
    });

    return { 
      isLoading,
      displayedText
    };
  }
}
</script>

<style>
/* Reset default margins and padding */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
}

#app {
  font-family: "Poppins", sans-serif;
  font-weight: 400;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 0;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgb(0, 0, 0);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.spinner {
  background-image: linear-gradient(rgb(255, 66, 66) 35%, rgb(255, 0, 4));
  width: 100px;
  height: 100px;
  animation: spinning82341 1.7s linear infinite;
  text-align: center;
  border-radius: 50px;
  filter: blur(1px);
  box-shadow: 0px -5px 20px 0px rgb(255, 66, 66), 0px 5px 20px 0px rgb(255, 0, 0);
}

.spinner1 {
  background-color: rgb(36, 36, 36);
  width: 100px;
  height: 100px;
  border-radius: 50px;
  filter: blur(10px);
}

.loading-text {
  color: white;
  font-size: 14px;
  letter-spacing: 2px;
  font-family: monospace;
  font-weight: bold;
  min-height: 30px;
  position: relative;
}

.typing-text {
  color: rgb(255, 66, 66);
}

.cursor {
  display: inline-block;
  position: relative;
  color: white;
  animation: blink 1s step-end infinite;
}

@keyframes spinning82341 {
  to {
    transform: rotate(360deg);
  }
}

@keyframes blink {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}
</style>