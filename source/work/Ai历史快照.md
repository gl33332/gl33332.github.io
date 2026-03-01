---
title: Ai历史快照
date: 2026-03-01 01:40:00
slug: ai-history-snapshot-20260301
permalink: /work/ai-history-snapshot-20260301/index.html
password: __WORK_PASS__
abstract: 🔐 三脑协作与博客修复发布事故全流程快照（内部）
message: ⚠️ 内部资料，请输入授权密码访问。
tags:
  - 私密归档
  - 运维复盘
  - 三脑协同
---

# ✅ 2026-02-28 ~ 2026-03-01 博客修复与发布事故快照

## 一、三脑角色与 Bot

- A 脑（主控）：@gl33331_bot
- B 脑（执行）：@gl33332_bot
- C 脑（审计）：@gl33333_bot

## 二、分支/部署架构（最终定稿）

- `master`：**源码主分支**（最终确认后才合并/推送）
- `preview`：**预览源码分支**（外部/移动端写作都先推这里）
- `main`：**生产镜像分支**（只放 Hexo 生成后的静态文件；Cloudflare Pages 生产站 `blog.138gl.com` 只看这里）
- `gh-pages`：**已删除**（曾临时用于预览，最终确认多余并清理）

## 三、预览地址规则（强制执行）

- 预览地址不是固定域名；每次 Deploy Preview 都会生成随机前缀 pages.dev：
  例：`https://8753ee22.gl33332-github-io.pages.dev/`
- 预览验收必须从 GitHub Actions / Deployments → View deployment 获取“本次最新 URL”
- 禁止使用旧 pages.dev 地址/缓存地址做验收

## 四、密码安全铁律（强制执行）

- 仓库任何文件禁止出现真实密码
- 只允许 `password: __WORK_PASS__` 占位符
- 真密码只放 GitHub Actions Secret：`WORK_PASS`
- 注入只在 CI runtime 做（不落盘到仓库/历史）

## 五、关键事故与修复时间线（摘要）

### 1) work 私密区加密链路修复

- 修复目标：`/work/` 必须弹密码框，且正文不明文直出
- 验收：本地与 pages.dev 预览均出现密码框，通过

### 2) gh-pages 临时引入与最终删除

- 曾因 peaceiris/actions-gh-pages 报错：`You deploy from preview to preview`
- 临时改 publish_branch 解决后，最终确认与你的 Cloudflare 分支模型冲突
- 已远端删除 gh-pages 并清理引用

### 3) 生产构建失败：缺少 brevity.yaml（Solitude）

- 报错：`If brevity is enabled, brevity data must be supplied! Please create brevity.yaml.`
- 先补文件 → 后发现类型错误导致 pug 白屏

### 4) 白屏根因最终定位：brevity 数据结构不对

- 本地复现关键报错：
  `site.data.brevity.slice is not a function`
  来自 `hexo-theme-solitude/layout/includes/widgets/home/bbTimeList.pug`
- 结论：`source/_data/brevity.yaml` 必须是顶层数组
- 修复：`brevity.yaml` 内容改为：

```yaml
[]
```

- 修复后：本地 build 通过、线上白屏消失

### 5) 工作台文章 404：缺失源文件 + 伪链接

- `source/work/index.md` 使用 `{{...}}` 伪链接且目标 md 文件不存在 → 404
- 修复：补齐缺失文章 + 采用稳定 slug 路由 + 修复 index 链接

### 6) 旧中文 .html 链接兼容跳转

- 旧地址：`/work/2026-02-28-石矿项目决策复盘.html`
- 新地址：`/work/shikuang-decision-review-20260228/`
- 已添加跳转页，最终验收：旧链接自动跳转正确 ✅

## 六、关键提交（群内回执）

- `ae3955da…`：master 上清理旧密码/去敏 message（通过审计）
- `f54c222…`：新增 `source/_data/brevity.yaml`（解决缺文件）
- `9418d23…`：`brevity.yaml` 改为顶层数组 `[]`（解决白屏根因）
- `48ac2431…`：补齐缺失文章 + 修复 work/index 链接 + stable permalink/slug
- `0158727…`：旧中文 URL → 新 slug 的跳转页

## 七、GitHub Actions 工作流（当前原则）

- Production：`master` 触发 → 构建 → 推送静态产物到 `main`
- Preview：`preview` 触发 → 构建 → 输出到预览通道，并用 pages.dev 最新 URL 验收
- `WORK_PASS` 注入在 CI runtime 进行，对以下文件做替换：
  - `source/_posts/work-gateway.md`
  - `source/tools/index.md`
  - `source/work/index.md`
  - 以及 work 下需要加密的文章（如复盘）

## 八、固定执行命令（规程用）

### 提交到 preview（外部改动/预览）

```bash
git checkout preview
git pull
git status -sb # 必须干净
git add -A
git commit -m "..."
git push origin preview
```

### 正式上线（preview → master）

```bash
git checkout master
git pull
git merge --no-ff preview
git push origin master
```

### 本地预览（Hexo）

```bash
cd /home/gl/gl33332.github.io
npx --no-install hexo clean
npx --no-install hexo s -i 0.0.0.0 -p 4000
```

### 安全审计（上线前）

```bash
git grep -n "" || true
git grep -n "d" || true
git grep -n "password:" source || true
```

## 九、最终验收清单（必须全部通过）

- 预览（pages.dev 最新 URL）：
  - `/work/` 弹密码框
  - `/tools/` 弹密码框
- 生产（blog.138gl.com）：
  - `/` 不白屏
  - `/work/` 弹密码框
  - `/tools/` 弹密码框
- 旧中文链接自动跳转到新 slug（如石矿复盘）

---

> 后续约定：你每次发送“快照内容”，默认按同样流程处理——加密入私密工作台并标准化命名归档。
