import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误和超时
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 处理超时错误，提供友好提示
    if (error.code === 'ECONNABORTED' && error.message.includes('timeout')) {
      console.error('请求超时:', error.message)
      alert('AI服务响应超时，请稍后重试或检查网络/服务状态')
    }

    return Promise.reject(error)
  }
)

// 接口自动化测试执行 API
export const testAPI = {
  runCode: (code, runner = 'python', timeout = 60) => {
    return api.post('/run-code', { code, runner, timeout }, {
      timeout: 90000  // 前端超时时间设为90秒，给后端足够时间
    })
  }
}

export default api
