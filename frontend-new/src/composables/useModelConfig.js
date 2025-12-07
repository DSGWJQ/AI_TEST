import { ref, computed } from "vue"

// 默认模型列表
const defaultOnlineModels = [
  "meta-llama/llama-3.3-70b-instruct:free",
  "deepseek/deepseek-r1:free",
  "google/gemini-flash-1.5:free",
  "microsoft/wizardlm-2-8x22b:free",
]

export const OLLAMA_URL = import.meta.env.VITE_OLLAMA_URL || "http://localhost:11434/v1"

export function useModelConfig() {
  // 从环境变量获取配置
  const OPENROUTER_API_KEY = import.meta.env.VITE_OPENROUTER_API_KEY || ""

  // 状态
  const modelSource = ref("online")
  const selectedModel = ref("deepseek/deepseek-r1:free")
  const isRefreshing = ref(false)
  const modelStatus = ref("点击刷新按钮获取最新模型列表")
  const apiKey = ref(OPENROUTER_API_KEY)
  const showApiKeyInput = ref(!OPENROUTER_API_KEY)
  const onlineModels = ref([...defaultOnlineModels])
  const localModels = ref([])

  // 计算属性
  const availableModels = computed(() => (modelSource.value === "online" ? onlineModels.value : localModels.value))

  const modelStatusClass = computed(() => {
    if (
      modelStatus.value.includes("成功") ||
      modelStatus.value.includes("可用") ||
      modelStatus.value.includes("发现")
    ) {
      return "bg-green-50 text-green-700 border border-green-200"
    } else if (
      modelStatus.value.includes("失败") ||
      modelStatus.value.includes("错误") ||
      modelStatus.value.includes("未启动")
    ) {
      return "bg-red-50 text-red-700 border border-red-200"
    } else if (modelStatus.value.includes("刷新中")) {
      return "bg-blue-50 text-blue-700 border border-blue-200"
    }
    return "bg-yellow-50 text-yellow-700 border border-yellow-200"
  })

  // 刷新在线模型列表
  async function refreshOnlineModels() {
    try {
      const currentApiKey = apiKey.value
      if (!currentApiKey) {
        throw new Error("请先设置 API Key")
      }

      const response = await fetch("https://openrouter.ai/api/v1/models", {
        headers: {
          Authorization: `Bearer ${currentApiKey}`,
          "Content-Type": "application/json",
        },
      })

      if (response.ok) {
        const data = await response.json()
        const freeModels = data.data
          ?.filter((model) => model.pricing?.prompt === "0" || model.id.includes(":free"))
          ?.map((model) => model.id)
          ?.slice(0, 10)

        if (freeModels && freeModels.length > 0) {
          onlineModels.value = [...new Set([...freeModels, ...defaultOnlineModels])]
          modelStatus.value = `成功获取 ${freeModels.length} 个在线模型`
        } else {
          throw new Error("未找到可用的免费模型")
        }
      } else {
        throw new Error(`API响应错误: ${response.status}`)
      }
    } catch (error) {
      onlineModels.value = [...defaultOnlineModels]
      modelStatus.value = `使用默认在线模型列表 (${error.message})`
    }
  }

  // 刷新本地模型列表
  async function refreshLocalModels() {
    try {
      const response = await fetch(`${OLLAMA_URL.replace("/v1", "")}/api/tags`)

      if (response.ok) {
        const data = await response.json()
        const installedModels = data.models?.map((model) => model.name) || []

        if (installedModels.length > 0) {
          localModels.value = installedModels
          modelStatus.value = `发现 ${installedModels.length} 个已安装的本地模型`
        } else {
          localModels.value = []
          modelStatus.value = '未发现已安装的模型，请先使用 "ollama pull <模型名>" 下载模型'
        }
      } else {
        throw new Error("无法连接到Ollama服务 (http://localhost:11434)")
      }
    } catch (error) {
      localModels.value = []
      if (error.message.includes("Failed to fetch")) {
        modelStatus.value = "Ollama服务未启动，请先启动Ollama服务"
      } else {
        modelStatus.value = `连接失败: ${error.message}`
      }
    }
  }

  // 刷新模型列表
  async function refreshModels() {
    if (isRefreshing.value) return

    isRefreshing.value = true
    modelStatus.value = "正在刷新模型列表..."

    try {
      if (modelSource.value === "online") {
        await refreshOnlineModels()
      } else {
        await refreshLocalModels()
      }
    } catch (error) {
      console.error("刷新模型列表失败:", error)
      modelStatus.value = `刷新失败: ${error.message}`
    } finally {
      isRefreshing.value = false
    }
  }

  return {
    // 状态
    modelSource,
    selectedModel,
    isRefreshing,
    modelStatus,
    apiKey,
    showApiKeyInput,
    onlineModels,
    localModels,
    // 计算属性
    availableModels,
    modelStatusClass,
    // 方法
    refreshModels,
  }
}
