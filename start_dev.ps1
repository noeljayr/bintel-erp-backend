# Django Development Server Startup Script
Write-Host "🚀 Starting Django Development Server with SQLite" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

Write-Host "`n🔄 Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

Write-Host "`n🚀 Starting server on http://localhost:5100/" -ForegroundColor Green
Write-Host "`n📚 API Documentation will be available at:" -ForegroundColor Cyan
Write-Host "   Swagger UI: http://localhost:5100/api/docs/" -ForegroundColor White
Write-Host "   ReDoc:      http://localhost:5100/api/redoc/" -ForegroundColor White
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

python manage.py runserver 5100 --settings=backend.settings_sqlite