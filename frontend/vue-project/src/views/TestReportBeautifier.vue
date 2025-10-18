<template>
  <div class="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-6 text-gray-800 flex items-center">
      <span class="mr-3">✨</span>
      测试报告美化工具
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
              <span v-else>🔄</span>
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

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 左侧：文件上传和原始报告 -->
      <div class="space-y-6">
        <!-- 文件上传区域 -->
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h2 class="text-xl font-semibold mb-4 text-gray-700 flex items-center">
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
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="mr-2">📋</span>
            原始报告内容
          </h3>
          <textarea 
            v-model="originalReport" 
            rows="12" 
            placeholder="上传的报告内容将显示在这里..." 
            class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all font-mono text-sm resize-none bg-gray-50"
          ></textarea>
        </div>
      </div>

      <!-- 右侧：操作按钮和美化结果 -->
      <div class="space-y-6">
        <!-- 操作按钮区域 -->
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-4 text-gray-700 flex items-center">
            <span class="mr-2">🛠️</span>
            操作面板
          </h3>
          <div class="flex flex-wrap items-center gap-3">
            <button 
              @click="generateReportSummary(originalReport)" 
              :disabled="!originalReport || isProcessing"
              class="px-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium rounded-lg hover:from-blue-600 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">📊</span>
              {{ isProcessing ? '生成中...' : '生成报告摘要' }}
            </button>
            
            <button 
              @click="beautifyReport" 
              :disabled="!originalReport || isProcessing"
              class="px-4 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-medium rounded-lg hover:from-green-600 hover:to-green-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">✨</span>
              {{ isProcessing ? '美化中...' : '美化报告' }}
            </button>
            
            <button 
              @click="downloadBeautifiedReport" 
              :disabled="!beautifiedReport"
              class="px-4 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white font-medium rounded-lg hover:from-purple-600 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex items-center justify-center"
            >
              <span class="mr-2">💾</span>
              下载美化报告
            </button>
          </div>
        </div>

        <!-- 报告摘要 -->
        <div v-if="reportSummary" class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="mr-2">📊</span>
            报告摘要
          </h3>
          <div class="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p class="text-blue-800">{{ reportSummary }}</p>
          </div>
        </div>

        <!-- 美化结果 -->
        <div class="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold mb-3 text-gray-700 flex items-center">
            <span class="mr-2">✨</span>
            美化结果
          </h3>
          <textarea 
            v-model="beautifiedReport" 
            rows="12" 
            placeholder="美化后的报告将显示在这里..." 
            class="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-all font-mono text-sm resize-none bg-gray-50"
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { callAI, validateInput, showSuccess } from '../utils/errorHandler'

// 响应式数据
const originalReport = ref('')
const beautifiedReport = ref('')
const reportSummary = ref('')
const isProcessing = ref(false)

// 页面内独立模型配置
const modelSource = ref('online') // 默认使用在线模式，避免本地模型为空的问题
const selectedModel = ref('deepseek/deepseek-r1:free') // 默认选择一个在线免费模型
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

// 文件上传处理
function handleReportUpload(e) {
  const file = e.target.files?.[0];
  if (!file) return;
  
  const reader = new FileReader();
  reader.onload = () => {
    originalReport.value = String(reader.result || "");
    showSuccess('文件上传成功');
  };
  reader.readAsText(file, "utf-8");
}

