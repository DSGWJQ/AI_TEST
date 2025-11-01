<template>
    <div class="w-[350px] mx-auto p-5 space-y-4">
        <h1 class="text-2xl font-bold">用户注册</h1>
        <form class="space-y-2">
            <div>用户名:<input type="text" v-model="registerform.username" class="ml-2 border border-gray-300 rounded px-2 py-1"/></div>
            <div>密码:<input type="password" v-model="registerform.password" class="ml-2 border border-gray-300 rounded px-2 py-1"/></div>
            <div>确认密码:<input type="password" v-model="registerform.confirmPassword" class="ml-2 border border-gray-300 rounded px-2 py-1"/></div>
        </form>
        <button @click="handleRegister" :disabled="loading" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed">
          {{ loading ? '注册中...' : '注册' }}
        </button>
        <p><router-link to="/login" class="text-blue-600 hover:underline">已有账号？去登录</router-link></p>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'

const router = useRouter()
const loading = ref(false)
const registerform = reactive({
    username: '',
    password: '',
    confirmPassword: ''
})

// 注册处理（使用 axios）
const handleRegister = async () => {
    // 表单验证
    if (!registerform.username || !registerform.password) {
        alert('请输入用户名和密码')
        return
    }
    
    if (registerform.password !== registerform.confirmPassword) {
        alert('两次输入的密码不一致')
        return
    }
    
    loading.value = true
    
    try {
        const response = await authAPI.register(registerform.username, registerform.password)
        
        alert('注册成功！请登录')
        router.push('/login')
    } catch (error) {
        console.error('注册错误:', error)
        const errorMsg = error.response?.data?.detail || '注册失败'
        alert(errorMsg)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.register_content {
    width: 350px;
    margin: 0 auto;
    padding: 20px;
}

button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>