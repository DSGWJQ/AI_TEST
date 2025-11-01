<template>
    <div class="w-[350px] mx-auto h-[357px] p-5 space-y-4">
        <h1 class="text-2xl font-bold">欢迎登录test系统</h1>
        <form class="space-y-2">
            <div>username:<input type="text" v-model="loginform.username" class="ml-2 border border-gray-300 rounded px-2 py-1"/></div>
            <div>password:<input type="password" v-model="loginform.password" class="ml-2 border border-gray-300 rounded px-2 py-1"/></div>
        </form>
        <button @click="handleLogin" :disabled="loading" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
          {{ loading ? '登录中...' : '登录' }}
        </button>
        
        <!-- 显示登录状态 -->
        <div v-if="store.isLoggedIn && store.user.username" class="mt-5 p-3 bg-gray-100 rounded">
            <p class="text-gray-700">已登录用户：{{ store.user.username || '用户' }}</p>
            <button @click="handleLogout" class="mt-2 px-3 py-2 bg-red-600 text-white rounded hover:bg-red-700">登出</button>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../store'
import { authAPI } from '../api'

const router = useRouter()
const loading = ref(false)
const loginform = reactive({
    username: '',
    password: ''
})

// 登录处理（使用 axios）
const handleLogin = async () => {
    if (!loginform.username || !loginform.password) {
        alert('请输入用户名和密码')
        return
    }
    
    loading.value = true
    
    try {
        const response = await authAPI.login(loginform.username, loginform.password)
        const data = response.data
        
        // 登录成功，更新store状态（包含token）
        store.login(data.username, data.user_id, data.access_token)
        alert('登录成功')
        router.push('/')
    } catch (error) {
        console.error('登录错误:', error)
        const errorMsg = error.response?.data?.detail || '登录失败'
        alert(errorMsg)
    } finally {
        loading.value = false
    }
}

// 登出处理
const handleLogout = () => {
    store.logout()
    alert('已登出')
}
</script>

