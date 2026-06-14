"""
简化版 DXF 解析器 - 无 numpy 依赖
仅支持基础 DXF R12 格式（文本格式）
"""
import re
from typing import List, Dict, Tuple, Optional

class SimpleDXFParser:
    """简化版 DXF 解析器
    
    支持：
    - 读取 DXF R12 文本格式
    - 提取图层信息
    - 提取文字实体
    - 保存修改
    """
    
    def __init__(self, file_path: str):
        """初始化
        
        Args:
            file_path: DXF 文件路径
        """
        self.file_path = file_path
        self.entities = []
        self.layers = set()
        self.text_entities = []
        self.raw_content = []
        
    def read(self):
        """读取 DXF 文件"""
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.raw_content = f.readlines()
        
        # 解析实体
        self._parse_entities()
        
        return self
    
    def _parse_entities(self):
        """解析 DXF 实体"""
        i = 0
        while i < len(self.raw_content):
            line = self.raw_content[i].strip()
            
            # 检测实体开始
            if line == '0' and i + 1 < len(self.raw_content):
                entity_type = self.raw_content[i + 1].strip()
                
                if entity_type == 'TEXT':
                    # 解析 TEXT 实体
                    text_entity = self._parse_text_entity(i)
                    if text_entity:
                        self.entities.append(text_entity)
                        self.text_entities.append(text_entity)
                elif entity_type == 'LAYER':
                    # 解析 LAYER 实体
                    layer_name = self._parse_layer_name(i)
                    if layer_name:
                        self.layers.add(layer_name)
            
            i += 1
    
    def _parse_text_entity(self, start_idx: int) -> Optional[Dict]:
        """解析 TEXT 实体
        
        Args:
            start_idx: 实体起始索引
        
        Returns:
            文字实体信息
        """
        entity = {
            'type': 'TEXT',
            'text': '',
            'layer': '0',
            'position': (0, 0),
            'start_idx': start_idx
        }
        
        i = start_idx + 2  # 跳过 "0" 和 "TEXT"
        while i < len(self.raw_content):
            group_code = self.raw_content[i].strip()
            value = self.raw_content[i + 1].strip() if i + 1 < len(self.raw_content) else ''
            
            if group_code == '1':  # 文字内容
                entity['text'] = value
            elif group_code == '8':  # 图层
                entity['layer'] = value
            elif group_code == '10':  # X 坐标
                x = float(value) if value else 0
                y = 0
                if i + 3 < len(self.raw_content) and self.raw_content[i + 2].strip() == '20':
                    y = float(self.raw_content[i + 3].strip()) if self.raw_content[i + 3].strip() else 0
                entity['position'] = (x, y)
                i += 2  # 跳过 Y 坐标
            
            # 遇到下一个实体或文件结束
            if group_code == '0':
                break
            
            i += 2
        
        return entity if entity['text'] else None
    
    def _parse_layer_name(self, start_idx: int) -> Optional[str]:
        """解析图层名称
        
        Args:
            start_idx: 实体起始索引
        
        Returns:
            图层名称
        """
        i = start_idx + 2  # 跳过 "0" 和 "LAYER"
        while i < len(self.raw_content):
            group_code = self.raw_content[i].strip()
            value = self.raw_content[i + 1].strip() if i + 1 < len(self.raw_content) else ''
            
            if group_code == '2':  # 图层名称
                return value
            
            i += 2
        
        return None
    
    def get_file_info(self) -> Dict:
        """获取文件信息
        
        Returns:
            文件信息字典
        """
        return {
            'version': 'DXF R12 (simplified parser)',
            'layers_count': len(self.layers),
            'entities_count': len(self.entities),
            'text_entities_count': len(self.text_entities)
        }
    
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
        
        for entity in self.text_entities:
            # 检查图层
            if layer_name and entity['layer'] != layer_name:
                continue
            
            # 替换文字
            if old_text in entity['text']:
                old_full_text = entity['text']
                entity['text'] = entity['text'].replace(old_text, new_text)
                
                # 更新 raw_content
                idx = entity['start_idx']
                while idx < len(self.raw_content):
                    if self.raw_content[idx].strip() == '1':  # 文字内容组码
                        self.raw_content[idx + 1] = entity['text'] + '\n'
                        break
                    idx += 1
                
                count += 1
        
        return count
    
    def save(self, output_path: str):
        """保存文件
        
        Args:
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(self.raw_content)
