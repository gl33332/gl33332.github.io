@echo off
setlocal enabledelayedexpansion

echo ======================================================
echo   正在启动：博客一键更新（番剧同步 + 源码备份 + 发布）
echo ======================================================

:: 1. 同步番剧数据 (如果你在 Bangumi 上有新动作)
echo [Step 1/4] 正在抓取 Bangumi.tv 番剧数据...
call hexo bangumi -u

:: ...前面的 pull 逻辑保持不变...

git add .
:: 下面这行会自动判断是否有改动，没改动就不 commit
git diff --quiet --exit-code --cached || git commit -m "Site Update: %date% %time%"

git push origin master
echo.
echo ======================================================
echo   任务完成！源码已推送，请稍后访问 blog.138gl.com
echo ======================================================
pause