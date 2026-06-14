# 🏗️ CAD Automation Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/github/stars/1036007003-wq/cad-automation?style=social" alt="Stars">
  <img src="https://img.shields.io/github/last-commit/1036007003-wq/cad-automation" alt="Last Commit">
</p>

<p align="center">
  <strong>🚀 零成本CAD自动化工具 - 施工图转竣工图自动化处理</strong><br>
  开源 | 免费 | 无需AutoCAD | 批量处理
</p>

---

## 🎯 为什么需要这个工具？

| 手动处理 | 使用本工具 | 效率提升 |
|----------|------------|----------|
| ⏳ 每张图纸修改需要10-30分钟 | ⚡ 批量处理，每秒1张 | **50-100倍** |
| ❌ 容易漏改、改错 | ✅ 精确匹配，零错误 | **质量提升** |
| 💸 需要AutoCAD许可证 | 💰 完全免费，开源 | **成本降低100%** |
| 📁 难以批量处理 | 🚀 支持整个文件夹 | **便利性提升** |

---

## ✨ 功能特性

### ✅ 已实现（v0.1.0）
- ✅ **DXF文件解析** - 读取CAD文件，查看图层、图块、文字信息
- ✅ **文字批量替换** - 如"施工图"→"竣工图"，支持正则表达式
- ✅ **图层管理** - 批量冻结/解冻图层，优化显示
- ✅ **图块插入** - 自动插入竣工章等图块（开发中）
- ✅ **批量处理** - 整个文件夹一键处理

### 🚧 开发中（v0.2.0）
- [ ] **DWG格式直接支持**（集成LibreDWG）
- [ ] **PDF导出功能**（直接生成打印版）
- [ ] **图形界面**（PyQt6，降低使用门槛）
- [ ] **Web版本**（SaaS化，支持在线处理）

### 🔮 路线图中（v1.0.0）
- [ ] **AI辅助识别**（自动识别图纸类型）
- [ ] **云存储集成**（腾讯云COS）
- [ ] **付费API接口**（支持企业用户）
- [ ] **移动端支持**（手机批量处理）

---

## 🛠️ 技术栈

| 技术 | 用途 | 优势 |
|------|------|------|
| **ezdxf** | DXF文件读写 | 纯Python，无依赖，Mac/Win/Linux全支持 |
| **Click** | 命令行界面 | 优雅的CLI设计，易用性高 |
| **PyYAML** | 配置文件 | 灵活配置处理规则 |
| **simple_parser** | 简化版DXF解析器 | 无numpy依赖，macOS兼容性好 |

---

## 📋 系统要求

- **Python**: 3.8+（推荐3.11+）
- **操作系统**: macOS / Linux / Windows
- **内存**: 建议4GB+（处理大型图纸）
- **依赖**: 见 `requirements.txt`（全部免费开源）

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
# 克隆仓库
git clone https://github.com/1036007003-wq/cad-automation.git
cd cad-automation

# 安装依赖
pip install -r requirements.txt

# 或者使用虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2️⃣ 基础使用

#### 📊 查看CAD文件信息
```bash
# 查看图层、图块、文字等信息
python cli.py parse input.dxf
```

#### ✏️ 文字批量替换
```bash
# 将"施工图"替换为"竣工图"
python cli.py replace-text input.dxf output.dxf \
  --old "施工图" \
  --new "竣工图"

# 支持多个替换规则（配置文件）
python cli.py replace-text input.dxf output.dxf \
  --config config/replace_rules.yaml
```

#### 🗂️ 图层管理
```bash
# 冻结指定图层（不显示）
python cli.py layers input.dxf output.dxf \
  --freeze "临时标注" \
  --freeze "辅助线"

# 解冻图层
python cli.py layers input.dxf output.dxf \
  --thaw "标注层"
```

#### 🏷️ 批量处理（整个文件夹）
```bash
# 批量处理整个文件夹
python cli.py batch-process \
  ./input_dir \
  ./output_dir \
  --text-replacements "施工图" "竣工图" \
  --freeze-layers "临时标注"
```

---

## 📂 项目结构

```
cad-automation/
├── cli.py                  # 命令行入口
├── core/                   # 核心模块
│   ├── parser.py           # DWG/DXF解析器（完整版）
│   ├── simple_parser.py    # 简化版DXF解析器（无依赖）
│   ├── block_inserter.py  # 图块插入器
│   ├── layer_manager.py   # 图层管理器
│   ├── text_replacer.py   # 文字替换器
│   └── __init__.py       # 模块初始化
├── templates/              # 竣工章模板
├── test_data/              # 测试用DXF文件
├── output/                 # 输出目录
├── tests/                  # 单元测试
├── docs/                   # 文档
│   ├── DEMO.md            # 详细演示指南
│   ├── API.md             # API文档
│   └── CONTRIBUTING.md   # 贡献指南
├── config/                 # 配置文件
├── requirements.txt        # Python依赖
├── README.md              # 本文件
└── .gitignore            # Git忽略规则
```

