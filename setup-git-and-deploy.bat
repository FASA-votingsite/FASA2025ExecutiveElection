@echo off
echo 🚀 Setting up Git and Deploying...

echo.
echo 📝 Setting Git identity...
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

echo.
echo 🔍 Checking Git status...
git status

echo.
echo 🌐 Setting up remote repository...
set /p "github_username=Enter your GitHub username: "
git remote add origin https://github.com/%github_username%/uniben-art-voting.git

echo.
echo 📦 Building React app...
cd frontend
npm run build
cd ..

echo.
echo 📁 Creating docs folder...
if exist "docs" rmdir /s /q docs
mkdir docs
xcopy /s /e /y "frontend\build\*" "docs\"

echo.
echo 💾 Committing and pushing...
git add docs/
git commit -m "Deploy frontend to GitHub Pages"

echo.
echo 📤 Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ Done! Now enable GitHub Pages:
echo 1. Go to: https://github.com/%github_username%/uniben-art-voting/settings/pages
echo 2. Set source to: Deploy from branch: main, folder: /docs
echo 3. Wait a few minutes for deployment
echo 4. Your site: https://%github_username%.github.io/uniben-art-voting
pause