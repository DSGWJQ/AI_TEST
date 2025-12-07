// 统一的错误处理工具
import api from '../api'

// 统一的错误处理函数
export function handleAIError(error) {
  console.error('AI调用失败:', error)
  
  // 根据HTTP状态码提供详细错误信息
  if (error.response?.status) {
    const status = error.response.status
    const statusMessages = {
      400: '请求参数错误，请检查输入内容格式是否正确',
      401: 'API Key无效或已过期，请检查认证信息',
      403: 'API Key权限不足或余额不足，请检查账户状态或更换模型',
      404: '请求的模型或服务不存在，请检查模型名称',
      429: '请求频率过高，请稍后重试（建议等待1-2分钟）',
      500: '服务器内部错误，请稍后重试或联系技术支持',
      502: '网关错误，服务暂时不可用，请稍后重试',
      503: '服务暂时不可用，请稍后重试',
      504: '请求超时，请检查网络连接或稍后重试'
    }
    
    const message = statusMessages[status] || `服务器返回错误 ${status}，请稍后重试`
    const errorMsg = `❌ ${message}`
    
    // 同时输出到控制台和弹窗
    console.error(`HTTP ${status}:`, message)
    alert(errorMsg)
    throw new Error(errorMsg)
  }
  
  // 网络连接错误
  if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
    const message = '⏱️ 请求超时，请检查网络连接或稍后重试'
    console.error('网络超时:', error)
    alert(message)
    throw new Error(message)
  }
  
  // 网络连接失败
  if (error.code === 'NETWORK_ERROR' || !navigator.onLine) {
    const message = '🌐 网络连接失败，请检查网络设置'
    console.error('网络错误:', error)
    alert(message)
    throw new Error(message)
  }
  
  // 本地Ollama连接错误
  if (error.message?.includes('fetch')) {
    const message = '🔌 无法连接到本地Ollama服务，请确认服务已启动'
    console.error('Ollama连接错误:', error)
    alert(message)
    throw new Error(message)
  }
  
  // 其他未知错误
  const message = `⚠️ 未知错误：${error.message || '请重试或联系技术支持'}`
  console.error('未知错误:', error)
  alert(message)
  throw new Error(message)
}

// 统一的AI调用函数
export async function callAI(prompt, modelSource, selectedModel, apiKey, ollamaUrl) {
  try {
    if (modelSource === 'online') {
      const { data } = await api.post('/ai/chat', {
        model: selectedModel,
        messages: [{ role: 'user', content: prompt }],
        api_key: apiKey
      })
      
      if (data?.content) return data.content
      throw new Error(data?.error || '在线服务响应异常')
      
    } else {
      // 本地模式（Ollama）
      const OpenAI = (await import('openai')).default
      const client = new OpenAI({
        baseURL: ollamaUrl,
        apiKey: 'ollama',
        dangerouslyAllowBrowser: true
      })
      
      const completion = await client.chat.completions.create({
        model: selectedModel,
        messages: [{ role: 'user', content: prompt }]
      })
      
      return completion.choices?.[0]?.message?.content || ''
    }
  } catch (error) {
    handleAIError(error)
  }
}

// 输入验证函数
export function validateInput(input, fieldName = '输入内容') {
  if (!input || !input.trim()) {
    const message = `📝 请输入${fieldName}`
    alert(message)
    throw new Error(message)
  }
  return input.trim()
}

// 成功提示函数
export function showSuccess(message) {
  console.log('✅ 操作成功:', message)
  // 使用 setTimeout 确保弹窗不被阻塞
  setTimeout(() => {
    try {
      alert(`✅ ${message}`)
    } catch (error) {
      console.error('弹窗显示失败:', error)
    }
  }, 100)
}

// 新增：显示错误弹窗
export function showError(message) {
  console.error('❌ 操作失败:', message)
  setTimeout(() => {
    try {
      alert(`❌ ${message}`)
    } catch (error) {
      console.error('错误弹窗显示失败:', error)
    }
  }, 100)
}