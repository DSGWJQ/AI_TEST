<template>
  <!-- Speedtest 风格的深色导航栏 -->
  <nav class="sticky top-0 z-50 w-full bg-[#0f1419] border-b border-[#1a2332]">
    <div class="max-w-screen-xl mx-auto px-4 py-3 flex items-center">
      <!-- 左侧：网站名称和Logo -->
      <div class="flex items-center gap-x-3">
        <div class="flex items-center gap-x-2">
          <div class="w-8 h-8 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-sm">测</span>
          </div>
          <h1 class="text-xl font-bold text-white">测试工具平台</h1>
        </div>
      </div>

      <!-- 右侧：页面导航按钮 -->
      <div class="flex items-center gap-3 ml-auto">
        <RouterLink to="/ai" custom v-slot="{ navigate, isActive }">
          <button 
            @click="navigate" 
            :class="buttonClass(isActive)"
          >
            AI测试工具
          </button>
        </RouterLink>
        <RouterLink to="/test-report-beautifier" custom v-slot="{ navigate, isActive }">
          <button 
            @click="navigate" 
            :class="buttonClass(isActive)"
          >
            测试报告美化
          </button>
        </RouterLink>
        <RouterLink to="/api-auto-test" custom v-slot="{ navigate, isActive }">
          <button 
            @click="navigate" 
            :class="buttonClass(isActive)"
          >
            接口自动化工厂
          </button>
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
const buttonClass = (isActive) =>
  isActive
    ? 'px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-medium rounded-lg hover:from-cyan-600 hover:to-blue-700 transition-all duration-200 shadow-lg shadow-cyan-500/30'
    : 'px-5 py-2.5 bg-[#1a2332] text-gray-300 font-medium rounded-lg hover:bg-[#2d3e50] hover:text-white transition-all duration-200'
</script>
