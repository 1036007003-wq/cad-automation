"""
CAD Automation Tool - 命令行入口
支持：DWG/DXF解析、竣工章加盖、图层管理、文字替换
"""
import click
import os
import sys
from pathlib import Path
from core.parser import DWGParser
from core.block_inserter import BlockInserter
from core.layer_manager import LayerManager
from core.text_replacer import TextReplacer

@click.group()
@click.version_option("1.0.0")
def cli():
    """CAD自动化工具 - 施工图转竣工图自动化处理"""
    pass

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", help="输出文件路径")
def parse(input_file, output):
    """解析DWG/DXF文件，查看图层、图块信息"""
    click.echo(f"📂 正在解析: {input_file}")
    parser = DWGParser(input_file)
    info = parser.get_file_info()
    
    click.echo(f"\n文件信息:")
    click.echo(f"  格式: {info['version']}")
    click.echo(f"  图层数: {info['layers_count']}")
    click.echo(f"  图块数: {info['blocks_count']}")
    click.echo(f"  实体数: {info['entities_count']}")
    
    if output:
        parser.save(output)
        click.echo(f"\n✅ 已保存到: {output}")

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--stamp", "-s", help="竣工章图块文件路径(.dxf)")
@click.option("--position", "-p", nargs=2, type=float, default=(100, 100), 
              help="竣工章插入位置 (x y)")
def add_stamp(input_file, output_file, stamp, position):
    """批量加盖竣工章"""
    click.echo(f"📝 处理文件: {input_file}")
    
    inserter = BlockInserter(input_file)
    
    if stamp:
        click.echo(f"  使用图章: {stamp}")
        inserter.insert_stamp(stamp, position)
    else:
        click.echo("  使用默认竣工章")
        inserter.add_default_stamp(position)
    
    inserter.save(output_file)
    click.echo(f"\n✅ 已保存: {output_file}")

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--freeze", "-f", multiple=True, help="要冻结的图层")
@click.option("--thaw", "-t", multiple=True, help="要解冻的图层")
def layers(input_file, output_file, freeze, thaw):
    """管理图层（冻结/解冻）"""
    click.echo(f"📂 处理图层: {input_file}")
    
    manager = LayerManager(input_file)
    
    if freeze:
        for layer in freeze:
            click.echo(f"  冻结图层: {layer}")
            manager.freeze_layer(layer)
    
    if thaw:
        for layer in thaw:
            click.echo(f"  解冻图层: {layer}")
            manager.thaw_layer(layer)
    
    manager.save(output_file)
    click.echo(f"\n✅ 已保存: {output_file}")

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--old", "-o", required=True, help="要替换的文字")
@click.option("--new", "-n", required=True, help="新文字")
@click.option("--layer", "-l", help="限定图层（可选）")
def replace_text(input_file, output_file, old, new, layer):
    """批量替换文字（如：施工图 → 竣工图）"""
    click.echo(f"📝 替换文字: {input_file}")
    click.echo(f"  '{old}' → '{new}'")
    
    replacer = TextReplacer(input_file)
    count = replacer.replace_text(old, new, layer)
    
    replacer.save(output_file)
    click.echo(f"\n✅ 替换了 {count} 处文字")
    click.echo(f"✅ 已保存: {output_file}")

@cli.command()
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False))
@click.argument("output_dir", type=click.Path())
@click.option("--stamp", "-s", help="竣工章图块")
@click.option("--text-replacements", "-t", nargs=2, multiple=True, 
              help="文字替换规则，可多次使用（如：-t '施工图' '竣工图'）")
def batch_process(input_dir, output_dir, stamp, text_replacements):
    """批量处理文件夹中的所有DWG/DXF文件"""
    click.echo(f"📂 批量处理: {input_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 查找所有DWG/DXF文件
    input_path = Path(input_dir)
    files = list(input_path.glob("*.dxf")) + list(input_path.glob("*.DWG"))
    
    if not files:
        click.echo("❌ 未找到DWG/DXF文件")
        return
    
    click.echo(f"  找到 {len(files)} 个文件")
    
    for file in files:
        click.echo(f"\n处理: {file.name}")
        output_file = Path(output_dir) / file.name
        
        # 处理流程
        doc = DWGParser(str(file))
        
        # 加盖竣工章
        inserter = BlockInserter(doc)
        if stamp:
            inserter.insert_stamp(stamp)
        else:
            inserter.add_default_stamp()
        
        # 文字替换
        if text_replacements:
            replacer = TextReplacer(doc)
            for old_text, new_text in text_replacements:
                replacer.replace_text(old_text, new_text)
        
        # 保存
        inserter.save(str(output_file))
        click.echo(f"  ✅ 已保存: {output_file.name}")
    
    click.echo(f"\n🎉 批量处理完成！共处理 {len(files)} 个文件")

if __name__ == "__main__":
    cli()
