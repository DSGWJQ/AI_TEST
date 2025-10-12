<template>
    <div class="max-w-[800px] mx-auto p-5 text-center">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">欢迎来到我的网站</h1>
        <p class="text-gray-600 mb-5">这是一个简单的首页</p>
        <!-- 中间链接已删除 -->
        <!-- 移除首页中部这组链接按钮，只保留左上角导航 -->
        <!-- （原本的 <div class="my-8 flex ..."> ... </div> 已删除） -->
        <div class="my-8 flex justify-center flex-wrap gap-3">
            <router-link to="/login" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">登录</router-link>
            <router-link to="/register" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">注册</router-link>
            <router-link to="/ai" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">AI测试用例</router-link>
            <router-link to="/test-report-beautifier" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">测试报告美化</router-link>
        </div>
        
        <div class="bg-gray-100 p-4 rounded mt-5" v-if="store.isLoggedIn && store.user.username">
            <p class="text-gray-700">你好，{{ store.user.username || '用户' }}！</p>
            <button class="mt-2 px-3 py-2 bg-red-600 text-white rounded hover:bg-red-700" @click="logout">退出登录</button>
        </div>

        <div class="text-left mt-8">
            <h2 class="text-xl font-semibold text-gray-800 border-b-2 border-blue-600 pb-1">功能介绍</h2>
            <ul class="list-disc pl-5">
                <li class="my-2 text-gray-700">用户注册和登录</li>
                <li class="my-2 text-gray-700">个人信息管理</li>
                <li class="my-2 text-gray-700">更多功能开发中...</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { store } from '../store'

const logout = () => {
    store.logout()
    alert('已退出登录')
}
</script>
