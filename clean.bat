@echo off
echo Cleaning up ConvoSearch...
docker-compose down
rmdir /s /q data 2>nul
rmdir /s /q logs 2>nul
echo Cleanup complete!
pause