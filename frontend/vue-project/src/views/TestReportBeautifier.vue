<template>
  <div class="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 flex items-center">
      <span class="mr-3">✨</span>
      测试报告美化工具
    </h1>

    <!-- 模型配置区域 -->
    <section class="bg-white rounded-2xl shadow-lg p-6 mb-6 border border-gray-100">
      <h2 class="text-xl font-semibold mb-4 text-gray-800 flex items-center">模型配置</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-700 whitespace-nowrap">模型来源：</label>
          <div class="flex gap-3">
            <label class="flex items-center cursor-pointer hover:text-blue-600 transition-colors">
              <input type="radio" value="online" v-model="modelSource" class="mr-2 text-blue-600">
              在线（OpenRouter）
            </label>
            <label class="flex items-center cursor-pointer hover:text-blue-600 transition-colors">
              <input type="radio" value="local" v-model="modelSource" class="mr-2 text-blue-600">
              本地（Ollama）
            </label>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-700 whitespace-nowrap">模型：</label>
          <div class="flex items-center gap-2">
            <select v-model="selectedModel" class="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white text-gray-700 text-sm">
              <option v-for="m in availableModels" :key="m" :value="m">{{ m }}</option>
            </select>
            <button
              @click="refreshModels"
              :disabled="isRefreshing"
              class="p-2 text-white rounded-lg transition-colors disabled:cursor-not-allowed bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400"
              title="刷新模型列表"
            >
              🔄
            </button>
          </div>
        </div>

        <!-- API Key 配置 -->
        <div v-if="modelSource === 'online'" class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-700 whitespace-nowrap">API Key：</label>
          <div class="flex items-center gap-2 flex-1">
            <input
              v-if="showApiKeyInput"
              v-model="apiKey"
              type="password"
              placeholder="请输入 OpenRouter API Key (sk-or-v1-...)"
              class="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm flex-1"
            />
            <span v-else class="text-green-600 text-sm">✓ 已配置 API Key</span>
            <button
              @click="showApiKeyInput = !showApiKeyInput"
              class="p-2 text-white rounded-lg transition-colors disabled:cursor-not-allowed bg-gray-500 hover:bg-gray-600"
            >
              {{ showApiKeyInput ? '隐藏' : '设置' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 模型状态提示 -->
      <div v-if="modelStatus" class="mt-3 p-2 rounded-lg text-sm" :class="modelStatusClass">
        {{ modelStatus }}
      </div>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 左侧：文件上传和原始报告 -->
      <div class="space-y-6">
        <!-- 文件上传区域 -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 flex items-center">
            <span class="mr-2">📁</span>
            上传测试报告
          </h2>
          <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
            <input
              type="file"
              @change="handleReportUpload"
              accept=".html,.htm"
              class="hidden"
              id="fileInput"
            >
            <label for="fileInput" class="cursor-pointer">
              <div class="text-gray-500 mb-2">
                <span class="text-4xl">📄</span>
              </div>
              <p class="text-gray-600 font-medium">点击选择HTML测试报告文件</p>
              <p class="text-sm text-gray-400 mt-1">支持 .html, .htm 格式</p>
            </label>
          </div>
        </div>

        <!-- 原始报告预览 -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h3 class="text-xl font-semibold mb-4 text-gray-800 flex items-center">
            <span class="mr-2">📋</span>
            原始报告内容
          </h3>
          <textarea
            v-model="originalReport"
            rows="12"
            placeholder="上传的报告内容将显示在这里..."
            class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-y text-sm leading-relaxed font-mono bg-gray-900 text-green-400"
          ></textarea>
        </div>
      </div>

      <!-- 右侧：操作按钮和美化结果 -->
      <div class="space-y-6">
        <!-- 操作按钮区域 -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h3 class="text-xl font-semibold mb-4 text-gray-800 flex items-center">
            <span class="mr-2">🛠️</span>
            操作面板
          </h3>
          <div class="flex flex-wrap items-center gap-3">
            <button
              @click="generateReportSummary(originalReport)"
              :disabled="!originalReport || isProcessing"
              class="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium rounded-xl hover:from-blue-600 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">📊</span>
              {{ isProcessing ? '生成中...' : '生成报告摘要' }}
            </button>

            <button
              @click="beautifyReport"
              :disabled="!originalReport || isProcessing"
              class="px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-medium rounded-xl hover:from-green-600 hover:to-green-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">✨</span>
              {{ isProcessing ? '美化中...' : '美化报告' }}
            </button>

            <button
              @click="downloadBeautifiedReport"
              :disabled="!beautifiedReport"
              class="px-6 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white font-medium rounded-xl hover:from-purple-600 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">💾</span>
              下载美化报告
            </button>
          </div>
        </div>

        <!-- 报告摘要 -->
        <div v-if="reportSummary" class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h3 class="text-xl font-semibold mb-4 text-gray-800 flex items-center">
            <span class="mr-2">📊</span>
            报告摘要
          </h3>
          <div class="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p class="text-blue-800">{{ reportSummary }}</p>
          </div>
        </div>

        <!-- 美化结果 -->
        <div class="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
          <h3 class="text-xl font-semibold mb-4 text-gray-800 flex items-center">
            <span class="mr-2">✨</span>
            美化结果
          </h3>
          <textarea
            v-model="beautifiedReport"
            rows="12"
            placeholder="美化后的报告将显示在这里..."
            class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-y text-sm leading-relaxed font-mono bg-gray-900 text-green-400"
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { callAI, validateInput, showSuccess } from '../utils/errorHandler'
import { useModelConfig } from '../composables/useModelConfig'

// 使用公共模型配置
const {
  modelSource,
  selectedModel,
  isRefreshing,
  modelStatus,
  apiKey,
  showApiKeyInput,
  availableModels,
  modelStatusClass,
  refreshModels,
  OLLAMA_URL
} = useModelConfig()

// 页面状态
const originalReport = ref('')
const beautifiedReport = ref('')
const reportSummary = ref('')
const isProcessing = ref(false)

// AI调用包装函数
async function callAIWrapper(prompt) {
  if (!apiKey.value && modelSource.value === 'online') {
    throw new Error('请先设置 OpenRouter API Key')
  }
  return await callAI(prompt, modelSource.value, selectedModel.value, apiKey.value, OLLAMA_URL)
}

// 文件上传处理
function handleReportUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    originalReport.value = String(reader.result || "")
    showSuccess('文件上传成功')
  }
  reader.readAsText(file, "utf-8")
}

