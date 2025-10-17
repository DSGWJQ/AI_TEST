import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import VueDevTools from 'vite-plugin-vue-devtools' // 临时注释

export default defineConfig({
  plugins: [
    vue(),
    // VueDevTools(), // 临时注释
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: '127.0.0.1',
    port: 5177,
    strictPort: true,
    proxy: {
      // 将以 /api 开头的请求，转发到后端 FastAPI
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
