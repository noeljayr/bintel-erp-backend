@echo off
echo 🐳 Starting Django Backend with Docker
echo ======================================

echo.
echo 🔄 Building and starting containers...
echo This may take a few minutes on first run...
echo.

docker-compose -f docker-compose.simple.yml up --build

echo.
echo 🛑 Containers stopped.
echo To run in background: docker-compose -f docker-compose.simple.yml up -d --build
pause