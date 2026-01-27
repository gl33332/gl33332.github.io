@echo off
setlocal enabledelayedexpansion

echo ======================================================
echo   正在启动：博客一键更新 (拉取 + 番剧 + 源码 + 发布)
echo ======================================================

:: 1. 同步远程仓库，防止覆盖远程手动修改的内容
echo [Step 1/4] 正在拉取远程最新代码...
git pull origin master

:: 2. 抓取番剧数据 (即使失败也不中断后续发布)
echo [Step 2/4] 正在同步 Bangumi 番剧数据...
call hexo bangumi -u || echo [!] 番剧抓取失败，跳过此步...

:: 3. 处理源码变动
echo [Step 3/4] 正在检查文件变更...
git add .

:: 检查是否有已暂存的改动（排除空提交报错）
git diff --quiet --exit-code --cached || (
    echo 发现变动，正在创建本地提交...
    git commit -m "Site Update: %date% %time%"
)

:: 4. 推送到远程触发 GitHub Actions 部署
echo [Step 4/4] 正在推送到 GitHub master 分支...
git push origin master

echo.
echo ======================================================
echo   任务完成！源码已推送。
echo   请等待 GitHub Actions 完成部署 (约 1-2 分钟)
echo   访问地址: blog.138gl.com
echo ======================================================
pause