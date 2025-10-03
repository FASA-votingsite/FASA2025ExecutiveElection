# Faculty Voting System - Frontend Deployment Script
Write-Host "🚀 Deploying Faculty Voting Frontend to GitHub Pages..." -ForegroundColor Green

# Step 1: Build React app
Write-Host "📦 Building React app..." -ForegroundColor Yellow
Set-Location frontend

# Check if node_modules exists
if (-Not (Test-Path "node_modules")) {
    Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Build the app
npm run build

# Check if build was successful
if (-Not (Test-Path "build")) {
    Write-Host "❌ Build failed! Check for errors above." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build successful!" -ForegroundColor Green

# Step 2: Create deployment directory
Set-Location ..
if (Test-Path "docs") {
    Remove-Item -Recurse -Force docs
}
New-Item -ItemType Directory -Path docs -Force

# Step 3: Copy build files
Write-Host "📁 Copying build files to docs folder..." -ForegroundColor Yellow
Get-ChildItem "frontend\build\*" -Recurse | Copy-Item -Destination "docs\" -Force

# Step 4: Create README for GitHub Pages
$readmeContent = @"
# Faculty of Art Voting System

This is the frontend for the University of Benin Faculty of Art Voting System.

## Live Site
View the live site at: https://yourusername.github.io/uniben-art-voting

## Backend API
The backend is hosted separately and provides the API for this frontend.

## Student Login
Students can login with their matric number and password.

## Admin Access
Admin panel is available at the backend URL.
"@

Out-File -FilePath "docs\README.md" -InputObject $readmeContent -Encoding UTF8

Write-Host "✅ Deployment files prepared!" -ForegroundColor Green
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Commit and push the docs folder" -ForegroundColor White
Write-Host "2. Go to GitHub repo Settings -> Pages" -ForegroundColor White
Write-Host "3. Set source to 'Deploy from a branch' and branch to 'main' folder '/docs'" -ForegroundColor White
Write-Host "4. Your site will be available at: https://yourusername.github.io/uniben-art-voting" -ForegroundColor Green