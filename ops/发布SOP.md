# 博客发布 SOP（GitHub Actions）

## 发布原则
- 仅使用 GitHub Actions 发布，禁止本地 `hexo deploy` 直推。
- `master` 分支自动发布到 `preview`。
- 正式发布通过手动触发 `Deploy Production` 工作流。

## 日常预览发布
1. 本地提交到 `master`。
2. 等待工作流 `Deploy Preview` 执行完成。
3. 访问预览站验证页面、样式、文章链接。

## 正式发布
1. 在 GitHub Actions 手动运行 `Deploy Production`。
2. 确认 `main` 分支更新成功。
3. 抽查首页、文章页、搜索、分类、标签页。

## 发布前检查
- 执行：`npm run verify`
- 确认无明显报错和构建失败。
- 核对当天新增文章日期、分类、标签。

## 回滚策略
- 方式一：在 `main` 分支回滚到上一稳定提交并重新触发 `Deploy Production`。
- 方式二：在 `master` 修复后重新触发预览与正式发布。
