/**
 * 前端代码清理工具函数
 * 用于在提交代码到 /run-code 前统一清理代码内容
 */

/**
 * 清理代码内容，删除不可见字符、三重反引号和尾部建议行
 * @param {string} code - 原始代码内容
 * @returns {string} - 清理后的代码内容
 */
export function sanitize(code) {
  if (!code || typeof code !== 'string') {
    return ''
  }

  let cleaned = code

  // 1. 删除不可见字符（保留常见的空白字符：空格、制表符、换行符）
  // 移除零宽字符、控制字符等不可见字符
  cleaned = cleaned.replace(/[\u200B-\u200D\uFEFF\u00A0\u2000-\u200A\u2028\u2029]/g, '')
  
  // 移除其他控制字符，但保留换行符(\n)、回车符(\r)、制表符(\t)
  cleaned = cleaned.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '')
  
  // 移除可能导致编码问题的字符
  cleaned = cleaned.replace(/[\uFFFD\uFFFE\uFFFF]/g, '')
  
  // 移除非打印字符（除了常见的空白字符和中文字符）
  cleaned = cleaned.replace(/[^\x20-\x7E\u4e00-\u9fff\t\n\r]/g, '')

  // 2. 删除代码块标记（三重反引号）
  cleaned = cleaned.replace(/```[a-zA-Z]*\n?/g, '')
  cleaned = cleaned.replace(/```\n?/g, '')

  // 3. 按行处理，删除尾部建议行和AI生成的解释行
  const lines = cleaned.split('\n')
  const cleanedLines = []
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const trimmedLine = line.trim()
    
    // 跳过空行（但保留用于代码结构的空行）
    if (trimmedLine === '') {
      cleanedLines.push(line)
      continue
    }
    
    // 检查是否是AI生成的建议行或解释行
    const chineseCount = (trimmedLine.match(/[\u4e00-\u9fff]/g) || []).length
    const isChineseExplanation = (
      chineseCount > trimmedLine.length * 0.3 &&  // 中文字符超过30%
      !trimmedLine.includes('"') &&  // 不在字符串中
      !trimmedLine.includes("'") &&  // 不在字符串中
      !trimmedLine.startsWith('#')   // 不是注释
    )
    
    // 检查是否是常见的AI建议模式
    const isAISuggestion = (
      trimmedLine.includes('建议') ||
      trimmedLine.includes('推荐') ||
      trimmedLine.includes('可以') ||
      trimmedLine.includes('应该') ||
      trimmedLine.includes('注意') ||
      trimmedLine.includes('提示') ||
      trimmedLine.match(/^(这里|这段|上面|下面|以上|以下)/) ||
      trimmedLine.match(/^(另外|此外|同时|最后|总之)/)
    )
    
    // 如果不是中文解释行或AI建议行，保留该行
    if (!isChineseExplanation && !isAISuggestion) {
      cleanedLines.push(line)
    }
  }
  
  // 4. 移除尾部多余的空行
  while (cleanedLines.length > 0 && cleanedLines[cleanedLines.length - 1].trim() === '') {
    cleanedLines.pop()
  }
  
  return cleanedLines.join('\n')
}

/**
 * 检测代码语言类型
 * @param {string} code - 代码内容
 * @returns {string} - 语言类型 ('python', 'javascript', 'java', 'unknown')
 */
export function detectCodeLanguage(code) {
  if (!code) return 'unknown'
  
  const lowerCode = code.toLowerCase()
  
  // Python 特征
  if (lowerCode.includes('import ') || 
      lowerCode.includes('def ') || 
      lowerCode.includes('print(') ||
      lowerCode.includes('if __name__')) {
    return 'python'
  }
  
  // JavaScript 特征
  if (lowerCode.includes('function ') || 
      lowerCode.includes('const ') || 
      lowerCode.includes('let ') ||
      lowerCode.includes('console.log')) {
    return 'javascript'
  }
  
  // Java 特征
  if (lowerCode.includes('public class') || 
      lowerCode.includes('public static void main') ||
      lowerCode.includes('system.out.println')) {
    return 'java'
  }
  
  return 'unknown'
}

/**
 * 验证代码内容的有效性
 * @param {string} code - 代码内容
 * @returns {object} - 验证结果 {isValid: boolean, message: string}
 */
export function validateCode(code) {
  if (!code || typeof code !== 'string') {
    return { isValid: false, message: '代码内容不能为空' }
  }
  
  const trimmedCode = code.trim()
  if (trimmedCode.length === 0) {
    return { isValid: false, message: '代码内容不能为空' }
  }
  
  // 检查是否只包含中文字符（可能是纯解释文本）
  const chineseCount = (trimmedCode.match(/[\u4e00-\u9fff]/g) || []).length
  if (chineseCount > trimmedCode.length * 0.8) {
    return { isValid: false, message: '代码内容主要为中文文本，请提供有效的代码' }
  }
  
  return { isValid: true, message: '代码内容有效' }
}