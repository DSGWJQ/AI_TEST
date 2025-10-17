<template>
  <nav class="sticky top-0 z-50 w-full bg-gray-50 border-b">
    <div class="max-w-screen-xl mx-auto px-4 py-3 flex items-center">
      <!-- 左侧：网站名称和Logo -->
      <div class="flex items-center gap-x-3">
        <div class="flex items-center gap-x-2">
          <img 
            src="/GIF_MAO.gif" 
            alt="网站Logo" 
            class="w-8 h-8 object-contain"
          />
          <h1 class="text-xl font-bold text-gray-800">测试工具平台</h1>
        </div>
      </div>

      <!-- 右侧：页面导航按钮 -->
      <div class="flex items-center gap-3 ml-auto">
        <RouterLink to="/ai" custom v-slot="{ navigate, isActive }">
          <button 
            @click="navigate" 
            :class="buttonClass(isActive)"
          >
            <span class="mr-2">🤖</span>
            AI测试工具
          </button>
        </RouterLink>
        <RouterLink to="/test-report-beautifier" custom v-slot="{ navigate, isActive }">
          <button 
            @click="navigate" 
            :class="buttonClass(isActive)"
          >
            <span class="mr-2">📊</span>
            测试报告美化
          </button>
        </RouterLink>
        <RouterLink to="/api-auto-test" custom v-slot="{ navigate, isActive }">
          <button 
            @click="navigate" 
            :class="buttonClass(isActive)"
          >
            <span class="mr-2">🔧</span>
            接口自动化工厂
          </button>
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
// 按钮样式：匹配ai_Test_case.vue的渐变按钮样式
const buttonClass = (isActive) =>
  isActive
    ? 'px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium rounded-xl hover:from-blue-600 hover:to-blue-700 transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center'
    : 'px-6 py-3 bg-gradient-to-r from-gray-400 to-gray-500 text-white font-medium rounded-xl hover:from-gray-500 hover:to-gray-600 transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center'
</script>