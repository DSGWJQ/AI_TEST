<script setup>
import { store } from './store'
</script>

<template>
  <div id="app">
    <nav class="navbar">
      <router-link to="/" class="nav-link">首页</router-link>
      <router-link to="/login" class="nav-link">登录</router-link>
      <router-link to="/register" class="nav-link">注册</router-link>
      <router-link to="/ai" class="nav-link">AI测试工具</router-link>
      <router-link to="/test-report-beautifier" class="nav-link">测试报告美化</router-link>
      <router-link to="/api-auto-test" class="nav-link">接口自动化工厂</router-link>
      <div v-if="store.isLoggedIn && store.user.username" class="user-info">
        欢迎，{{ store.user.username || '用户' }}！
        <button @click="store.logout()" class="logout-btn">登出</button>
      </div>
    </nav>
    <router-view />
  </div>
</template>
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
