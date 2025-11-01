import { reactive } from 'vue'

// 创建全局状态
export const store = reactive({
  // 用户登录状态
  isLoggedIn: false,
  // 用户信息
  user: {
    username: '',
    userId: null
  },
  // 存储 token
  token: null,
  
  // 登录方法
  login(username, userId, token) {
    // 验证参数
    if (!username || !userId || !token) {
      console.error('登录参数不完整:', { username, userId, token })
      return false
    }
    
    this.isLoggedIn = true
    this.user.username = username
    this.user.userId = userId
    this.token = token
    
    // 保存到localStorage
    try {
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('username', username)
      localStorage.setItem('userId', userId.toString())
      localStorage.setItem('token', token)
      console.log('用户信息已保存到localStorage:', { username, userId })
    } catch (error) {
      console.error('保存用户信息到localStorage失败:', error)
    }
    
    return true
  },
  
  // 登出方法
  logout() {
    this.isLoggedIn = false
    this.user.username = ''
    this.user.userId = null
    this.token = null
    
    // 清除localStorage
    try {
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('username')
      localStorage.removeItem('userId')
      localStorage.removeItem('token')
      console.log('用户信息已从localStorage清除')
    } catch (error) {
      console.error('清除localStorage失败:', error)
    }
  },
  
  // 初始化状态（从localStorage恢复）
  init() {
    try {
      const isLoggedIn = localStorage.getItem('isLoggedIn')
      const username = localStorage.getItem('username')
      const userId = localStorage.getItem('userId')
      const token = localStorage.getItem('token')
      
      console.log('从localStorage读取用户信息:', { isLoggedIn, username, userId, token: token ? '***' : null })
      
      if (isLoggedIn === 'true' && username && userId && token) {
        this.isLoggedIn = true
        this.user.username = username
        this.user.userId = parseInt(userId) || null
        this.token = token
        console.log('用户状态已恢复:', { username, userId: this.user.userId })
      } else {
        console.log('localStorage中无有效用户信息，保持未登录状态')
        // 确保清理不完整的数据
        this.logout()
      }
    } catch (error) {
      console.error('初始化用户状态失败:', error)
      // 发生错误时清理状态
      this.logout()
    }
  }
})