// 生成摘要
async function generateReportSummary(reportContent) {
  try {
    validateInput(reportContent, '测试报告内容')
    if (isProcessing.value) return
    
    isProcessing.value = true
    
    const summaryPrompt = `
# Role：自动化测试报告分析专家

## Background：  
用户需要快速评估pytest测试结果的总体质量与关键问题，通常用于项目进度汇报、缺陷跟踪或测试策略优化场景。测试报告包含详细的执行数据，但要求以简洁形式提炼核心指标，帮助决策者快速把握测试状态。

## Attention：  
需精准提取通过率、问题数量及模块分布等量化数据，避免过度解读。同时识别潜在风险，如关键模块失败或高优先级缺陷，为后续修复提供方向。

## Profile：  
- Author: prompt-optimizer  
- Version: 1.0  
- Language: 中文  
- Description: 专注于自动化测试报告分析，能高效解析HTML格式测试结果，提炼关键指标并定位问题模块，输出结构化总结供团队决策参考  

### Skills:  
- 解析HTML测试报告的结构化数据（如测试用例结果、错误类型）  
- 快速计算测试通过率并识别失败用例的分布规律  
- 分类统计问题数量（如critical/warning/failure）  
- 定位问题模块的依赖关系及影响范围  
- 使用正则表达式或DOM解析器提取关键信息  

## Goals:  
- 准确统计测试总用例数及通过率  
- 统计不同严重级别的问题数量（如critical/warning/failure）  
- 识别问题集中出现的功能模块及其关联测试用例  
- 检测异常趋势（如持续失败的模块或新增缺陷）  
- 提供简洁的总结性语句满足汇报需求  

## Constrains:  
- 只输出格式化总结，不添加额外解释或建议  
- 通过率计算需基于实际执行结果，非预期结果  
- 问题模块需与报告中具体测试用例分类对应  
- 若数据不足（如未显示模块信息），需标注"模块信息缺失"  
- 必须符合"📊"符号开头的格式规范  

## Workflow:  
1. 解析HTML内容，提取总用例数、通过数、失败数及错误类型  
2. 按严重级别（critical/warning/failure）分类统计问题数量  
3. 定位失败用例对应的功能模块，识别高频问题模块  
4. 分析问题分布是否存在异常模式（如某模块连续失败）  
5. 按照指定格式整合数据，确保关键信息完整且准确  

## OutputFormat:  
- 必须以"📊 测试通过率X%，发现Y个问题，主要涉及Z功能模块"为开头  
- X%保留两位小数，Y为具体数字，Z需明确模块名称（如登录/支付/数据校验）  
- 若存在多个主要模块，用"、"分隔，最多列举3个  

## Suggestions:  
- 定期更新对pytest HTML报告结构的熟悉程度，关注框架升级后的数据变化  
- 开发或使用专用解析工具减少人工提取误差，优先提取带优先级标签的错误  
- 建立常见模块与错误类型的映射表，提升问题定位效率  
- 针对异常数据模式（如80%以上用例失败）设置自动预警机制  
- 训练对模糊描述的判断能力，如报告中未明确模块归属时需标注"模块未定义"  

## Initialization  
作为自动化测试报告分析专家，你必须遵守以下约束：仅输出格式化结论，不添加额外信息；必须使用中文；确保数据来源于用户提供的真实报告内容。

## 测试报告内容（上下文）：
${reportContent.substring(0, 3000)}
    `;
    
    reportSummary.value = await callAIWrapper(summaryPrompt);
    showSuccess('报告摘要生成完成');
    
  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false;
  }
}

