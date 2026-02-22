@echo off
setlocal enabledelayedexpansion

echo ======================================================
echo   正在启动：博客一键更新 (拉取 + 番剧 + 源码 + 发布)
echo ======================================================

:: 1. 同步远程仓库，防止多端同步冲突
echo [Step 1/4] 正在从 GitHub 拉取最新源码...
git pull origin master

:: 2. 抓取番剧数据
:: 使用 call 确保 hexo 运行，即便报错也会继续执行下一步
echo [Step 2/4] 正在同步 Bangumi 番剧数据 (包含手动 JSON)...
call hexo bangumi -u || echo [!] 提示：番剧同步出现部分错误，已跳过，将使用本地缓存数据继续...

:: 3. 处理源码变动
echo [Step 3/4] 正在扫描文件变动...
git add .

:: 检查是否有已暂存的改动，避免空提交报错
git diff --quiet --exit-code --cached || (
    echo 发现变动，正在记录更新日志...
    git commit -m "Site Update: %date:~0,10% %time:~0,5%"
)

:: 4. 推送到远程触发 GitHub Actions 自动部署
echo [Step 4/4] 正在推送到 GitHub，请稍候...
git push origin master

echo.
echo ======================================================
echo   恭喜！所有任务已处理完毕。
echo   1. 源码已成功备份至 GitHub。
echo   2. GitHub Actions 正在后台构建部署。
echo   约 1-2 分钟后访问: https://blog.138gl.com
echo ======================================================
pause