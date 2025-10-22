@echo off
echo Testing ConvoSearch Docker Setup...
echo ==================================

echo Step 1: Checking Docker is running...
docker version > nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running or not installed!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo ✅ Docker is running

echo.
echo Step 2: Building containers (this will install all dependencies)...
docker-compose build

if errorlevel 1 (
    echo ❌ Build failed! Check the errors above.
    pause
    exit /b 1
)

echo.
echo Step 3: Testing dependencies inside Docker container...
docker-compose run --rm api python -c "
import sys
modules = ['fastapi', 'uvicorn', 'pydantic', 'chromadb', 'psycopg2', 'sklearn', 'numpy', 'requests']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError as e:
        print(f'❌ {module}: {e}')
        sys.exit(1)
print('🎉 All dependencies installed in Docker container!')
"

if errorlevel 1 (
    echo ❌ Dependency test failed inside container!
    pause
    exit /b 1
)

echo.
echo ✅ SUCCESS: All dependencies are properly installed in Docker!
echo.
echo Next steps:
echo 1. Run: run-detached.bat
echo 2. Then open: http://localhost:8000
echo 3. Or run: demo.bat
pause