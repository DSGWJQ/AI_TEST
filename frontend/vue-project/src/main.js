import { createApp } from 'vue'
import './index.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
// 全局错误兜底，避免白屏
app.config.errorHandler = (err) => {
  console.error(err)
  alert(`页面错误：${err?.message || err}`)
}
app.use(router).mount('#app')
