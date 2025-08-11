@echo off
echo ========================================
echo   MEDICAL CHATBOT - VERCEL DEPLOYMENT
echo ========================================
echo.

echo Step 1: Checking Vercel CLI...
npx vercel --version
if %errorlevel% neq 0 (
    echo Error: Vercel CLI not available
    exit /b 1
)

echo.
echo Step 2: Starting Vercel login process...
echo Please complete authentication in your browser...
npx vercel login

echo.
echo Step 3: Deploying to production...
npx vercel --prod --confirm

echo.
echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your medical chatbot should now be live!
echo Check the URL provided above.
echo.
pause 