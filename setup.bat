@echo off
echo 🚀 Django Backend Setup for Windows
echo =====================================

echo.
echo 📦 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    echo Trying direct installation...
    goto direct_install
)

echo.
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    echo Trying direct installation...
    goto direct_install
)

echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    goto error_exit
)

goto run_migrations

:direct_install
echo.
echo 📥 Installing dependencies directly...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    goto error_exit
)

:run_migrations
echo.
echo 🔄 Creating migrations...
python manage.py makemigrations users
python manage.py makemigrations requests

echo.
echo 🔄 Running migrations...
python manage.py migrate
if errorlevel 1 (
    echo ❌ Failed to run migrations
    goto error_exit
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 🚀 To start the server:
echo    python manage.py runserver 5100
echo.
echo 📚 API Documentation:
echo    Swagger UI: http://localhost:5100/api/docs/
echo    ReDoc:      http://localhost:5100/api/redoc/
echo.
echo 📝 Don't forget to update your .env file with database credentials
pause
exit /b 0

:error_exit
echo.
echo ❌ Setup failed. Please check the error messages above.
echo You can try running commands manually:
echo    pip install -r requirements.txt
echo    python manage.py makemigrations
echo    python manage.py migrate
pause
exit /b 1