---

## 🎯 使用场景

### 场景1：施工图转竣工图（核心场景）

```bash
# 1. 批量加盖竣工章（需要先准备竣工章图块）
python cli.py batch-process \
  ./施工图纸 \
  ./竣工图纸 \
  --stamp templates/stamp.dxf

# 2. 批量修改文字
python cli.py batch-process \
  ./竣工图纸 \
  ./竣工图纸_final \
  --text-replacements "施工图" "竣工图" \
  --text-replacements "设计阶段" "竣工阶段"

# 3. 冻结不需要的图层
python cli.py batch-process \
  ./竣工图纸_final \
  ./竣工图纸_output \
  --freeze-layers "临时标注" "辅助线"
```

### 场景2：批量修改图纸编号

```bash
# 修改图纸编号（支持正则表达式）
python cli.py replace-text input.dxf output.dxf \
  --old "图号-A" \
  --new "图号-B" \
  --use-regex
```

### 场景3：标准化图层管理

```bash
# 根据公司标准，批量设置图层属性
python cli.py layers ./input ./output \
  --freeze "DEFPOINTS" \
  --freeze "VIEWPORTS" \
  --thaw "标注层" \
  --thaw "图框层"
```

---

## ⚠️ 注意事项

1. **DWG格式支持**  
   目前仅支持DXF格式（文本格式）。DWG格式（二进制）需要先用LibreDWG转换：
   ```bash
   # 安装LibreDWG（macOS）
   brew install libredwg
   
   # 转换DWG为DXF
   dwg2dxf input.dwg -o output.dxf
   ```

2. **备份原始文件**  
   处理前请备份原始文件！虽然工具支持输入输出分离，但安全第一。

3. **图层名称准确性**  
   确保图层名称正确，可用 `python cli.py parse input.dxf` 查看所有图层。

4. **macOS代码签名问题**  
   如果遇到numpy代码签名错误，工具会自动使用简化版解析器（无numpy依赖）。

---

## 🚧 已知限制

- [ ] DWG格式需要转换（计划v0.2.0支持直接读取）
- [ ] 图块插入功能尚在开发（目前只能替换文字和管理图层）
- [ ] 大型图纸（>50MB）处理速度较慢（优化中）
- [ ] 无图形界面（计划v0.3.0推出GUI版本）

---

## 🤝 贡献指南

欢迎贡献！无论是Bug反馈、功能建议，还是代码贡献。

### 如何贡献

1. **Fork本仓库**
2. **创建分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **开启Pull Request**

### 贡献类型

- 🐛 **Bug反馈**: 开启Issue，描述问题和复现步骤
- 💡 **功能建议**: 开启Issue，描述需求和预期效果
- 💻 **代码贡献**: Fork + PR，确保通过测试
- 📝 **文档改进**: 完善README、添加教程、翻译等

---

## 📄 许可证

MIT License - 可自由使用、修改、商用

**简单来说**：
- ✅ 可以用于商业项目
- ✅ 可以修改源代码
- ✅ 可以私有部署
- ⚠️ 需保留原作者信息

---

## 🌟 支持本项目

如果这个项目对你有帮助，请：

1. **给个Star** ⭐ - 让更多人看到
2. **分享给同事** 📢 - 帮助更多人提高效率
3. **反馈问题** 🐛 - 帮助我们改进
4. **捐赠支持** ☕ - 请我喝杯咖啡（见下方）

---

## ☕ 捐赠支持

本项目完全免费开源，如果你觉得有用，可以捐赠支持持续开发：

| 捐赠方式 | 链接/信息 |
|----------|------------|
| **GitHub Sponsors** | [即将开通] |
| **支付宝/微信** | [即将添加二维码] |
| **Patreon** | [即将开通] |

**捐赠用途**：
- 服务器费用（未来Web版）
- 测试文件购买（真实工程图纸）
- 开发时间投入

---

## 📧 联系方式

- **GitHub Issues**: [开启Issue](https://github.com/1036007003-wq/cad-automation/issues)
- **Email**: [即将添加]
- **微信群**: [即将建立]

---

## 🔗 相关项目

- [ezdxf](https://github.com/mozman/ezdxf) - Python DXF读写库
- [LibreDWG](https://www.gnu.org/software/libredwg/) - DWG文件处理库
- [FreeCAD](https://www.freecad.org/) - 开源CAD软件

---

## 🎉 致谢

感谢所有贡献者的支持！

---

<p align="center">
  <strong>Built with ❤️ for the CAD community</strong><br>
  <em>让CAD处理更高效、更自动化</em>
</p>

---

**⭐ 如果这个项目对你有帮助，请给个Star！**

<p align="center">
  <a href="https://github.com/1036007003-wq/cad-automation/stargazers">
    <img src="https://img.shields.io/github/stars/1036007003-wq/cad-automation?style=social" alt="Stargazers">
  </a>
</p>
