<script setup>
import NavBar from './components/NavBar.vue'
import { store } from './store'
</script>

<template>
  <div id="app" class="min-h-screen">
    <NavBar />
    <div class="max-w-screen-xl mx-auto px-4 py-6">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
/* 移除旧样式，使用统一的暗色主题 */
#app {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
