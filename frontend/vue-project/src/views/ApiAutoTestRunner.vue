<template>
  <div class="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
    <h1 class="page-title">
      <span class="mr-3">🚀</span>
      接口自动化测试工厂
    </h1>

    <!-- 模型配置区域 -->
    <section class="config-section">
      <h2 class="section-title">模型配置</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex items-center gap-4">
          <label class="label-text">模型来源：</label>
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
          <label class="label-text">模型：</label>
          <div class="flex items-center gap-2">
            <select v-model="selectedModel" class="select-base">
              <option v-for="m in availableModels" :key="m" :value="m">{{ m }}</option>
            </select>
            <button
              @click="refreshModels"
              :disabled="isRefreshing"
              class="btn-small bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400"
              title="刷新模型列表"
            >
              🔄
            </button>
          </div>
        </div>

        <!-- API Key 配置 -->
        <div v-if="modelSource === 'online'" class="flex items-center gap-4">
          <label class="label-text">API Key：</label>
          <div class="flex items-center gap-2 flex-1">
            <input
              v-if="showApiKeyInput"
              v-model="apiKey"
              type="password"
              placeholder="请输入 OpenRouter API Key (sk-or-v1-...)"
              class="input-password flex-1"
            />
            <span v-else class="text-green-600 text-sm">✓ 已配置 API Key</span>
            <button
              @click="showApiKeyInput = !showApiKeyInput"
              class="btn-small bg-gray-500 hover:bg-gray-600"
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
        <div class="card">
          <h3 class="section-title">
            <span class="mr-2">📋</span>
            需求文档
          </h3>
          <textarea
            v-model="inputText"
            rows="8"
            placeholder="请输入接口需求文档..."
            class="textarea-base"
          ></textarea>
        </div>

        <!-- 源代码输入 -->
        <div class="card">
          <h3 class="section-title">
            <span class="mr-2">💻</span>
            源代码（可选）
          </h3>
          <textarea
            v-model="sourceCode"
            rows="8"
            placeholder="可选：粘贴相关源代码以提高生成质量..."
            class="textarea-code"
          ></textarea>
        </div>
      </div>

      <!-- 操作按钮区域 -->
      <div class="flex flex-col gap-4 justify-start">
        <div class="card">
          <h3 class="section-title">
            <span class="mr-2">🛠️</span>
            操作流程
          </h3>
          <div class="flex flex-wrap gap-3 items-center">
            <button
              @click="generateTestScript"
              :disabled="isProcessing"
              class="btn-primary"
            >
              <span class="mr-2">1️⃣</span>
              {{ isProcessing ? '生成中...' : '生成测试脚本' }}
            </button>

            <button
              @click="selfReview"
              :disabled="!originalOutput || isProcessing"
              class="btn-secondary"
            >
              <span class="mr-2">2️⃣</span>
              {{ isProcessing ? '审查中...' : 'AI 审查并优化' }}
            </button>

            <button
              @click="executeScript"
              :disabled="!outputText || isProcessing"
              class="btn-accent"
            >
              <span class="mr-2">3️⃣</span>
              {{ isProcessing ? '执行中...' : '执行测试脚本' }}
            </button>

            <button
              @click="generateAdvice"
              :disabled="!execResultText || isProcessing"
              class="btn-warning"
            >
              <span class="mr-2">4️⃣</span>
              {{ isProcessing ? '分析中...' : '生成优化建议' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 输出区域 -->
      <div class="space-y-6">
        <!-- 生成的脚本 -->
        <div class="card">
          <h3 class="section-title">
            <span class="mr-2">📄</span>
            生成的测试脚本
          </h3>
          <textarea
            v-model="outputText"
            rows="8"
            placeholder="生成的测试脚本将显示在这里..."
            class="textarea-code"
          ></textarea>
        </div>

        <!-- 执行结果 -->
        <div class="card">
          <h3 class="section-title">
            <span class="mr-2">⚡</span>
            执行结果
          </h3>
          <textarea
            v-model="execResultText"
            rows="8"
            placeholder="脚本执行结果将显示在这里..."
            class="textarea-code"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- 优化建议区域 -->
    <div v-if="finalAdvice" class="mt-6 card">
      <h3 class="section-title">
        <span class="mr-2">💡</span>
        优化建议
      </h3>
      <div class="p-4 bg-orange-50 rounded-lg border border-orange-200">
        <pre class="whitespace-pre-wrap text-sm text-orange-800">{{ finalAdvice }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { callAI, validateInput, showSuccess, showError } from '../utils/errorHandler'
import { testAPI } from '../api'
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
const inputText = ref('')
const sourceCode = ref('')
const originalOutput = ref('')
const outputText = ref('')
const execResultText = ref('')
const finalAdvice = ref('')
const isProcessing = ref(false)

// AI调用包装函数
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
  cleaned = cleaned.replace(/```python\n?/g, '')
  cleaned = cleaned.replace(/```\n?/g, '')

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
