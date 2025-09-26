# Docker Startup Script
Write-Host "🐳 Starting Django Backend with Docker" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

Write-Host "`n🔄 Building and starting containers..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run...`n" -ForegroundColor Yellow

try {
    docker-compose -f docker-compose.simple.yml up --build
} catch {
    Write-Host "`n❌ Docker failed to start. Please ensure Docker is running." -ForegroundColor Red
    Write-Host "💡 Try: docker --version" -ForegroundColor Yellow
}

Write-Host "`n🛑 Containers stopped." -ForegroundColor Yellow
Write-Host "To run in background: docker-compose -f docker-compose.simple.yml up -d --build" -ForegroundColor Cyan

Read-Host "`nPress Enter to continue"