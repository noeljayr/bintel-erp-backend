# Django Backend Setup Script for PowerShell
Write-Host "🚀 Django Backend Setup" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green

try {
    Write-Host "`n📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    
    Write-Host "`n🔄 Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    
    Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    Write-Host "`n🔄 Creating migrations..." -ForegroundColor Yellow
    python manage.py makemigrations users
    python manage.py makemigrations requests
    
    Write-Host "`n🔄 Running migrations..." -ForegroundColor Yellow
    python manage.py migrate
    
    Write-Host "`n🎉 Setup completed successfully!" -ForegroundColor Green
    Write-Host "`n🚀 To start the server:" -ForegroundColor Cyan
    Write-Host "   python manage.py runserver 5100" -ForegroundColor White
    Write-Host "`n📚 API Documentation:" -ForegroundColor Cyan
    Write-Host "   Swagger UI: http://localhost:5100/api/docs/" -ForegroundColor White
    Write-Host "   ReDoc:      http://localhost:5100/api/redoc/" -ForegroundColor White
    Write-Host "`n📝 Don't forget to update your .env file!" -ForegroundColor Yellow
    
} catch {
    Write-Host "`n❌ Setup failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`nTrying direct installation..." -ForegroundColor Yellow
    
    try {
        pip install -r requirements.txt
        python manage.py makemigrations users
        python manage.py makemigrations requests
        python manage.py migrate
        
        Write-Host "`n✅ Direct installation successful!" -ForegroundColor Green
        Write-Host "`n🚀 To start the server:" -ForegroundColor Cyan
        Write-Host "   python manage.py runserver 5100" -ForegroundColor White
        
    } catch {
        Write-Host "`n❌ Direct installation also failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "`nPlease run commands manually:" -ForegroundColor Yellow
        Write-Host "   pip install -r requirements.txt" -ForegroundColor White
        Write-Host "   python manage.py makemigrations" -ForegroundColor White
        Write-Host "   python manage.py migrate" -ForegroundColor White
    }
}

Read-Host "`nPress Enter to continue"