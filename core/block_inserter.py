"""
图块插入器 - 用于加盖竣工章
"""

import ezdxf
from pathlib import Path
from typing import Tuple, Optional

class BlockInserter:
    """图块插入工具"""
    
    def __init__(self, input_source):
        """初始化
        
        Args:
            input_source: 可以是文件路径字符串或DWGParser对象
        """
        if isinstance(input_source, str):
            self.doc = ezdxf.readfile(input_source)
        else:
            # 假设是DWGParser对象
            self.doc = input_source.doc
        
        self.msp = self.doc.modelspace()
    
    def add_default_stamp(self, position: Tuple[float, float] = (100, 100)):
        """添加默认竣工章
        
        创建一个简单的竣工章图块
        """
        # 创建竣工章图块
        if "COMPLETION_STAMP" not in self.doc.blocks:
            block = self.doc.blocks.new(name="COMPLETION_STAMP")
            
            # 绘制竣工章（简单矩形 + 文字）
            # 外框
            block.add_lwpolyline([
                (0, 0), (50, 0), (50, 30), (0, 30), (0, 0)
            ], dxfattribs={"color": 1})
            
            # 文字
            block.add_text(
                "竣 工 图", 
                dxfattribs={"height": 5, "color": 1, "insert": (10, 22)}
            )
            block.add_text(
                "审查合格", 
                dxfattribs={"height": 3, "color": 3, "insert": (10, 15)}
            )
        
        # 插入图块
        self.msp.add_blockref(
            "COMPLETION_STAMP", 
            insertion_point=position,
            dxfattribs={"color": 1}
        )
        
        return self
    
    def insert_stamp(self, stamp_file: str, position: Tuple[float, float] = (100, 100)):
        """插入自定义竣工章
        
        Args:
            stamp_file: 竣工章DXF文件路径
            position: 插入位置 (x, y)
        """
        # 读取竣工章文件
        stamp_doc = ezdxf.readfile(stamp_file)
        
        # 复制图块定义
        for block in stamp_doc.blocks:
            if block.name not in self.doc.blocks:
                new_block = self.doc.blocks.new(name=block.name)
                for entity in block:
                    new_block.add_duplicate_entity(entity)
        
        # 插入图块（假设第一个图块是竣工章）
        stamp_block_name = list(stamp_doc.blocks)[0].name
        
        self.msp.add_blockref(
            stamp_block_name,
            insertion_point=position,
            dxfattribs={"color": 1}
        )
        
        return self
    
    def save(self, output_path: str):
        """保存文件"""
        self.doc.saveas(output_path)
