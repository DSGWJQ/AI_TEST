import axios from 'axios'
import { store } from '../store'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000, // 从5000ms增加到30000ms
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 自动添加 token
api.interceptors.request.use(
  config => {
    if (store.token) {
      config.headers.Authorization = `Bearer ${store.token}`
    }
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
    if (error.response?.status === 401) {
      // token 过期，自动登出
      store.logout()
      window.location.href = '/login'
    }
    
    // 处理超时错误，提供友好提示
    if (error.code === 'ECONNABORTED' && error.message.includes('timeout')) {
      console.error('请求超时:', error.message)
      // 可以在这里添加全局提示组件
      alert('AI服务响应超时，请稍后重试或检查网络/服务状态')
    }
    
    return Promise.reject(error)
  }
)

// API 方法
export const authAPI = {
  // 登录
  login: (username, password) => {
    return api.post('/login', { username, password })
  },
  
  // 注册
  register: (username, password) => {
    return api.post('/register', { username, password })
  }
}

// 新增：接口自动化测试执行 API
export const testAPI = {
  runCode: (code, runner = 'python', timeout = 60) => {
    return api.post('/run-code', { code, runner, timeout }, {
      timeout: 90000  // 前端超时时间设为90秒，给后端足够时间
    })
  }
}

export default api