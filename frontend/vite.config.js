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
    host: '0.0.0.0',
    port: 5173,
    strictPort: false, // 允许自动选择端口，避免冲突
    proxy: {
      '/api': {
        // 环境变量优先，容器内用 host.docker.internal，本机用 localhost
        target: process.env.DOCKER_ENV ? 'http://host.docker.internal:8000' : 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
