"""
DWG/DXF文件解析器
依赖: ezdxf (纯Python, 支持DXF)
       LibreDWG (可选, 用于DWG转换)
"""

import ezdxf
from pathlib import Path
from typing import Dict, List, Any

class DWGParser:
    """CAD文件解析器 - 支持DXF格式"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.doc = None
        self._load_file()
    
    def _load_file(self):
        """加载CAD文件"""
        if self.file_path.suffix.lower() == ".dxf":
            self.doc = ezdxf.readfile(str(self.file_path))
        elif self.file_path.suffix.lower() == ".dwg":
            # DWG需要先用LibreDWG转换
            raise NotImplementedError(
                "DWG格式需要LibreDWG转换，请先转换为DXF格式\n"
                "转换命令: dwg2dxf input.dwg -o output.dxf"
            )
        else:
            raise ValueError(f"不支持的文件格式: {self.file_path.suffix}")
    
    def get_file_info(self) -> Dict[str, Any]:
        """获取文件基本信息"""
        if not self.doc:
            return {}
        
        msp = self.doc.modelspace()
        
        info = {
            "version": self.doc.dxfversion,
            "encoding": self.doc.encoding,
            "layers_count": len(self.doc.layers),
            "blocks_count": len(self.doc.blocks),
            "entities_count": len(list(msp)),
            "units": self._get_units()
        }
        
        return info
    
    def _get_units(self) -> str:
        """获取绘图单位"""
        units_map = {
            0: "无单位",
            1: "英寸", 
            2: "英尺",
            3: "英里",
            4: "毫米",
            5: "厘米",
            6: "米"
        }
        try:
            unit_code = self.doc.header.get("$INSUNITS", 0)
            return units_map.get(unit_code, "未知")
        except:
            return "未知"
    
    def get_layers(self) -> List[Dict[str, Any]]:
        """获取所有图层信息"""
        layers = []
        for layer in self.doc.layers:
            layers.append({
                "name": layer.dxf.name,
                "color": layer.dxf.color,
                "is_on": layer.is_on(),
                "is_frozen": layer.is_frozen()
            })
        return layers
    
    def get_blocks(self) -> List[str]:
        """获取所有图块名称"""
        return [block.name for block in self.doc.blocks]
    
    def save(self, output_path: str):
        """保存文件"""
        self.doc.saveas(output_path)
