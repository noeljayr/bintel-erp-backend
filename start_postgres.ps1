# Django with PostgreSQL Startup Script
Write-Host "🐘 Starting Django with PostgreSQL" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

Write-Host "`n🔄 Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

Write-Host "`n🔍 Testing PostgreSQL connection..." -ForegroundColor Yellow
& python test_postgres.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n🔧 Setting up PostgreSQL database..." -ForegroundColor Yellow
    & python setup_postgres.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ PostgreSQL setup failed. Using SQLite instead..." -ForegroundColor Red
        Write-Host "🚀 Starting with SQLite..." -ForegroundColor Yellow
        python manage.py runserver 5100 --settings=backend.settings_sqlite
    } else {
        Write-Host "`n🚀 Starting server with PostgreSQL on http://localhost:5100/" -ForegroundColor Green
        Write-Host "`n📚 API Documentation:" -ForegroundColor Cyan
        Write-Host "   Swagger UI: http://localhost:5100/api/docs/" -ForegroundColor White
        Write-Host "   ReDoc:      http://localhost:5100/api/redoc/" -ForegroundColor White
        Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow
        
        python manage.py runserver 5100
    }
} else {
    Write-Host "`n🚀 Starting server with PostgreSQL on http://localhost:5100/" -ForegroundColor Green
    Write-Host "`n📚 API Documentation:" -ForegroundColor Cyan
    Write-Host "   Swagger UI: http://localhost:5100/api/docs/" -ForegroundColor White
    Write-Host "   ReDoc:      http://localhost:5100/api/redoc/" -ForegroundColor White
    Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow
    
    python manage.py runserver 5100
}