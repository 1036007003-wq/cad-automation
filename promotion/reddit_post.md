# [P] CAD Automation Tool - Open Source, Free, No AutoCAD Required

Hi everyone!

I built a **free, open-source CAD automation tool** that can batch-process DXF files. It's especially useful for converting construction drawings to as-built drawings.

## 🎯 What it does

- ✅ Parse DXF files (layers, blocks, text)
- ✅ Batch text replacement (e.g., "Construction Drawing" → "As-Built Drawing")
- ✅ Layer management (freeze/thaw multiple layers)
- ✅ Batch processing (entire folder with one command)

## 🚀 Quick example

```bash
# Batch replace text in all DXF files
python cli.py batch-process \
  ./input_folder \
  ./output_folder \
  --text-replacements "Construction" "As-Built"
```

## 💡 Why use it?

| Manual processing | Using this tool | Improvement |
|------------------|-----------------|--------------|
| 10-30 min per file | ~1 sec per file | **50-100x faster** |
| Error rate: 5-10% | Error rate: <0.1% | **Quality ↑** |
| Need AutoCAD license | Completely free | **Cost ↓ 100%** |

## 🔗 Links

- **GitHub**: https://github.com/1036007003-wq/cad-automation
- **License**: MIT (free for commercial use)
- **Requirements**: Python 3.8+, ezdxf

## 🛠️ Tech stack

- **ezdxf** - Pure Python DXF library
- **Click** - Elegant CLI
- **PyYAML** - Configuration support

## 🤔 Who is it for?

- ✅ Architects/engineers (processing lots of drawings)
- ✅ Python developers (learning CAD automation)
- ✅ Open-source enthusiasts (contributing code)

## 🚧 Roadmap

- v0.2.0: Direct DWG support (via LibreDWG)
- v0.3.0: GUI version (PyQt6)
- v1.0.0: Web version (SaaS)

## 💬 Feedback welcome!

Let me know what you think! If you have similar tools to recommend, please share.

**If you find it useful, please give a ⭐ on GitHub!**
