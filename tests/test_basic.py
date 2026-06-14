"""
测试用例
"""
import pytest
from pathlib import Path
import sys
import os

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.parser import DWGParser
from core.text_replacer import TextReplacer

def test_parser_init():
    """测试解析器初始化"""
    # 需要一个测试DXF文件
    pass

def test_text_replacer():
    """测试文字替换功能"""
    pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
