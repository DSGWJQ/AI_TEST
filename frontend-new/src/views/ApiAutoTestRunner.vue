<template>
  <div class="max-w-7xl mx-auto p-6 min-h-screen bg-[#0f1419]">
    <h1 class="text-3xl font-bold mb-6 text-white flex items-center">
      接口自动化测试工厂
    </h1>

    <!-- 模型配置区域 -->
    <section class="bg-[#0f1419] rounded-2xl shadow-lg p-6 mb-6 border border-[#1a2332]">
      <h2 class="text-xl font-semibold mb-4 text-white flex items-center">模型配置</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-300 whitespace-nowrap">模型来源：</label>
          <div class="flex gap-3">
            <label class="flex items-center cursor-pointer hover:text-cyan-400 transition-colors">
              <input type="radio" value="online" v-model="modelSource" class="mr-2 accent-cyan-500">
              <span class="text-gray-300">在线（OpenRouter）</span>
            </label>
            <label class="flex items-center cursor-pointer hover:text-cyan-400 transition-colors">
              <input type="radio" value="local" v-model="modelSource" class="mr-2 accent-cyan-500">
              <span class="text-gray-300">本地（Ollama）</span>
            </label>
          </div>
        </div>

        <div class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-300 whitespace-nowrap">模型：</label>
          <div class="flex items-center gap-2">
            <select v-model="selectedModel" class="px-4 py-2 border border-[#2d3e50] rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 bg-[#1a2332] text-gray-200 text-sm">
              <option v-for="m in availableModels" :key="m" :value="m">{{ m }}</option>
            </select>
            <button
              @click="refreshModels"
              :disabled="isRefreshing"
              class="p-2 text-white rounded-lg transition-colors disabled:cursor-not-allowed bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600"
              title="刷新模型列表"
            >
            </button>
          </div>
        </div>

        <!-- API Key 配置 -->
        <div v-if="modelSource === 'online'" class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-300 whitespace-nowrap">API Key：</label>
          <div class="flex items-center gap-2 flex-1">
            <input
              v-if="showApiKeyInput"
              v-model="apiKey"
              type="password"
              placeholder="请输入 OpenRouter API Key (sk-or-v1-...)"
              class="px-4 py-2 border border-[#2d3e50] rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 bg-[#1a2332] text-gray-200 text-sm flex-1"
            />
            <span v-else class="text-cyan-400 text-sm">已配置 API Key</span>
            <button
              @click="showApiKeyInput = !showApiKeyInput"
              class="p-2 text-white rounded-lg transition-colors bg-[#2d3e50] hover:bg-[#3d4e60]"
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
      <div class="space-y-6">
        <!-- 需求输入 -->
        <div class="bg-[#0f1419] rounded-2xl shadow-lg p-6 border border-[#1a2332]">
          <h3 class="text-xl font-semibold mb-4 text-white flex items-center">
            需求文档
          </h3>
          <textarea
            v-model="inputText"
            rows="8"
            placeholder="请输入接口需求文档..."
            class="w-full p-4 border border-[#2d3e50] rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 resize-y text-sm leading-relaxed bg-[#0f1419] text-gray-200"
          ></textarea>
        </div>

        <!-- 源代码输入 -->
        <div class="bg-[#0f1419] rounded-2xl shadow-lg p-6 border border-[#1a2332]">
          <h3 class="text-xl font-semibold mb-4 text-white flex items-center">
            源代码（可选）
          </h3>
          <textarea
            v-model="sourceCode"
            rows="8"
            placeholder="可选：粘贴相关源代码以提高生成质量..."
            class="w-full p-4 border border-[#2d3e50] rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 resize-y text-sm leading-relaxed font-mono bg-[#050810] text-cyan-300"
          ></textarea>
        </div>
      </div>

      <!-- 操作按钮区域 -->
      <div class="flex flex-col gap-4 justify-start">
        <div class="bg-[#0f1419] rounded-2xl shadow-lg p-6 border border-[#1a2332]">
          <h3 class="text-xl font-semibold mb-4 text-white flex items-center">
            操作流程
          </h3>
          <div class="flex flex-wrap gap-3 items-center">
            <button
              @click="generateTestScript"
              :disabled="isProcessing"
              class="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-medium rounded-xl hover:from-cyan-600 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg shadow-cyan-500/30"
            >
              {{ isProcessing ? '生成中...' : '生成测试脚本' }}
            </button>

            <button
              @click="selfReview"
              :disabled="!originalOutput || isProcessing"
              class="px-6 py-3 bg-gradient-to-r from-green-500 to-green-700 text-white font-medium rounded-xl hover:from-green-600 hover:to-green-800 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg shadow-green-500/30"
            >
              {{ isProcessing ? '审查中...' : 'AI 审查并优化' }}
            </button>

            <button
              @click="executeScript"
              :disabled="!outputText || isProcessing"
              class="px-6 py-3 bg-gradient-to-r from-purple-500 to-purple-700 text-white font-medium rounded-xl hover:from-purple-600 hover:to-purple-800 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg shadow-purple-500/30"
            >
              {{ isProcessing ? '执行中...' : '执行测试脚本' }}
            </button>

            <button
              @click="generateAdvice"
              :disabled="!execResultText || isProcessing"
              class="px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-700 text-white font-medium rounded-xl hover:from-orange-600 hover:to-orange-800 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg shadow-orange-500/30"
            >
              {{ isProcessing ? '分析中...' : '生成优化建议' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 输出区域 -->
      <div class="space-y-6">
        <!-- 生成的脚本 -->
        <div class="bg-[#0f1419] rounded-2xl shadow-lg p-6 border border-[#1a2332]">
          <h3 class="text-xl font-semibold mb-4 text-white flex items-center">
            生成的测试脚本
          </h3>
          <textarea
            v-model="outputText"
            rows="8"
            placeholder="生成的测试脚本将显示在这里..."
            class="w-full p-4 border border-[#2d3e50] rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 resize-y text-sm leading-relaxed font-mono bg-[#050810] text-cyan-300"
          ></textarea>
        </div>

        <!-- 执行结果 -->
        <div class="bg-[#0f1419] rounded-2xl shadow-lg p-6 border border-[#1a2332]">
          <h3 class="text-xl font-semibold mb-4 text-white flex items-center">
            执行结果
          </h3>
          <textarea
            v-model="execResultText"
            rows="8"
            placeholder="脚本执行结果将显示在这里..."
            class="w-full p-4 border border-[#2d3e50] rounded-xl focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 resize-y text-sm leading-relaxed font-mono bg-[#050810] text-cyan-300"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- 优化建议区域 -->
    <div v-if="finalAdvice" class="mt-6 bg-[#0f1419] rounded-2xl shadow-lg p-6 border border-[#1a2332]">
      <h3 class="text-xl font-semibold mb-4 text-white flex items-center">
        优化建议
      </h3>
      <div class="p-4 bg-[#050810] rounded-lg border border-orange-500/30">
        <pre class="whitespace-pre-wrap text-sm text-orange-300">{{ finalAdvice }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { callAI, validateInput, showSuccess, showError } from '../utils/errorHandler'
import { testAPI } from '../api'
import { useModelConfig, OLLAMA_URL } from '../composables/useModelConfig'

const {
  modelSource,
  selectedModel,
  isRefreshing,
  modelStatus,
  apiKey,
  showApiKeyInput,
  availableModels,
  modelStatusClass,
  refreshModels
} = useModelConfig()

const inputText = ref('')
const sourceCode = ref('')
const originalOutput = ref('')
const outputText = ref('')
const execResultText = ref('')
const finalAdvice = ref('')
const isProcessing = ref(false)

async function callAIWrapper(prompt) {
  if (!apiKey.value && modelSource.value === 'online') {
    throw new Error('请先设置 OpenRouter API Key')
  }
  return await callAI(prompt, modelSource.value, selectedModel.value, apiKey.value, OLLAMA_URL)
}

// 生成测试脚本
async function generateTestScript() {
  try {
    validateInput(inputText.value, '需求文档')
    if (isProcessing.value) return

    isProcessing.value = true

    const prompt = `作为专业的接口测试工程师，请根据需求文档生成基于 pytest 的 Python 接口测试脚本。

需求文档：
${inputText.value}

${sourceCode.value ? `参考源代码：\n${sourceCode.value}\n` : ''}

要求：
1. 必须在文件开头导入：import pytest, import requests, import json, import time
2. 所有测试函数必须以 test_ 开头
3. 使用 requests 库进行 HTTP 请求，所有请求必须设置 timeout=10
4. 基础 URL 必须使用：http://localhost:8000
5. 覆盖正常与异常场景，添加必要断言与错误处理
6. 优先使用 pytest fixture 管理通用数据

重要：请直接输出 Python 代码，不要包含任何解释或代码块标记。`

    const content = await callAIWrapper(prompt)
    const cleanedContent = cleanAIResponse(content)

    outputText.value = cleanedContent || ''
    originalOutput.value = outputText.value
    showSuccess('测试脚本生成完成')

  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false
  }
}

// AI审查并优化
async function selfReview() {
  try {
    validateInput(originalOutput.value, '测试脚本')
    if (isProcessing.value) return

    isProcessing.value = true

    const prompt = `请审查以下基于 pytest 的接口测试脚本并提供优化后的完整版本：

${originalOutput.value}

审查要点：
1. 代码语法和逻辑是否正确
2. 测试覆盖是否充分
3. 断言与错误处理是否合理
4. 代码结构与可读性是否良好

重要：请直接输出修正后的完整 pytest 脚本，不要包含任何解释或代码块标记。`

    const content = await callAIWrapper(prompt)
    const cleanedContent = cleanAIResponse(content)

    outputText.value = cleanedContent || originalOutput.value
    showSuccess('脚本审查优化完成')

  } catch (error) {
    console.error('AI审查失败:', error)
    showError(`AI审查失败：${error.message || '未知错误'}`)
  } finally {
    isProcessing.value = false
  }
}

// 清理AI返回的内容
function cleanAIResponse(content) {
  if (!content) return ''

  let cleaned = content

  // 移除 <think> 标签及其内容
  cleaned = cleaned.replace(/<think>[\s\S]*?<\/think>/gi, '')
  cleaned = cleaned.replace(/<[^>]*>/g, '')

  // 移除代码块标记
  cleaned = cleaned.replace(/\`\`\`python\n?/g, '')
  cleaned = cleaned.replace(/\`\`\`\n?/g, '')

  // 按行处理
  const lines = cleaned.split('\n')
  const cleanedLines = []
  let foundCode = false

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()

    if (line === '') {
      if (foundCode) cleanedLines.push('')
      continue
    }

    const isValidPythonLine = (
      line.startsWith('import ') ||
      line.startsWith('from ') ||
      line.startsWith('def ') ||
      line.startsWith('class ') ||
      line.startsWith('#') ||
      line.startsWith('@') ||
      line.startsWith('if ') ||
      line.startsWith('for ') ||
      line.startsWith('while ') ||
      line.startsWith('try:') ||
      line.startsWith('except') ||
      line.startsWith('finally:') ||
      line.startsWith('with ') ||
      line.startsWith('return ') ||
      line.startsWith('yield ') ||
      line.startsWith('raise ') ||
      line.startsWith('assert ') ||
      line.startsWith('print(') ||
      /^[a-zA-Z_][a-zA-Z0-9_]*\s*=/.test(line) ||
      /^[a-zA-Z_][a-zA-Z0-9_]*\s*\(/.test(line) ||
      /^\s+/.test(lines[i]) && foundCode
    )

    const chineseCount = (line.match(/[\u4e00-\u9fff]/g) || []).length
    const isChineseExplanation = (
      chineseCount > line.length * 0.3 &&
      !line.includes('"') &&
      !line.includes("'") &&
      !line.startsWith('#')
    )

    if (isValidPythonLine && !isChineseExplanation) {
      foundCode = true
      cleanedLines.push(lines[i])
    } else if (foundCode && !isChineseExplanation) {
      cleanedLines.push(lines[i])
    }
  }

  if (!foundCode) {
    console.warn('未找到有效的Python代码，返回原内容')
    return content.trim()
  }

  cleaned = cleanedLines.join('\n')
  cleaned = cleaned.replace(/\n{3,}/g, '\n\n')

  return cleaned.trim()
}

// 执行测试脚本
async function executeScript() {
  try {
    validateInput(outputText.value, '测试脚本')
    if (isProcessing.value) return

    isProcessing.value = true

    const runner = detectRunner(outputText.value)
    console.log('开始执行脚本，runner:', runner)

    const response = await testAPI.runCode(outputText.value, runner, 60)
    const baseResponse = response.data
    const result = baseResponse.data

    if (!result) {
      throw new Error('后端返回的执行结果数据为空')
    }

    let resultText = ''

    if (result.stdout && result.stdout.trim()) {
      resultText += `标准输出：\n${result.stdout}\n`
    }

    if (result.stderr && result.stderr.trim()) {
      resultText += `错误输出：\n${result.stderr}\n`
    }

    const exitCode = result.exit_code !== undefined ? result.exit_code : '未知'
    resultText += `退出码：${exitCode}`

    if (result.error) {
      resultText += `\n错误类型：${result.error}`
    }

    execResultText.value = resultText || '执行完成，无输出内容'

    if (result.exit_code === 0) {
      showSuccess('脚本执行成功')
    } else if (result.exit_code === undefined) {
      showError('脚本执行异常，未获取到退出码')
    } else {
      showError(`脚本执行失败，退出码：${result.exit_code}`)
    }

  } catch (error) {
    console.error('执行失败:', error)

    let errorMessage = '脚本执行失败'

    if (error.response?.status === 500) {
      errorMessage = `服务器内部错误：${error.response?.data?.msg || '请检查脚本内容'}`
    } else if (error.response?.status === 408) {
      errorMessage = '脚本执行超时'
    } else if (error.response?.data?.msg) {
      errorMessage = `执行失败：${error.response.data.msg}`
    } else {
      errorMessage = `执行失败：${error.message || '未知错误'}`
    }

    showError(errorMessage)
    execResultText.value = `${errorMessage}`
  } finally {
    isProcessing.value = false
  }
}

// 生成优化建议
async function generateAdvice() {
  try {
    validateInput(execResultText.value, '执行结果')
    if (isProcessing.value) return

    isProcessing.value = true

    const prompt = `基于以下测试脚本和执行结果，请提供详细的优化建议：

测试脚本：
${outputText.value}

执行结果：
${execResultText.value}

请提供：
1. 问题分析
2. 优化建议
3. 最佳实践
4. 后续改进方向`

    const content = await callAIWrapper(prompt)
    finalAdvice.value = content || ''
    showSuccess('优化建议生成完成')

  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false
  }
}

// 检测运行器类型
function detectRunner(code) {
  const hasPytestImport = /import\s+pytest/.test(code)
  const hasPytestWord = /\bpytest\b/.test(code)
  const hasTestFn = /def\s+test_[A-Za-z0-9_]+\s*\(/.test(code)
  const hasTestClass = /class\s+Test[A-Za-z0-9_]*\s*\(/.test(code)
  return (hasPytestImport || hasPytestWord || hasTestFn || hasTestClass) ? 'pytest' : 'python'
}
</script>
