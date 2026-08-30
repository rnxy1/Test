import path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import frappeui from 'frappe-ui/vite'

const isAIStudioPreview = process.env.VITE_AI_STUDIO_PREVIEW === '1'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    frappeui({
      frappeProxy: !isAIStudioPreview,
      lucideIcons: true,
      jinjaBootData: !isAIStudioPreview,
      buildConfig: {
        indexHtmlPath: '../marley_frontend/www/healthcare.html',
        emptyOutDir: true,
        sourcemap: true,
      },
    }),
    vue()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      interactjs: 'interactjs/dist/interact.min.js',
    },
  },
  build: {
    outDir: '../marley_frontend/public/frontend',
    emptyOutDir: true,
    target: 'es2015'
  },
  frappe: {
    buildOutputDir: '../marley_frontend/public/frontend'
  },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', "tailwind.config.js", 'engine.io-client', 'highlight.js', 'lowlight', 'interactjs'],
  },
  server: {
    sourcemapIgnoreList: () => false,
  },
  define: {
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
  },
})
