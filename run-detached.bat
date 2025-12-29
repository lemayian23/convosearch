@echo off
echo Starting ConvoSearch services in background...
docker-compose up -d
echo Services started! Check with: docker-compose ps
pause