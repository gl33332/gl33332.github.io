---
title: 我的轻量级工具箱
date: 2026-02-28 18:00:00
password: "__WORK_PASS__"
abstract: 🛠️ 集中管理常用的技术脚本和配置方案。此页面受保护，仅限内部授权访问。
message: 🔒 战略级资产库，请输入授权密码。
---

> 这里不存垃圾，只留经过实战检验的轻量化重型武器。

## 🔤 Whisper 转写脚本

### 背景
Mac 上需要快速转写音频文件为文本，原生功能有限。

### 解决方案
```bash
#!/bin/bash
# Whisper 自动转写脚本
# 用途：将音频文件转写为文本并保存

INPUT_FILE="$1"
OUTPUT_DIR="./transcripts"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="$OUTPUT_DIR/${TIMESTAMP}_$(basename "$INPUT_FILE" .m4a).md"

mkdir -p "$OUTPUT_DIR"

echo "🎙️ 开始转写: $INPUT_FILE"
echo "📝 输出文件: $OUTPUT_FILE"

# 使用 Whisper CLI 转写
openai whisper "$INPUT_FILE" --model base --output_dir "$OUTPUT_DIR" --output_format txt --output_dir "$OUTPUT_DIR"

# 转换为 Markdown 格式
if [ -f "$OUTPUT_DIR/$(basename "$INPUT_FILE" .m4a).txt" ]; then
    mv "$OUTPUT_DIR/$(basename "$INPUT_FILE" .m4a).txt" "$OUTPUT_FILE"
    echo "✅ 转写完成！"
    echo "📖 内容预览："
    head -20 "$OUTPUT_FILE"
else
    echo "❌ 转写失败"
    exit 1
fi