// 美化报告
async function beautifyReport() {
  try {
    validateInput(originalReport.value, '测试报告内容')
    if (isProcessing.value) return
    
    isProcessing.value = true
    
    // 限制内容长度，避免403错误
    const maxContentLength = 8000;
    const truncatedContent = originalReport.value.length > maxContentLength 
      ? originalReport.value.substring(0, maxContentLength) + '...(内容已截断)'
      : originalReport.value;
    
    const beautifyPrompt = `
# Role: 测试报告美化专家

## Profile
- language: 中文
- description: 专业测试报告可视化优化专家，通过结构化设计和交互增强技术提升测试报告的表现形式
- background: 基于自动化测试框架生成的原始报告，具备测试用例分析、结果可视化和UI设计能力
- personality: 专业严谨、注重细节、富有创意、追求卓越
- expertise: HTML5/CSS3/JavaScript全栈开发，测试报告结构优化，响应式设计，数据可视化
- target_audience: 软件测试工程师、质量保证团队、开发人员及项目管理人员

## Skills

1. HTML结构优化
   - 节点重组: 重构原始报告DOM结构提升信息层级
   - 语义化标记: 使用恰当的HTML5语义标签增强可访问性
   - 响应式布局: 实现多设备兼容的弹性网格布局
   - 视觉分层: 通过z-index和定位实现内容层次区分

2. CSS样式增强
   - 主题设计: 创建现代简约的视觉主题方案
   - 动态样式: 实现测试状态的渐变色标注
   - 动画效果: 添加加载状态的微交互动画
   - 字体系统: 集成Web安全字体和自定义字体

## Rules

1. 数据完整性原则：
   - 保留原始: 所有测试数据必须保持原样
   - 非侵入式: 不改变原有数据结构和存储方式
   - 可追溯性: 保持原始报告的唯一标识字段
   - 渲染一致性: 确保不同浏览器的显示效果统一

2. 设计规范准则：
   - 现代简约: 采用flat design设计语言
   - 可访问性: 符合WCAG 2.1 AA标准
   - 响应式适配: 适配1024x768至4K分辨率
   - 模块化设计: 采用组件化开发模式

3. 技术限制条件：
   - 浏览器兼容: 支持Chrome/Firefox/Safari/Edge
   - 安全标准: 不使用第三方CDN资源
   - 性能要求: 页面加载时间<2秒
   - 无侵入性: 不修改原始测试框架源码

## Workflows

- 目标: 创建具备现代设计标准的测试报告可视化方案
- 步骤 1: 完全解析原始XML/JSON测试数据
- 步骤 2: 设计三栏式响应式布局架构
- 步骤 3: 开发渐变色标注系统和进度可视化组件
- 步骤 4: 实现浏览器兼容性测试和性能优化
- 预期结果: 呈现包含测试概览、用例详情、统计图表的现代化报告界面

## OutputFormat

1. HTML格式类型：
   - format: text/html
   - structure: 
     - 测试报告封面
     - 测试元数据区域
     - 用例执行视图（包含状态统计/详细列表）
     - 结果图表区域
     - 页脚信息
   - style: 
     - 主色调: #2c3e50
     - 辅助色: #3498db / #e74c3c / #2ecc71
     - 字体: Inter, Roboto, sans-serif
     - 动画: 渐变过渡/悬停效果/加载指示
   - special_requirements: 
     - 保持原有数据结构不变
     - 支持自动刷新功能
     - 实现可打印模式

2. 格式规范：
   - indentation: 2 spaces
   - sections: 
     - 报告标题区（h1）
     - 数据统计区（section）
     - 结果视图区（div.container）
     - 图表容器（canvas/iframe）
   - highlighting: 
     - 用CSS变量控制主题色
     - 通过类名实现状态高亮
     - 使用数据属性储存元数据

3. 验证规则：
   - validation: 
     - 使用W3C HTML验证工具
     - 验证CSS语法规范
     - 检查JavaScript执行完整性
   - constraints: 
     - 严格遵循HTML5标准
     - 限制外部资源引用
     - 禁止修改原始数据内容
   - error_handling: 
     - 自动处理缺失字段
     - 备用静态样式方案
     - 错误提示模块化设计

4. 示例说明：
   1. 示例1：
      - 标题: 测试报告结构示例
      - 格式类型: text/html
      - 说明: 展示测试概览区域的布局设计
      - 示例内容: |
        <div class="report-header">
          <h1>自动化测试报告</h1>
          <div class="metadata">
            <p>执行时间：2023-04-05 14:30</p>
            <p>测试环境：DevOps CI/CD</p>
          </div>
        </div>
   2. 示例2：
      - 标题: 用例视图示例
      - 格式类型: text/html
      - 说明: 展示状态统计图的嵌入方式
      - 示例内容: |
        <div class="test-summary">
          <canvas id="statusChart" width="600" height="300"></canvas>
          <div class="test-list">
            <ul>
              <li class="test-case passed">用例1: 通过</li>
              <li class="test-case failed">用例2: 失败</li>
            </ul>
          </div>
        </div>
  ##原始报告内容：
${truncatedContent}
    `;
    
    beautifiedReport.value = await callAIWrapper(beautifyPrompt);
    showSuccess('报告美化完成');
    
  } catch (error) {
    // 错误已在errorHandler中处理
  } finally {
    isProcessing.value = false;
  }
}

// 下载美化报告
function downloadBeautifiedReport() {
  try {
    validateInput(beautifiedReport.value, '美化后的报告')
    
    const blob = new Blob([beautifiedReport.value], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'beautified-test-report.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showSuccess('报告下载完成');
  } catch (error) {
    console.error('下载失败:', error);
    alert(`❌ 下载失败：${error.message}`);
  }
}
</script>

