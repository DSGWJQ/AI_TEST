<template>
  <div class="max-w-[1400px] mx-auto p-6 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 flex items-center">
      AI自动化测试工具
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
            <span v-else class="text-green-600 text-sm">已配置 API Key</span>
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

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 输入区域 -->
      <div class="lg:col-span-1">
        <label class="block mb-3 font-semibold text-gray-700 flex items-center">
          输入需求文档：
        </label>
        <textarea
          class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-y text-sm leading-relaxed bg-gray-50"
          v-model="inputText"
          placeholder="请输入您的产品需求文档..."
          rows="12"
        ></textarea>
      </div>

      <!-- 按钮区域 -->
      <div class="lg:col-span-1">
        <div class="flex flex-wrap items-center gap-3">
          <button
            class="px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium rounded-xl hover:from-blue-600 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            @click="generateTextCases"
            :disabled="isProcessing"
          >
            {{ isProcessing ? '处理中...' : '文本用例生成' }}
          </button>

          <button
            class="px-6 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white font-medium rounded-xl hover:from-purple-600 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            @click="generatePytestCases"
            :disabled="isProcessing"
          >
            {{ isProcessing ? '处理中...' : 'pytest用例生成' }}
          </button>

          <button
            class="px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-medium rounded-xl hover:from-green-600 hover:to-green-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            @click="selfReview"
            :disabled="isProcessing || !outputText"
          >
            {{ isProcessing ? '处理中...' : '自动审查优化' }}
          </button>
        </div>
      </div>

      <!-- 输出区域 -->
      <div class="lg:col-span-1">
        <label class="block mb-3 font-semibold text-gray-700 flex items-center">
          生成的测试用例：
        </label>
        <textarea
          class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-y text-sm leading-relaxed font-mono bg-gray-900 text-green-400"
          v-model="outputText"
          placeholder="生成的测试用例将显示在这里..."
          rows="12"
        ></textarea>
      </div>
    </div>

    <!-- 审查结果区域 -->
    <div v-if="reviewResult" class="mt-6 bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
      <h3 class="text-xl font-semibold mb-4 text-gray-800 flex items-center">
        审查结果：
      </h3>
      <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
        <pre class="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50">{{ reviewResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
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
const inputText = ref("")
const outputText = ref("")
const reviewResult = ref("")
const originalOutput = ref("")
const isProcessing = ref(false)

// AI调用包装函数
async function callAIWrapper(prompt) {
  if (!apiKey.value && modelSource.value === 'online') {
    throw new Error('请先设置 OpenRouter API Key')
  }
  return await callAI(prompt, modelSource.value, selectedModel.value, apiKey.value, OLLAMA_URL)
}

// 文本用例生成
async function generateTextCases() {
  try {
    validateInput(inputText.value, '需求文档')
    if (isProcessing.value) return

    isProcessing.value = true

    const prompt = `
# Role: 测试用例设计专家

## Profile
- language: 中文
- description: 基于需求文档构建包含功能、性能、安全及兼容性验证的完整测试用例体系

## Rules
1. 全面性: 覆盖需求文档所有功能点
2. 可执行性: 用例需包含明确操作步骤
3. 独立性: 单个用例应可单独执行验证

## Workflows
1. 解析需求文档中的功能模块与业务规则
2. 通过场景法拆分核心业务流程
3. 编写用例执行步骤与预期结果
4. 建立用例优先级与风险等级评估

## OutputFormat
测试用例包含：编号、标题、前置条件、操作步骤、预期结果、优先级

需求文档内容：
${inputText.value}
`

    const content = await callAIWrapper(prompt)
    outputText.value = content || ""
    originalOutput.value = outputText.value
    showSuccess('文本测试用例生成完成')

  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false
  }
}

// pytest用例生成
async function generatePytestCases() {
  try {
    validateInput(inputText.value, '需求文档')
    if (isProcessing.value) return

    isProcessing.value = true

    const prompt = `你是一个超级测试专家，擅长编写 pytest 测试用例。请根据以下需求文档生成完整的 pytest 测试脚本：

需求文档：
${inputText.value}

要求：
1. 生成符合 pytest 标准格式的 Python 脚本
2. 包含完整的测试用例，可以直接执行
3. 覆盖主要功能点和边界情况
4. 包含必要的 import 语句和 fixture
5. 使用参数化测试提高覆盖率
6. 只返回代码，不要添加解释

请直接返回可执行的 pytest 脚本：`

    const content = await callAIWrapper(prompt)
    outputText.value = content || ""
    originalOutput.value = outputText.value
    showSuccess('pytest测试用例生成完成')

  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false
  }
}

// 测试用例自审
async function selfReview() {
  try {
    validateInput(outputText.value, '测试用例')
    if (isProcessing.value) return

    isProcessing.value = true

    const reviewPrompt = `你是一个严格的测试用例审查专家，请对以下测试用例进行全面审查：

${outputText.value}

请从以下角度进行审查：
1. 代码语法和结构是否正确（如果是代码）
2. 测试覆盖是否充分
3. 断言是否合理（如果是代码）
4. 测试步骤是否清晰（如果是文本用例）
5. 是否有潜在的bug或改进点
6. 提供修正后的完整内容

请提供详细的审查报告和修正后的内容：`

    const content = await callAIWrapper(reviewPrompt)
    reviewResult.value = content || ""
    showSuccess('测试用例审查完成')

    setTimeout(() => {
      if (confirm("是否要用修正后的测试用例替换原版本？")) {
        const correctedContent = extractCorrectedContent(reviewResult.value)
        if (correctedContent) {
          outputText.value = correctedContent
          showSuccess('测试用例已更新')
        }
      }
    }, 100)

  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false
  }
}

function extractCorrectedContent(reviewContent) {
  try {
    const codeBlockMatch = reviewContent.match(/```[\s\S]*?```/g)
    if (codeBlockMatch && codeBlockMatch.length > 0) {
      return codeBlockMatch[codeBlockMatch.length - 1]
        .replace(/^```[\w]*\n?/, '')
        .replace(/\n?```$/, '')
    }
    return null
  } catch (error) {
    console.error('提取修正内容失败:', error)
    return null
  }
}
</script>
