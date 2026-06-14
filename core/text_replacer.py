"""
文字替换器 - 批量替换CAD文字
"""

import ezdxf
from typing import List, Optional

class TextReplacer:
    """文字替换工具"""
    
    def __init__(self, input_source):
        """初始化
        
        Args:
            input_source: 文件路径或DWGParser对象
        """
        if isinstance(input_source, str):
            self.doc = ezdxf.readfile(input_source)
        else:
            self.doc = input_source.doc
        
        self.msp = self.doc.modelspace()
    
    def replace_text(self, old_text: str, new_text: str, layer_name: Optional[str] = None) -> int:
        """替换文字
        
        Args:
            old_text: 要替换的文字
            new_text: 新文字
            layer_name: 限定图层（可选）
        
        Returns:
            替换次数
        """
        count = 0
        
        for entity in self.msp:
            # 检查是否是指定图层的实体
            if layer_name and entity.dxf.layer != layer_name:
                continue
            
            # 处理TEXT实体
            if entity.dxftype() == "TEXT":
                if old_text in entity.dxf.text:
                    entity.dxf.text = entity.dxf.text.replace(old_text, new_text)
                    count += 1
            
            # 处理MTEXT实体（多行文字）
            elif entity.dxftype() == "MTEXT":
                if old_text in entity.text:
                    entity.text = entity.text.replace(old_text, new_text)
                    count += 1
        
        return count
    
    def replace_text_in_blocks(self, old_text: str, new_text: str) -> int:
        """替换图块中的文字
        
        Args:
            old_text: 要替换的文字
            new_text: 新文字
        
        Returns:
            替换次数
        """
        count = 0
        
        for block in self.doc.blocks:
            for entity in block:
                if entity.dxftype() == "TEXT":
                    if old_text in entity.dxf.text:
                        entity.dxf.text = entity.dxf.text.replace(old_text, new_text)
                        count += 1
                elif entity.dxftype() == "MTEXT":
                    if old_text in entity.text:
                        entity.text = entity.text.replace(old_text, new_text)
                        count += 1
        
        return count
    
    def find_text(self, search_text: str, layer_name: Optional[str] = None) -> List[dict]:
        """查找包含指定文字的实体
        
        Args:
            search_text: 要查找的文字
            layer_name: 限定图层（可选）
        
        Returns:
            匹配的实体信息列表
        """
        results = []
        
        for entity in self.msp:
            if layer_name and entity.dxf.layer != layer_name:
                continue
            
            if entity.dxftype() == "TEXT":
                if search_text in entity.dxf.text:
                    results.append({
                        "type": "TEXT",
                        "text": entity.dxf.text,
                        "layer": entity.dxf.layer,
                        "position": entity.dxf.insert
                    })
            elif entity.dxftype() == "MTEXT":
                if search_text in entity.text:
                    results.append({
                        "type": "MTEXT",
                        "text": entity.text,
                        "layer": entity.dxf.layer,
                        "position": entity.dxf.insert
                    })
        
        return results
    
    def save(self, output_path: str):
        """保存文件"""
        self.doc.saveas(output_path)
