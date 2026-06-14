"""CAD自动化工具核心模块"""
import sys

# 尝试导入完整版解析器（依赖 ezdxf + numpy）
# 如果失败，使用简化版解析器（无依赖）
try:
    from .parser import DWGParser
    USE_FULL_PARSER = True
except ImportError:
    # ezdxf/numpy 不可用，使用简化版
    from .simple_parser import SimpleDXFParser as DWGParser
    USE_FULL_PARSER = False

# 条件导入其他模块
try:
    from .block_inserter import BlockInserter
    from .layer_manager import LayerManager
    from .text_replacer import TextReplacer
except ImportError:
    # 如果其他模块也依赖 ezdxf，可以这里添加简化版
    pass

__all__ = [
    "DWGParser",
    "BlockInserter", 
    "LayerManager",
    "TextReplacer"
]

# 导出简化版解析器（如果使用的是简化版）
if not USE_FULL_PARSER:
    from .simple_parser import SimpleDXFParser
    __all__.append("SimpleDXFParser")
