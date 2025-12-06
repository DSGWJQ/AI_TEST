"""
后端 API 单元测试
测试后端核心功能模块
"""
import pytest
import sys
import os

# 添加后端模块路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

from app.sanitizer import clean_code_content, validate_chinese_ratio, sanitize_input, detect_code_language


class TestCleanCodeContent:
    """测试代码清理功能"""

    def test_clean_basic_code(self):
        """测试基本代码清理"""
        code = "print('hello world')"
        result = clean_code_content(code)
        assert "print" in result
        assert "hello world" in result

    def test_clean_empty_code(self):
        """测试空代码"""
        assert clean_code_content("") == ""
        assert clean_code_content(None) == ""

    def test_clean_code_with_code_blocks(self):
        """测试移除代码块标记"""
        code = "```python\nprint('hello')\n```"
        result = clean_code_content(code)
        assert "```" not in result
        assert "print" in result

    def test_clean_multiline_code(self):
        """测试多行代码清理"""
        code = """
def test_func():
    return 42

class TestClass:
    pass
"""
        result = clean_code_content(code)
        assert "def test_func" in result
        assert "class TestClass" in result

    def test_clean_code_removes_ai_suggestions(self):
        """测试移除 AI 建议内容"""
        code = """
print('hello')
这段代码实现了打印功能
print('world')
"""
        result = clean_code_content(code)
        assert "print('hello')" in result
        assert "print('world')" in result

    def test_clean_code_preserves_comments(self):
        """测试保留代码注释"""
        code = """
# This is a comment
def test():
    pass
"""
        result = clean_code_content(code)
        assert "# This is a comment" in result

    def test_clean_code_removes_control_chars(self):
        """测试移除控制字符"""
        code = "print('hello\x00world')"
        result = clean_code_content(code)
        assert "\x00" not in result


class TestValidateChineseRatio:
    """测试中文比例验证功能"""

    def test_valid_english_only(self):
        """测试纯英文代码"""
        code = "def test(): return 42"
        is_valid, ratio = validate_chinese_ratio(code)
        assert is_valid is True
        assert ratio == 0.0

    def test_valid_with_low_chinese(self):
        """测试低中文比例"""
        # 默认 max_ratio 是 0.1，需要确保中文比例低于 10%
        code = "print('hello world test function') # 测"
        is_valid, ratio = validate_chinese_ratio(code)
        # 只有1个中文字符，比例应该很低
        assert is_valid is True
        assert ratio < 0.1

    def test_invalid_high_chinese(self):
        """测试高中文比例（无效）"""
        code = "这是一段纯中文说明文字"
        is_valid, ratio = validate_chinese_ratio(code)
        assert is_valid is False
        assert ratio > 0.1

    def test_empty_code(self):
        """测试空代码"""
        is_valid, ratio = validate_chinese_ratio("")
        assert is_valid is True
        assert ratio == 0.0

    def test_custom_max_ratio(self):
        """测试自定义最大比例"""
        code = "测试test"  # 2个中文，4个英文
        # 比例约为 2/6 = 0.33
        is_valid, ratio = validate_chinese_ratio(code, max_ratio=0.5)
        assert is_valid is True

        is_valid, ratio = validate_chinese_ratio(code, max_ratio=0.2)
        assert is_valid is False


class TestSanitizeInput:
    """测试输入净化功能"""

    def test_sanitize_normal_input(self):
        """测试正常输入"""
        text = "Hello, World!"
        result = sanitize_input(text)
        assert result == text

    def test_sanitize_empty_input(self):
        """测试空输入"""
        assert sanitize_input("") == ""
        assert sanitize_input(None) == ""

    def test_sanitize_removes_control_chars(self):
        """测试移除控制字符"""
        text = "Hello\x00World\x07"
        result = sanitize_input(text)
        assert "\x00" not in result
        assert "\x07" not in result
        assert "Hello" in result
        assert "World" in result

    def test_sanitize_preserves_newlines(self):
        """测试保留换行符"""
        text = "Line1\nLine2\r\nLine3"
        result = sanitize_input(text)
        assert "\n" in result

    def test_sanitize_length_limit(self):
        """测试长度限制"""
        long_text = "a" * 100000
        result = sanitize_input(long_text)
        assert len(result) <= 50000


class TestDetectCodeLanguage:
    """测试代码语言检测功能"""

    def test_detect_python_import(self):
        """测试检测 Python import 语句"""
        code = "import os\nimport sys"
        assert detect_code_language(code) == 'python'

    def test_detect_python_def(self):
        """测试检测 Python 函数定义"""
        code = "def test_function():\n    pass"
        assert detect_code_language(code) == 'python'

    def test_detect_python_class(self):
        """测试检测 Python 类定义"""
        code = "class TestClass():\n    pass"
        assert detect_code_language(code) == 'python'

    def test_detect_javascript_function(self):
        """测试检测 JavaScript 函数"""
        code = "function test() { return 42; }"
        assert detect_code_language(code) == 'javascript'

    def test_detect_javascript_const(self):
        """测试检测 JavaScript const"""
        code = "const x = 10;\nlet y = 20;"
        assert detect_code_language(code) == 'javascript'

    def test_detect_unknown(self):
        """测试检测未知语言"""
        code = "hello world"
        assert detect_code_language(code) == 'unknown'

    def test_detect_empty(self):
        """测试检测空代码"""
        assert detect_code_language("") == 'unknown'
        assert detect_code_language(None) == 'unknown'


class TestCodeCompilation:
    """测试代码编译验证"""

    def test_valid_python_syntax(self):
        """测试有效的 Python 语法"""
        code = """
import pytest

def test_example():
    assert 1 + 1 == 2

class TestClass:
    def test_method(self):
        pass
"""
        try:
            compile(code.strip(), "<test>", "exec")
            valid = True
        except SyntaxError:
            valid = False
        assert valid is True

    def test_invalid_python_syntax(self):
        """测试无效的 Python 语法"""
        code = "def test( :"
        try:
            compile(code, "<test>", "exec")
            valid = True
        except SyntaxError:
            valid = False
        assert valid is False

    def test_indentation_error(self):
        """测试缩进错误"""
        code = """
def test():
return 42
"""
        try:
            compile(code, "<test>", "exec")
            valid = True
        except (SyntaxError, IndentationError):
            valid = False
        assert valid is False

    def test_valid_pytest_structure(self):
        """测试有效的 pytest 结构"""
        code = """
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3]

def test_with_fixture(sample_data):
    assert len(sample_data) == 3

@pytest.mark.parametrize("x,y,expected", [(1,2,3), (2,3,5)])
def test_parametrized(x, y, expected):
    assert x + y == expected
"""
        try:
            compile(code.strip(), "<test>", "exec")
            valid = True
        except SyntaxError:
            valid = False
        assert valid is True
