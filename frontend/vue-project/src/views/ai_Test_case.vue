<template>
  <div class="max-w-[1400px] mx-auto p-6 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 flex items-center">
      <span class="mr-3">🤖</span>
      AI自动化测试工具
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
          <div class="flex items-center gap-2">
            <select v-model="selectedModel" class="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all flex-1">
              <option v-for="m in availableModels" :key="m" :value="m">{{ m }}</option>
            </select>
            <button 
              @click="refreshModels" 
              :disabled="isRefreshing"
              class="px-3 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 transition-colors"
              title="刷新模型列表"
            >
              <span v-if="isRefreshing">🔄</span>
              <span v-else">🔄</span>
            </button>
          </div>
        </div>
        
        <!-- API Key 配置 -->
        <div v-if="modelSource === 'online'" class="flex items-center gap-4">
          <label class="font-medium text-gray-600">API Key：</label>
          <div class="flex items-center gap-2 flex-1">
            <input 
              v-if="showApiKeyInput"
              v-model="apiKey" 
              type="password" 
              placeholder="请输入 OpenRouter API Key (sk-or-v1-...)"
              class="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all flex-1 bg-gray-50"
            />
            <span v-else class="text-green-600 text-sm">✓ 已配置 API Key</span>
            <button 
              @click="showApiKeyInput = !showApiKeyInput"
              class="px-3 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors text-sm"
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
          <span class="mr-2">📋</span>
          输入需求文档：
        </label>
        <textarea 
          class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm resize-none bg-gray-50" 
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
            <span class="mr-2">📝</span>
            {{ isProcessing ? '处理中...' : '文本用例生成' }}
          </button>
          
          <button 
            class="px-6 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white font-medium rounded-xl hover:from-purple-600 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center" 
            @click="generatePytestCases"
            :disabled="isProcessing"
          >
            <span class="mr-2">🐍</span>
            {{ isProcessing ? '处理中...' : 'pytest用例生成' }}
          </button>
          
          <button 
            class="px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-medium rounded-xl hover:from-green-600 hover:to-green-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center" 
            @click="selfReview"
            :disabled="isProcessing || !outputText"
          >
            <span class="mr-2">🔍</span>
            {{ isProcessing ? '处理中...' : '自动审查优化' }}
          </button>
        </div>
      </div>

      <!-- 输出区域 -->
      <div class="lg:col-span-1">
        <label class="block mb-3 font-semibold text-gray-700 flex items-center">
          <span class="mr-2">📄</span>
          生成的测试用例：
        </label>
        <textarea 
          class="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all shadow-sm resize-none font-mono text-sm" 
          v-model="outputText" 
          placeholder="生成的测试用例将显示在这里..." 
          rows="12"
        ></textarea>
      </div>
    </div>

    <!-- 审查结果区域 -->
    <div v-if="reviewResult" class="mt-6 p-4 bg-white rounded-xl shadow-md border border-gray-200">
      <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
        <span class="mr-2">🔍</span>
        审查结果：
      </h3>
      <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
        <pre class="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50">{{ reviewResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { callAI, validateInput, showSuccess } from '../utils/errorHandler'

// 页面状态变量定义
const inputText = ref("")
const outputText = ref("")
const reviewResult = ref("")
const originalOutput = ref("")
const isProcessing = ref(false)

// 独立模型配置与调用
const modelSource = ref("online") // 默认使用在线模式，避免本地模型为空的问题
const selectedModel = ref("deepseek/deepseek-r1:free") // 默认选择一个在线免费模型
const isRefreshing = ref(false)
const modelStatus = ref("点击刷新按钮获取最新模型列表")

// 从环境变量获取配置，如果没有则使用默认值
const OPENROUTER_API_KEY = import.meta.env.VITE_OPENROUTER_API_KEY || ''
const OLLAMA_URL = import.meta.env.VITE_OLLAMA_URL || 'http://localhost:11434/v1'

// API Key 状态管理
const apiKey = ref(OPENROUTER_API_KEY)
const showApiKeyInput = ref(!OPENROUTER_API_KEY) // 如果没有环境变量中的 API Key，显示输入框

// 默认模型列表（作为备选）
const defaultOnlineModels = [
  'meta-llama/llama-3.3-70b-instruct:free',
  'deepseek/deepseek-r1:free',
  'google/gemini-flash-1.5:free',
  'microsoft/wizardlm-2-8x22b:free'
]
// 本地模型列表为空，需要用户手动添加或通过API获取
const defaultLocalModels = []

// 动态模型列表
const onlineModels = ref([...defaultOnlineModels])
const localModels = ref([]) // 初始为空，需要通过API获取或用户手动添加
const availableModels = computed(() => (modelSource.value === 'online' ? onlineModels.value : localModels.value))

// 模型状态样式
const modelStatusClass = computed(() => {
  if (modelStatus.value.includes('成功') || modelStatus.value.includes('可用')) {
    return 'bg-green-50 text-green-700 border border-green-200'
  } else if (modelStatus.value.includes('失败') || modelStatus.value.includes('错误')) {
    return 'bg-red-50 text-red-700 border border-red-200'
  } else if (modelStatus.value.includes('刷新中')) {
    return 'bg-blue-50 text-blue-700 border border-blue-200'
  }
  return 'bg-yellow-50 text-yellow-700 border border-yellow-200'
})

// 硬编码配置（仅作为备用，建议使用环境变量）
const HARDCODED_API_KEY = '' // 已移除硬编码，请使用环境变量或手动输入
const HARDCODED_OLLAMA_URL = OLLAMA_URL

// 统一的AI调用函数
async function callAIWrapper(prompt) {
  const currentApiKey = apiKey.value || HARDCODED_API_KEY
  if (!currentApiKey && modelSource.value === 'online') {
    throw new Error('请先设置 OpenRouter API Key')
  }
  return await callAI(prompt, modelSource.value, selectedModel.value, currentApiKey, HARDCODED_OLLAMA_URL)
}

// 刷新模型列表
async function refreshModels() {
  if (isRefreshing.value) return
  
  isRefreshing.value = true
  modelStatus.value = "正在刷新模型列表..."
  
  try {
    if (modelSource.value === 'online') {
      // 刷新在线模型列表
      await refreshOnlineModels()
    } else {
      // 刷新本地模型列表
      await refreshLocalModels()
    }
  } catch (error) {
    console.error('刷新模型列表失败:', error)
    modelStatus.value = `刷新失败: ${error.message}`
  } finally {
    isRefreshing.value = false
  }
}

// 刷新在线模型列表
async function refreshOnlineModels() {
  try {
    const currentApiKey = apiKey.value || HARDCODED_API_KEY
    if (!currentApiKey) {
      throw new Error('请先设置 API Key')
    }
    
    // 尝试获取OpenRouter的模型列表
    const response = await fetch('https://openrouter.ai/api/v1/models', {
      headers: {
        'Authorization': `Bearer ${currentApiKey}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      const freeModels = data.data
        ?.filter(model => model.pricing?.prompt === "0" || model.id.includes(':free'))
        ?.map(model => model.id)
        ?.slice(0, 10) // 限制数量避免列表过长
      
      if (freeModels && freeModels.length > 0) {
        onlineModels.value = [...new Set([...freeModels, ...defaultOnlineModels])]
        modelStatus.value = `成功获取 ${freeModels.length} 个在线模型`
      } else {
        throw new Error('未找到可用的免费模型')
      }
    } else {
      throw new Error(`API响应错误: ${response.status}`)
    }
  } catch (error) {
    // 如果获取失败，使用默认列表
    onlineModels.value = [...defaultOnlineModels]
    modelStatus.value = `使用默认在线模型列表 (${error.message})`
  }
}

// 刷新本地模型列表
async function refreshLocalModels() {
  try {
    // 尝试获取Ollama的模型列表
    // fetch到: http://localhost:11434/api/tags (Ollama的标准API端点)
    const response = await fetch(`${HARDCODED_OLLAMA_URL.replace('/v1', '')}/api/tags`)
    
    if (response.ok) {
      const data = await response.json()
      const installedModels = data.models?.map(model => model.name) || []
      
      if (installedModels.length > 0) {
        localModels.value = installedModels
        modelStatus.value = `发现 ${installedModels.length} 个已安装的本地模型`
      } else {
        localModels.value = []
        modelStatus.value = '未发现已安装的模型，请先使用 "ollama pull <模型名>" 下载模型'
      }
    } else {
      throw new Error('无法连接到Ollama服务 (http://localhost:11434)')
    }
  } catch (error) {
    // 如果获取失败，清空列表并提供指导
    localModels.value = []
    if (error.message.includes('Failed to fetch')) {
      modelStatus.value = 'Ollama服务未启动，请先启动Ollama服务，然后下载模型：ollama pull deepseek-r1:7b'
    } else {
      modelStatus.value = `连接失败: ${error.message}`
    }
  }
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
- description: 基于需求文档构建包含功能、性能、安全及兼容性验证的完整测试用例体系，确保覆盖所有业务场景与技术边界
- background: 拥有10年以上软件测试经验，精通黑盒测试、白盒测试、自动化测试框架设计及测试工具链应用
- personality: 严谨细致、逻辑清晰、善于沟通、具备风险预判能力
- expertise: 软件测试方法论、测试场景建模、接口测试设计、测试优先级评估
- target_audience: 软件开发人员、测试工程师、项目管理者及质量保证团队

## Skills

1. 测试用例设计
   - 等价类划分: 识别有效/无效输入集合
   - 边界值分析: 验证极端数据处理逻辑
   - 场景法设计: 构建业务流程分支路径
   - 接口测试: 设计API交互验证点

2. 测试工具应用
   - Postman测试: 编写API测试脚本
   - Selenium测试: 设计Web界面操作路径
   - JMeter测试: 制定性能压测方案
   - TestRail管理: 构建测试用例库结构

## Rules

1. 基本原则：
   - 全面性: 覆盖需求文档所有功能点
   - 可执行性: 用例需包含明确操作步骤
   - 独立性: 单个用例应可单独执行验证
   - 可追溯性: 每个用例需标注对应需求编号

2. 行为准则：
   - 遵循IEEE 829测试用例标准
   - 保持中立客观，不添加主观判断
   - 使用行业标准测试术语
   - 及时反馈用例执行中的潜在风险

3. 限制条件：
   - 不涉及代码开发工作
   - 不提供调试或故障排查服务
   - 不修改原始需求文档内容
   - 不承担非功能测试（如兼容性测试）需求

## Workflows

- 目标: 生成结构化且可执行的测试用例文档
- 步骤 1: 解析需求文档中的功能模块与业务规则
- 步骤 2: 通过场景法拆分核心业务流程
- 步骤 3: 应用测试设计技术构建验证点矩阵
- 步骤 4: 按测试类型划分用例分类体系
- 步骤 5: 制定测试数据准备方案
- 步骤 6: 编写用例执行步骤与预期结果
- 步骤 7: 建立用例优先级与风险等级评估
- 步骤 8: 生成测试用例编号与版本控制信息
- 步骤 9: 完成用例评审与可执行性验证
- 预期结果: 产出包含测试套件、测试用例列表、前置条件、操作步骤、预期结果、实际结果、优先级标注的完整测试文档

## OutputFormat

1. 输出格式类型：
   - format: text/markdown
   - structure: 
     - 测试套件封面：含项目名称、模块编号、版本信息
     - 测试用例列表：按功能模块分类展示
     - 用例详情：包含编号、标题、前置条件、操作步骤、预期结果、实际结果、优先级
     - 附录：含测试数据准备说明、风险分析文档
   - style: 采用测试用例标准模板，使用表头、列表、代码块强调关键信息
   - special_requirements: 必须包含测试用例状态字段（如通过/失败/未执行）

2. 格式规范：
   - indentation: 使用4个空格缩进
   - sections: 包含测试套件、测试用例、附录等章节
   - highlighting: 使用\`代码块\`标注操作步骤与预期结果，

3. 验证规则：
   - validation: 所有用例必须包含操作步骤与预期结果字段，
   - constraints: 用例编号需采用字母数字组合，长度不超过10位
   - error_handling: 遇到无法解析的需求点时，需标注"需求待澄清"状态

4. 示例说明：
   1. 示例1：
      - 标题: 用户注册功能测试
      - 格式类型: text/markdown
      - 说明: 覆盖正常注册、重复注册、异常注册场景
      - 示例内容: |
          ## 测试套件: 用户注册模块 V1.0
          ### 测试用例: TC_REG_001
          **前置条件**: 无
          **操作步骤**:
          1. 访问注册页面
          2. 输入有效邮箱与密码
          3. 点击注册按钮
          **预期结果**:
          - 显示注册成功提示
          - 生成用户账户
          **实际结果**: 
          - [待执行]
          **优先级**: 高
          **风险等级**: 低
      2. 示例2：
      - 标题: 支付流程测试
      - 格式类型: text/markdown
      - 说明: 包含支付成功、支付失败、异常金额等测试场景
      - 示例内容: |
          ## 测试套件: 支付系统功能 V2.0
          ### 测试用例: TC_PAY_003
          **前置条件**: 用户已登录并绑定支付方式
          **操作步骤**:
          1. 选择商品并加入购物车
          2. 进入结算页面
          3. 输入金额100元
          4. 选择支付方式
          5. 点击支付按钮
          **预期结果**:
          - 显示支付成功状态
          - 扣除相应账户余额
          **实际结果**: 
          - [待执行]
          **优先级**: 中
          **风险等级**: 高

## Initialization
作为测试用例设计专家，你必须遵守上述Rules，按照Workflows执行任务，并按照[输出格式]输出。
需求文档内容：
${inputText.value}
`;

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


