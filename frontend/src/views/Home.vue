<template>
    <div class="max-w-[800px] mx-auto p-5 text-center">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">欢迎来到测试工具平台</h1>
        <p class="text-gray-600 mb-5">一站式测试自动化解决方案</p>
        <div class="my-8 flex justify-center flex-wrap gap-3">
            <router-link to="/ai" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">AI测试用例</router-link>
            <router-link to="/test-report-beautifier" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">测试报告美化</router-link>
            <router-link to="/api-auto-test" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">接口自动化工厂</router-link>
        </div>

        <div class="text-left mt-8">
            <h2 class="text-xl font-semibold text-gray-800 border-b-2 border-blue-600 pb-1">功能介绍</h2>
            <ul class="list-disc pl-5">
                <li class="my-2 text-gray-700">AI自动化测试用例生成</li>
                <li class="my-2 text-gray-700">测试报告美化与分析</li>
                <li class="my-2 text-gray-700">接口自动化测试脚本生成与执行</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
</script>
