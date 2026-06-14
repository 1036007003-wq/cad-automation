# CAD Automation Tool

🚀 **零成本CAD自动化工具** - 施工图转竣工图自动化处理

## ✨ 功能特性

- ✅ **DWG/DXF解析** - 读取CAD文件，查看图层、图块信息
- ✅ **批量加盖竣工章** - 自动插入竣工章图块
- ✅ **图层管理** - 批量冻结/解冻图层
- ✅ **文字批量替换** - 如"施工图"→"竣工图"
- ✅ **批量处理** - 整个文件夹一键处理
- ✅ **PDF导出** - 转换为PDF供打印（开发中）

## 🛠️ 技术栈

- **ezdxf** - 纯Python DXF读写库
- **Click** - 优雅的命令行界面
- **PyYAML** - 配置文件支持

## 📋 系统要求

- Python 3.8+
- macOS / Linux / Windows

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 基础使用

#### 查看CAD文件信息

```bash
python cli.py parse input.dxf
```

#### 加盖竣工章

```bash
python cli.py add-stamp input.dxf output.dxf
```

#### 文字替换

```bash
python cli.py replace-text input.dxf output.dxf --old "施工图" --new "竣工图"
```

#### 图层管理

```bash
# 冻结图层
python cli.py layers input.dxf output.dxf --freeze "Layer1" --freeze "Layer2"

# 解冻图层  
python cli.py layers input.dxf output.dxf --thaw "Layer1"
```

#### 批量处理

```bash
python cli.py batch-process ./input_dir ./output_dir \
  --stamp stamp.dxf \
  --text-replacements "施工图" "竣工图"
```

## 📂 项目结构

```
cad-automation/
├── cli.py              # 命令行入口
├── core/               # 核心模块
│   ├── parser.py       # DWG/DXF解析器
│   ├── block_inserter.py  # 图块插入器
│   ├── layer_manager.py    # 图层管理器
│   └── text_replacer.py   # 文字替换器
├── templates/          # 竣工章模板
├── output/            # 输出目录
├── tests/             # 测试文件
└── requirements.txt   # 依赖列表
```

## 🎯 使用场景

### 场景1：施工图转竣工图

```bash
# 1. 批量加盖竣工章
python cli.py batch-process ./施工图纸 ./竣工图纸 \
  --stamp 竣工章.dxf \
  --text-replacements "施工图" "竣工图"

# 2. 冻结不需要的图层
python cli.py layers ./竣工图纸/*.dxf ./output \
  --freeze "临时标注" --freeze "辅助线"
```

### 场景2：批量修改文字

```bash
# 修改图纸编号
python cli.py batch-process ./input ./output \
  --text-replacements "图号-A" "图号-B"
```

## ⚠️ 注意事项

1. **DWG格式** - 目前仅支持DXF格式，DWG需要先用LibreDWG转换
2. **备份文件** - 处理前请备份原始文件
3. **图层名称** - 确保图层名称正确，可用`parse`命令查看

## 🚧 开发中功能

- [ ] DWG格式直接支持（集成LibreDWG）
- [ ] PDF导出功能
- [ ] Web界面（SaaS化）
- [ ] 云存储集成
- [ ] 付费API接口

## 📄 许可证

MIT License - 可自由使用、修改、商用

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

- GitHub: [你的用户名]
- Email: [你的邮箱]

---

**⭐ 如果这个项目对你有帮助，请给个Star！**
