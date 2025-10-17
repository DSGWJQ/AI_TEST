<template>
  <div class="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 flex items-center">
      <span class="mr-3">🚀</span>
      接口自动化测试工厂
    </h1>

    <!-- 优化的模型配置区域 -->
    <section class="mb-6 p-4 bg-white rounded-xl shadow-md border border-gray-200">
      <h2 class="text-lg font-semibold mb-3 text-gray-700">模型配置</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex items-center gap-4">
          <label class="font-medium text-gray-600">模型来源：</label>
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
          <label class="font-medium text-gray-600">模型：</label>
          <select v-model="selectedModel" class="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all">
            <option v-for="m in availableModels" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
      </div>
    </section>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 输入区域 -->
      <div class="space-y-6">
        <!-- 需求输入 -->
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="mr-2">📋</span>
            需求文档
          </h3>
          <textarea 
            v-model="inputText" 
            rows="8" 
            placeholder="请输入接口需求文档..." 
            class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all resize-none"
          ></textarea>
        </div>

        <!-- 源代码输入 -->
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="mr-2">💻</span>
            源代码（可选）
          </h3>
          <textarea 
            v-model="sourceCode" 
            rows="8" 
            placeholder="可选：粘贴相关源代码以提高生成质量..." 
            class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all font-mono text-sm resize-none"
          ></textarea>
        </div>
      </div>

      <!-- 操作按钮区域 -->
      <div class="flex flex-col gap-4 justify-start">
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-4 text-gray-700 flex items-center">
            <span class="mr-2">🛠️</span>
            操作流程
          </h3>
          <div class="flex flex-wrap gap-3 items-center">
            <button 
              @click="generateTestScript" 
              :disabled="isProcessing"
              class="px-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium rounded-lg hover:from-blue-600 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">1️⃣</span>
              {{ isProcessing ? '生成中...' : '生成测试脚本' }}
            </button>
            
            <button 
              @click="selfReview" 
              :disabled="!originalOutput || isProcessing"
              class="px-4 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-medium rounded-lg hover:from-green-600 hover:to-green-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">2️⃣</span>
              {{ isProcessing ? '审查中...' : 'AI 审查并优化' }}
            </button>
            
            <button 
              @click="executeScript" 
              :disabled="!outputText || isProcessing"
              class="px-4 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white font-medium rounded-lg hover:from-purple-600 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">3️⃣</span>
              {{ isProcessing ? '执行中...' : '执行测试脚本' }}
            </button>
            
            <button 
              @click="generateAdvice" 
              :disabled="!execResultText || isProcessing"
              class="px-4 py-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-medium rounded-lg hover:from-orange-600 hover:to-orange-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
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
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="mr-2">📄</span>
            生成的测试脚本
          </h3>
          <textarea 
            v-model="outputText" 
            rows="8" 
            placeholder="生成的测试脚本将显示在这里..." 
            class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all font-mono text-sm resize-none"
          ></textarea>
        </div>

        <!-- 执行结果 -->
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="mr-2">⚡</span>
            执行结果
          </h3>
          <textarea 
            v-model="execResultText" 
            rows="8" 
            placeholder="脚本执行结果将显示在这里..." 
            class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all font-mono text-sm resize-none"
          ></textarea>
        </div>
      </div>
    </div>

    <!-- 优化建议区域 -->
    <div v-if="finalAdvice" class="mt-6 bg-white p-6 rounded-xl shadow-md border border-gray-200">
      <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
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
import { ref, computed } from 'vue'
import { callAI, validateInput, showSuccess, showError } from '../utils/errorHandler'
import { testAPI } from '../api'  // 导入 testAPI

const inputText = ref('')
const sourceCode = ref('')
const originalOutput = ref('')
const outputText = ref('')
const execResultText = ref('')
const finalAdvice = ref('')
const isProcessing = ref(false)

// 页面内独立模型配置
const modelSource = ref('local')
const selectedModel = ref('deepseek-r1:7b')
const onlineModels = [
  'meta-llama/llama-3.3-70b-instruct:free',
  'deepseek/deepseek-r1:free'
]
const localModels = ['deepseek-r1:7b', 'qwen:4b']
const availableModels = computed(() => (modelSource.value === 'online' ? onlineModels : localModels))

// 写死的配置
const HARDCODED_API_KEY = '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'
const HARDCODED_OLLAMA_URL = 'http://localhost:11434/v1'

