# 开源CAD自动化工具：用Python批量处理DXF图纸

## 前言

作为建筑行业从业者，经常需要处理大量CAD图纸。特别是「施工图转竣工图」这种重复性工作，手动处理效率低下且容易出错。

最近用Python开发了一个**零成本、开源的CAD自动化工具**，可以批量处理DXF格式图纸。本文将详细介绍其功能和使用方法。

## 一、工具功能特性

### 1.1 核心功能

| 功能模块 | 描述 | 状态 |
|----------|------|--------|
| **DXF解析器** | 读取DXF文件，提取图层、图块、文字信息 | ✅ 已实现 |
| **文字批量替换** | 支持单文件/批量替换，支持正则表达式 | ✅ 已实现 |
| **图层管理器** | 批量冻结/解冻图层，优化显示 | ✅ 已实现 |
| **图块插入器** | 自动插入竣工章等图块 | 🚧 开发中 |
| **批量处理器** | 整个文件夹一键处理 | ✅ 已实现 |

### 1.2 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.8+ | 主开发语言 |
| ezdxf | 1.0+ | DXF文件读写 |
| Click | 8.0+ | 命令行界面 |
| PyYAML | 6.0+ | 配置文件支持 |

## 二、安装与配置

### 2.1 环境要求

- **Python**: 3.8+（推荐3.11+）
- **操作系统**: macOS / Linux / Windows
- **内存**: 建议4GB+（处理大型图纸）

### 2.2 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/1036007003-wq/cad-automation.git
cd cad-automation

# 2. 创建虚拟环境（推荐）
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
# venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
```

## 三、实战案例：施工图转竣工图

### 3.1 需求分析

假设有以下需求：
1. 将100张施工图纸转换为竣工图
2. 替换所有"施工图"文字为"竣工图"
3. 冻结"临时标注"和"辅助线"图层
4. 插入竣工章图块

### 3.2 实现步骤

#### 步骤1：查看图纸信息

```bash
# 查看单张图纸的图层、文字等信息
python cli.py parse input/图纸001.dxf
```

**输出示例**：
```
图纸信息: 图纸001.dxf
图层数量: 15
图块数量: 3
文字实体数量: 28

主要图层:
  - 0 (默认图层)
  - DEFPOINTS (def点)
  - 标注层
  - 图框层
  - 临时标注 (需要冻结)
```

#### 步骤2：批量替换文字

```bash
# 批量处理整个文件夹
python cli.py batch-process \
  ./input \
  ./output \
  --text-replacements "施工图" "竣工图" \
  --text-replacements "设计阶段" "竣工阶段"
```

#### 步骤3：管理图层

```bash
# 冻结不需要的图层
python cli.py layers \
  ./output/图纸001.dxf \
  ./output_final/图纸001.dxf \
  --freeze "临时标注" \
  --freeze "辅助线"
```

### 3.3 完整脚本

创建 `process_all.sh` 脚本：

```bash
#!/bin/bash

# 1. 批量替换文字
python cli.py batch-process \
  ./input \
  ./temp \
  --text-replacements "施工图" "竣工图"

# 2. 批量冻结图层
python cli.py batch-process \
  ./temp \
  ./output \
  --freeze-layers "临时标注" \
  --freeze-layers "辅助线"

echo "处理完成！输出目录: ./output"
```

运行：
```bash
chmod +x process_all.sh
./process_all.sh
```

## 四、高级功能

### 4.1 使用配置文件

创建 `config/replace_rules.yaml`：

```yaml
replace_rules:
  - old: "施工图"
    new: "竣工图"
  - old: "设计阶段"
    new: "竣工阶段"
  - old: "图号-A"
    new: "图号-B"
```

使用配置：

```bash
python cli.py replace-text input.dxf output.dxf \
  --config config/replace_rules.yaml
```

### 4.2 正则表达式替换

```bash
# 替换所有"图号-XXX"为"图号-YYY"
python cli.py replace-text input.dxf output.dxf \
  --old "图号-.*" \
  --new "图号-新" \
  --use-regex
```

## 五、性能对比

### 5.1 测试环境

- **硬件**: MacBook Pro M2 Pro, 16GB RAM
- **测试文件**: 100张DXF图纸（每张约2-5MB）
- **对比方式**: 手动处理 vs 工具处理

### 5.2 结果

| 处理方式 | 总时间 | 平均每张 | 错误率 |
|----------|----------|----------|---------|
| 手动处理 | ~25小时 | 15分钟 | ~8% |
| 工具处理 | ~3分钟 | 1.8秒 | <0.1% |

**效率提升**: **500倍**  
**质量提升**: **80倍**（错误率降低）

## 六、常见问题

### Q1: 支持DWG格式吗？

**A**: 目前仅支持DXF格式（文本格式）。DWG格式需要先用LibreDWG转换：

```bash
# macOS安装LibreDWG
brew install libredwg

# 转换DWG为DXF
dwg2dxf input.dwg -o output.dxf
```

### Q2: 处理速度如何优化？

**A**: 
1. 使用SSD硬盘（I/O速度更快）
2. 增加内存（处理大型图纸）
3. 使用多进程（工具支持`--workers`参数）

### Q3: 可以商用吗？

**A**: 可以！本工具使用MIT许可证，可自由使用、修改、商用。

## 七、开源地址

**GitHub**: https://github.com/1036007003-wq/cad-automation

**许可证**: MIT License

## 八、后续计划

- [ ] v0.2.0: 支持DWG格式直接读取
- [ ] v0.3.0: 推出图形界面（PyQt6）
- [ ] v1.0.0: Web版本（SaaS化）

## 九、总结

本文介绍了一个开源的CAD自动化工具，可以大幅提升图纸处理效率。适合建筑/工程从业者、Python开发者使用。

如果觉得有用，请：
1. ⭐ 给GitHub仓库点个Star
2. 🔗 分享给需要的同事
3. 🐛 反馈问题或建议

---

**相关资源**:
- ezdxf文档: https://ezdxf.readthedocs.io/
- LibreDWG官网: https://www.gnu.org/software/libredwg/

希望这个工具能帮到大家！欢迎留言交流～
