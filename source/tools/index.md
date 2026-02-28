---
title: 我的轻量级工具箱
date: 2026-02-28 17:16:20
---

> 这里不存垃圾，只留经过实战检验的轻量化重型武器。

## 1) Whisper 本地转写脚本（速记版）

适用：会议录音、电话语音、微信语音导出后批量转写。

```bash
# 单文件
whisper input/demo.m4a --language zh --model medium --output_dir output

# 批量
for f in input/*.{m4a,mp3,wav}; do
  [ -e "$f" ] || continue
  whisper "$f" --language zh --model medium --output_dir output
done
```

## 2) NAS 映射（Linux）

```bash
sudo mkdir -p /mnt/nas
sudo mount -t cifs //NAS_IP/share /mnt/nas \
  -o username=YOUR_USER,password=YOUR_PASS,iocharset=utf8,vers=3.0
```

```fstab
//NAS_IP/share /mnt/nas cifs credentials=/home/gl/.smbcredentials,iocharset=utf8,vers=3.0,_netdev 0 0
```
