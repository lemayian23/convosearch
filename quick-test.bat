@echo off
echo ConvoSearch Quick Test for Windows
echo ==================================

echo Checking Docker...
docker version > nul 2>&1
if errorlevel 1 (
    echo ❌ Please start Docker Desktop first!
    pause
    exit /b 1
)

echo.
echo Building containers (this may take a few minutes)...
docker-compose build

if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo Starting services in background...
docker-compose up -d

echo.
echo Waiting for services to start...
timeout /t 15 /nobreak

echo.
echo Testing services...
echo Testing API...
curl -s -o nul -w "%%{http_code}" http://localhost:8000/health | find "200" > nul
if errorlevel 1 (
    echo ❌ API not responding correctly!
    goto :cleanup
) else (
    echo ✅ API is working
)

echo Testing ChromaDB...
curl -s -o nul -w "%%{http_code}" http://localhost:8001/api/v1/heartbeat | find "200" > nul
if errorlevel 1 (
    echo ❌ ChromaDB not responding correctly!
    goto :cleanup
) else (
    echo ✅ ChromaDB is working
)

echo.
echo 🎉 ALL SYSTEMS GO! ConvoSearch is running successfully!
echo.
echo 🌐 Access your application:
echo    Main Interface: http://localhost:8000
echo    Knowledge Chat: http://localhost:8000/chat
echo    Message Triage: http://localhost:8000/triage
echo.
echo Press any key to run the full demo...
pause > nul

echo.
echo Running full demo...
docker-compose run --rm api python scripts/run_demo.py

echo.
:cleanup
echo Press any key to stop services...
pause > nul

echo Stopping services...
docker-compose down
echo Services stopped!