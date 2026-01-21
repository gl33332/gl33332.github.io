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