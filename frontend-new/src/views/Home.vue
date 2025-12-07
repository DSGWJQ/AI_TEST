<template>
    <!-- Speedtest 风格的深色主题首页 -->
    <div class="max-w-[800px] mx-auto p-5 text-center">
        <h1 class="text-3xl font-bold text-white mb-3">欢迎来到测试工具平台</h1>
        <p class="text-gray-400 mb-8 text-lg">一站式测试自动化解决方案</p>
        
        <div class="my-8 flex justify-center flex-wrap gap-4">
            <router-link 
                to="/ai" 
                class="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-medium rounded-lg hover:from-cyan-600 hover:to-blue-700 transition-all duration-200 shadow-lg shadow-cyan-500/30"
            >
                AI测试用例
            </router-link>
            <router-link 
                to="/test-report-beautifier" 
                class="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-medium rounded-lg hover:from-cyan-600 hover:to-blue-700 transition-all duration-200 shadow-lg shadow-cyan-500/30"
            >
                测试报告美化
            </router-link>
            <router-link 
                to="/api-auto-test" 
                class="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-medium rounded-lg hover:from-cyan-600 hover:to-blue-700 transition-all duration-200 shadow-lg shadow-cyan-500/30"
            >
                接口自动化工厂
            </router-link>
        </div>

        <div class="text-left mt-10 bg-[#0f1419] rounded-xl p-6 border border-[#1a2332]">
            <h2 class="text-2xl font-semibold text-white border-b-2 border-cyan-500 pb-2 mb-4">功能介绍</h2>
            <ul class="space-y-3">
                <li class="flex items-start text-gray-300">
                    <span class="text-cyan-500 mr-3">•</span>
                    <span>AI自动化测试用例生成</span>
                </li>
                <li class="flex items-start text-gray-300">
                    <span class="text-cyan-500 mr-3">•</span>
                    <span>测试报告美化与分析</span>
                </li>
                <li class="flex items-start text-gray-300">
                    <span class="text-cyan-500 mr-3">•</span>
                    <span>接口自动化测试脚本生成与执行</span>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
</script>
