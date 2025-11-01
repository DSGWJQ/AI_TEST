"""
代码清理和验证工具模块
提供代码内容清理和中文字符比例验证功能
与前端保持一致的清理逻辑
"""

import re
from typing import Tuple


def clean_code_content(code: str) -> str:
    """
    清理代码内容，移除AI生成的无关内容和格式化问题
    与前端sanitize.js保持一致的清理逻辑
    
    Args:
        code (str): 原始代码字符串
        
    Returns:
        str: 清理后的代码字符串
    """
    if not code:
        return ""
    
    # 移除代码块标记（```html, ```python等）
    code = re.sub(r'^```\w*\s*\n?', '', code, flags=re.MULTILINE)
    # 修复未闭合的正则：删除任意位置的 ``` 及后续可选换行
    code = re.sub(r'```\n?', '', code)
    
    lines = code.split('\n')
    cleaned_lines = []
    
    # AI生成建议的模式
    ai_suggestion_patterns = [
        r'这段代码',
        r'以上代码',
        r'这个.*实现了',
        r'注意.*事项',
        r'建议.*使用',
        r'可以.*优化',
        r'推荐.*方式',
        r'另外.*可以',
        r'如果.*需要',
        r'当.*时候',
        r'为了.*安全',
        r'确保.*正确',
        r'避免.*问题'
    ]
    
    for line in lines:
        stripped_line = line.strip()
        
        # 跳过空行
        if not stripped_line:
            continue
        
        # 跳过AI生成的建议行（中文字符占比超过30%且包含建议模式）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', stripped_line))
        if chinese_chars > len(stripped_line) * 0.3:
            # 检查是否包含AI建议模式
            if any(re.search(pattern, stripped_line) for pattern in ai_suggestion_patterns):
                continue
        
        # 跳过纯中文注释行（中文字符占比超过60%的行）
        if chinese_chars > len(stripped_line) * 0.6 and not stripped_line.startswith('#'):
            continue
        
        # 移除不可见字符和问题字符（保留常用空白字符）
        # 移除控制字符
        cleaned_line = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', line)
        # 移除零宽字符和其他问题字符
        cleaned_line = re.sub(r'[\u200B-\u200D\uFEFF\u00A0\u2000-\u200A\u2028\u2029]', '', cleaned_line)
        # 移除可能导致编码问题的字符
        cleaned_line = re.sub(r'[\uFFFD\uFFFE\uFFFF]', '', cleaned_line)
        # 移除非打印字符（除了常见的空白字符）
        cleaned_line = re.sub(r'[^\x20-\x7E\u4e00-\u9fff\t\n\r]', '', cleaned_line)
        
        cleaned_lines.append(cleaned_line)
    
    # 合并行并移除多余的连续空行
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    # 移除首尾空白
    result = result.strip()
    
    return result


def validate_chinese_ratio(code: str, max_ratio: float = 0.1) -> Tuple[bool, float]:
    """
    验证代码中中文字符的比例
    
    Args:
        code (str): 代码字符串
        max_ratio (float): 允许的最大中文字符比例，默认0.1 (10%)
        
    Returns:
        Tuple[bool, float]: (是否通过验证, 实际中文字符比例)
    """
    if not code:
        return True, 0.0
    
    # 计算中文字符数量
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', code))
    total_chars = len(code)
    
    if total_chars == 0:
        return True, 0.0
    
    chinese_ratio = chinese_chars / total_chars
    is_valid = chinese_ratio <= max_ratio
    
    return is_valid, chinese_ratio


def sanitize_input(text: str) -> str:
    """
    净化输入文本，移除危险字符和控制字符
    与前端保持一致的净化逻辑
    
    Args:
        text (str): 输入文本
        
    Returns:
        str: 净化后的文本
    """
    if not text:
        return ""
    
    # 移除控制字符（除了换行符、制表符和回车符）
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # 限制长度，防止过长输入
    max_length = 50000  # 50KB
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def detect_code_language(code: str) -> str:
    """
    检测代码语言类型
    
    Args:
        code (str): 代码字符串
        
    Returns:
        str: 检测到的语言类型 ('python', 'javascript', 'unknown')
    """
    if not code:
        return 'unknown'
    
    # Python 特征
    python_patterns = [
        r'\bimport\s+\w+',
        r'\bfrom\s+\w+\s+import',
        r'\bdef\s+\w+\s*\(',
        r'\bclass\s+\w+\s*\(',
        r'\bif\s+__name__\s*==\s*["\']__main__["\']',
        r'\bprint\s*\(',
    ]
    
    # JavaScript 特征
    js_patterns = [
        r'\bfunction\s+\w+\s*\(',
        r'\bvar\s+\w+\s*=',
        r'\blet\s+\w+\s*=',
        r'\bconst\s+\w+\s*=',
        r'\bconsole\.log\s*\(',
        r'=>',
    ]
    
    python_score = sum(1 for pattern in python_patterns if re.search(pattern, code))
    js_score = sum(1 for pattern in js_patterns if re.search(pattern, code))
    
    if python_score > js_score:
        return 'python'
    elif js_score > 0:
        return 'javascript'
    else:
        # 修复错误的 return 语句
        return 'unknown'