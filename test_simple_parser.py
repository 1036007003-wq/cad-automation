#!/usr/bin/env python3
"""
测试简化版 DXF 解析器
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core.simple_parser import SimpleDXFParser

def test_parse_dxf():
    """测试解析 DXF 文件"""
    print("=" * 60)
    print("  测试简化版 DXF 解析器")
    print("=" * 60)
    print()
    
    # 读取测试文件
    test_file = Path(__file__).parent / "test_data" / "sample.dxf"
    
    if not test_file.exists():
        print(f"❌ 测试文件不存在: {test_file}")
        return False
    
    print(f"📂 读取测试文件: {test_file.name}")
    print()
    
    # 解析文件
    parser = SimpleDXFParser(str(test_file))
    parser.read()
    
    # 获取文件信息
    info = parser.get_file_info()
    
    print("📊 文件信息:")
    print(f"  版本: {info['version']}")
    print(f"  图层数: {info['layers_count']}")
    print(f"  实体数: {info['entities_count']}")
    print(f"  文字实体数: {info['text_entities_count']}")
    print()
    
    # 显示文字实体
    print("📝 文字实体:")
    for i, entity in enumerate(parser.text_entities, 1):
        print(f"  {i}. 文字: '{entity['text']}'")
        print(f"     图层: {entity['layer']}")
        print(f"     位置: {entity['position']}")
        print()
    
    # 测试文字替换
    print("🔄 测试文字替换: '施工图' → '竣工图'")
    count = parser.replace_text('施工图', '竣工图')
    print(f"  替换了 {count} 处文字")
    print()
    
    # 保存修改后的文件
    output_file = Path(__file__).parent / "test_data" / "sample_modified.dxf"
    parser.save(str(output_file))
    print(f"✅ 已保存到: {output_file.name}")
    print()
    
    # 验证修改
    print("🔍 验证修改:")
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if '竣工图' in content:
            print("  ✅ 文字替换成功！")
        else:
            print("  ❌ 文字替换失败！")
    
    print()
    print("=" * 60)
    print("  测试完成！")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_parse_dxf()
    sys.exit(0 if success else 1)
