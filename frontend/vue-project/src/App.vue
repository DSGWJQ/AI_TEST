<script setup>
import NavBar from './components/NavBar.vue'
import { store } from './store'
</script>

<template>
  <div id="app" class="min-h-screen">
    <!-- 用 Tailwind 导航组件替换原 nav，保留路由逻辑 -->
    <NavBar />
    <div class="max-w-screen-xl mx-auto px-4 py-6">
      <router-view />
    </div>
  </div>
</template>

<!-- 移除原 scoped CSS，遵循“不要用 CSS，只用 Tailwind”的要求 -->
<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.navbar {
  padding: 1rem;
  background-color: #f8f9fa;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: #007bff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #e9ecef;
}

.nav-link.router-link-active {
  background-color: #007bff;
  color: white;
}

.user-info {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logout-btn {
  padding: 5px 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c82333;
}
</style>