// 统一的AI调用函数
async function callAIWrapper(prompt) {
  return await callAI(prompt, modelSource.value, selectedModel.value, HARDCODED_API_KEY, HARDCODED_OLLAMA_URL)
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
1. 必须在文件开头导入：import pytest, import requests, import json, import time（禁止使用 unittest）
2. 所有测试函数必须以 test_ 开头；如使用测试类，类名以 Test 开头且方法以 test_ 开头
3. 使用 requests 库进行 HTTP 请求，所有请求必须设置 timeout=10
4. 基础 URL 必须使用：http://localhost:8000（注意是 8000 端口）
5. 仅使用以下 API 端点：
   - POST /register - 用户注册，参数：{"username": "用户名", "password": "密码"}
   - POST /login - 用户登录，参数：{"username": "用户名", "password": "密码"}
   - POST /send-code - 发送验证码，参数：{"email": "邮箱"}
   - POST /verify-code - 验证码验证，参数：{"email": "邮箱", "code": "验证码"}
   - GET / - 根路径测试，返回：{"code": 200, "msg": "success", "data": {"hello": "world"}}
6. 响应格式为：{"code": 200, "msg": "success", "data": {...}}
7. 覆盖正常与异常场景，添加必要断言与错误处理
8. 禁止包含 if __name__ == "__main__" 或 unittest.main()，脚本需可通过 pytest 直接运行
9. 优先使用 pytest fixture 管理通用数据（如 base_url、登录态、公共请求头等）
10. 确保至少包含一个可收集的测试函数（以 test_ 开头）
11. 如需唯一标识符，使用 time.time() 并确保已导入

重要：请直接输出 Python 代码，不要包含任何中文解释、说明文字或代码块标记。第一行必须是 Python 代码（如 import 语句）。`

    const content = await callAIWrapper(prompt)
    
    // 清理AI返回的内容，移除思考标签和非代码内容
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
    
    const prompt = `请审查以下基于 pytest 的接口测试脚本并提供优化后的完整版本（保持 pytest 与 test_ 规范）：

${originalOutput.value}

审查要点：
1. 代码语法和逻辑是否正确
2. 测试覆盖是否充分（正常/异常/边界）
3. 断言与错误处理是否合理
4. 代码结构与可读性是否良好（fixture/参数化等）
5. 性能与稳定性建议

重要：请直接输出修正后的完整 pytest 脚本，不要包含任何中文解释、说明文字或代码块标记。第一行必须是 Python 代码（如 import 语句）。`

    const content = await callAIWrapper(prompt)
    
    // 清理AI返回的内容
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

// 清理AI返回的内容，移除思考标签和非代码内容
function cleanAIResponse(content) {
  if (!content) return ''
  
  let cleaned = content
  
  // 移除 <think> 标签及其内容
  cleaned = cleaned.replace(/<think>[\s\S]*?<\/think>/gi, '')
  
  // 移除其他可能的标签
  cleaned = cleaned.replace(/<[^>]*>/g, '')
  
  // 移除代码块标记
  cleaned = cleaned.replace(/```python\n?/g, '')
  cleaned = cleaned.replace(/```\n?/g, '')
  
  // 按行处理，移除解释性文字
  const lines = cleaned.split('\n')
  const cleanedLines = []
  let foundCode = false
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    // 跳过空行
    if (line === '') {
      if (foundCode) cleanedLines.push('')
      continue
    }
    
    // 检查是否是有效的Python代码行
    const isValidPythonLine = (
      line.startsWith('import ') ||
      line.startsWith('from ') ||
      line.startsWith('def ') ||
      line.startsWith('class ') ||
      line.startsWith('#') ||
      line.startsWith('@') ||  // 装饰器
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
      /^[a-zA-Z_][a-zA-Z0-9_]*\s*=/.test(line) ||  // 变量赋值
      /^[a-zA-Z_][a-zA-Z0-9_]*\s*\(/.test(line) ||  // 函数调用
      /^\s+/.test(lines[i]) && foundCode  // 缩进行（在找到代码后）
    )
    
    // 检查是否是中文解释行
    const chineseCount = (line.match(/[\u4e00-\u9fff]/g) || []).length
    const isChineseExplanation = (
      chineseCount > line.length * 0.3 &&  // 中文字符超过30%
      !line.includes('"') &&  // 不是字符串
      !line.includes("'") &&  // 不是字符串
      !line.startsWith('#')   // 不是注释
    )
    
    // 如果是有效的Python代码行，保留它
    if (isValidPythonLine && !isChineseExplanation) {
      foundCode = true
      cleanedLines.push(lines[i])  // 保持原始缩进
    } else if (foundCode && !isChineseExplanation) {
      // 如果已经找到代码，且不是中文解释，也保留（可能是代码的一部分）
      cleanedLines.push(lines[i])
    }
    // 否则跳过这一行（中文解释或无效内容）
  }
  
  // 如果没有找到任何有效代码，返回原内容（避免过度清理）
  if (!foundCode) {
    console.warn('未找到有效的Python代码，返回原内容')
    return content.trim()
  }
  
  cleaned = cleanedLines.join('\n')
  
  // 清理多余的空行
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
    
    // 使用正确的 API 方法，增加超时时间到60秒
    const response = await testAPI.runCode(outputText.value, runner, 60)
    console.log('后端响应:', response)
    console.log('BaseResponse结构:', response.data)
    
    // 修复：正确获取执行结果数据
    const baseResponse = response.data
    const result = baseResponse.data  // 这里是真正的执行结果
    
    console.log('执行结果数据:', result)
    
    // 检查返回数据的完整性
    if (!result) {
      throw new Error('后端返回的执行结果数据为空')
    }
    
    // 处理返回结果
    let resultText = ''
    
    if (result.stdout && result.stdout.trim()) {
      resultText += `标准输出：\n${result.stdout}\n`
    }
    
    if (result.stderr && result.stderr.trim()) {
      resultText += `错误输出：\n${result.stderr}\n`
    }
    
    // 确保 exit_code 有值
    const exitCode = result.exit_code !== undefined ? result.exit_code : '未知'
    resultText += `退出码：${exitCode}`
    
    if (result.error) {
      resultText += `\n错误类型：${result.error}`
    }
    
    execResultText.value = resultText || '执行完成，无输出内容'
    
    // 根据退出码判断执行结果
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
      errorMessage = `服务器内部错误：${error.response?.data?.msg || '请检查脚本内容或联系管理员'}`
    } else if (error.response?.status === 408) {
      errorMessage = '脚本执行超时，请检查脚本是否有无限循环或耗时过长的操作'
    } else if (error.response?.data?.msg) {
      errorMessage = `执行失败：${error.response.data.msg}`
    } else {
      errorMessage = `执行失败：${error.message || '未知错误'}`
    }
    
    showError(errorMessage)
    execResultText.value = `❌ ${errorMessage}`
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