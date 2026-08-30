import path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import frappeui from 'frappe-ui/vite'

export default defineConfig({
  base: '/',
  plugins: [
    frappeui({
      frappeProxy: false,
      jinjaBootData: false,
      buildConfig: false,
      lucideIcons: true,
    }),
    vue(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      interactjs: 'interactjs/dist/interact.min.js',
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    target: 'es2015',
  },
  optimizeDeps: {
    include: [
      'frappe-ui > feather-icons',
      'tailwind.config.js',
      'engine.io-client',
      'highlight.js',
      'lowlight',
      'interactjs',
    ],
  },
  server: {
    host: '0.0.0.0',
    port: 8080,
    sourcemapIgnoreList: () => false,
  },
  define: {
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
  },
})
