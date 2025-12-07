import { reactive } from 'vue'

// 创建全局状态（已移除登录认证功能）
export const store = reactive({
  // 应用设置
  settings: {
    theme: 'light'
  }
})
