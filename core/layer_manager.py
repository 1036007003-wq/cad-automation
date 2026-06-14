"""
图层管理器 - 冻结/解冻图层
"""

import ezdxf
from typing import List, Optional

class LayerManager:
    """图层管理工具"""
    
    def __init__(self, input_source):
        """初始化
        
        Args:
            input_source: 文件路径或DWGParser对象
        """
        if isinstance(input_source, str):
            self.doc = ezdxf.readfile(input_source)
        else:
            self.doc = input_source.doc
    
    def freeze_layer(self, layer_name: str):
        """冻结图层"""
        try:
            layer = self.doc.layers.get(layer_name)
            layer.freeze()
        except KeyError:
            print(f"⚠️ 图层不存在: {layer_name}")
    
    def thaw_layer(self, layer_name: str):
        """解冻图层"""
        try:
            layer = self.doc.layers.get(layer_name)
            layer.thaw()
        except KeyError:
            print(f"⚠️ 图层不存在: {layer_name}")
    
    def turn_off_layer(self, layer_name: str):
        """关闭图层（不显示）"""
        try:
            layer = self.doc.layers.get(layer_name)
            layer.off()
        except KeyError:
            print(f"⚠️ 图层不存在: {layer_name}")
    
    def turn_on_layer(self, layer_name: str):
        """打开图层（显示）"""
        try:
            layer = self.doc.layers.get(layer_name)
            layer.on()
        except KeyError:
            print(f"⚠️ 图层不存在: {layer_name}")
    
    def list_layers(self) -> List[dict]:
        """列出所有图层及其状态"""
        layers_info = []
        for layer in self.doc.layers:
            layers_info.append({
                "name": layer.dxf.name,
                "color": layer.dxf.color,
                "is_on": layer.is_on(),
                "is_frozen": layer.is_frozen()
            })
        return layers_info
    
    def save(self, output_path: str):
        """保存文件"""
        self.doc.saveas(output_path)
