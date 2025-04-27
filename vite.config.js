import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueScss from 'vite-plugin-vue-scss';

export default defineConfig({
  base: '/Kompyler/',
  plugins: [
    vue(),
    vueScss()
  ],
  define: {
    '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': false
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @import "./src/styles/variables.scss";
        `
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
});