// 生成摘要
async function generateReportSummary(reportContent) {
  try {
    validateInput(reportContent, '测试报告内容')
    if (isProcessing.value) return

    isProcessing.value = true

    const summaryPrompt = `
# Role：自动化测试报告分析专家

## Goals:
- 准确统计测试总用例数及通过率
- 统计不同严重级别的问题数量
- 识别问题集中出现的功能模块
- 提供简洁的总结性语句

## OutputFormat:
以"📊 测试通过率X%，发现Y个问题，主要涉及Z功能模块"为开头

## 测试报告内容：
${reportContent.substring(0, 3000)}
    `

    reportSummary.value = await callAIWrapper(summaryPrompt)
    showSuccess('报告摘要生成完成')

  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false
  }
}

// 美化报告
async function beautifyReport() {
  try {
    validateInput(originalReport.value, '测试报告内容')
    if (isProcessing.value) return

    isProcessing.value = true

    const maxContentLength = 8000
    const truncatedContent = originalReport.value.length > maxContentLength
      ? originalReport.value.substring(0, maxContentLength) + '...(内容已截断)'
      : originalReport.value

    const beautifyPrompt = `
# Role: 测试报告美化专家

## Profile
- language: 中文
- description: 专业测试报告可视化优化专家

## Skills
1. HTML结构优化 - 重构原始报告DOM结构
2. CSS样式增强 - 创建现代简约的视觉主题

## Rules
1. 保留原始数据不变
2. 采用现代简约设计风格
3. 支持响应式布局

## OutputFormat
输出完整的HTML文件，包含内联CSS样式

## 原始报告内容：
${truncatedContent}
    `

    beautifiedReport.value = await callAIWrapper(beautifyPrompt)
    showSuccess('报告美化完成')

  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false
  }
}

// 下载美化报告
function downloadBeautifiedReport() {
  try {
    validateInput(beautifiedReport.value, '美化后的报告')

    const blob = new Blob([beautifiedReport.value], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'beautified-test-report.html'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    showSuccess('报告下载完成')
  } catch (error) {
    console.error('下载失败:', error)
    alert(`下载失败：${error.message}`)
  }
}
</script>
