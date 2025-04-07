import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  base: '/Kompyler/',  // Set the base path for your project
  plugins: [vue()],
  define: {
    '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': false  // Prevents hydration mismatch warnings
  }
});
