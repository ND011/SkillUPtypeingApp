@echo off
cd /d "%~dp0"

echo # %~n0 > README.md

git init
git remote set-url origin git@github.com:ND011/SkillUPtypeingApp.git

git config user.email "99769678+ND011@users.noreply.github.com"
git config user.name "ND011"

git checkout -b main

git add .
git commit -m "Initial clean commit with all files"

git push -u origin main --force

pause
