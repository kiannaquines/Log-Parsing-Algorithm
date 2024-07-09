@echo off

set /p message="Enter commit message: "
set /p branch="Enter your branch: "


git add .
git commit -m "%message%"
git push -u origin %branch%

timeout /t 6 /nobreak

cls