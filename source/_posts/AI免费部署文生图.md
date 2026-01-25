---
title: AI免费部署文生图
date: 2025-08-19 12:00:00
categories: #分类
  - 工具 
  - 热门
tags: #标签
  - AI
comments: true
top: 2 # 置顶
cover: https://imgbed.138gl.com/file/blog/文章/AI/1755614107881_TWAIbt-001.png
mathjax: true # 数学公式支持
toc: true # 显示目录
---
<img src="https://imgbed.138gl.com/file/blog/文章/AI/1755614107881_TWAIbt-001.png" alt="AI免费部署文生图">

## 文生图AI部署

1.域名:如(ai.138gl.com)，需要自己购买或注册免费域名。

2.登录Cloudflare

3.Wercker部署 [复制Wercker代码➡️](https://github.com/gl33332/138gl-ai/blob/main/worker.js)

4.登录Wercker，创建新的Hello World项目，将复制的代码粘贴到项目中。

5.拉到代码第75行，const PASSWORDS = [‘admin123’]，将admin123替换为自己的密码。

6.左侧工具栏右键新建文件名称 index.html [复制index.html代码➡️](https://github.com/gl33332/138gl-ai/blob/main/index.html)将以下代码复制到新建文件中。

7.点击部署，等待部署完成。

8.返回Workers 和 Pages 页面点击 绑定 。

9.打开绑定页面后点击添加绑定选择 Workers AI 绑定。

10.绑定完成后点击返回 Workers 和 Pages 页面。

11.如果有域名的话在此处选择 域或路由 点击右侧添加例如: ai.138gl.com 点击添加。

12.等待域名解析完后就可以打开浏览器输入 ai.138gl.com 就可以使用了。