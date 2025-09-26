@echo off
echo 🚀 Starting Django Development Server with SQLite
echo ================================================

echo.
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo 🚀 Starting server on http://localhost:5100/
echo.
echo 📚 API Documentation will be available at:
echo    Swagger UI: http://localhost:5100/api/docs/
echo    ReDoc:      http://localhost:5100/api/redoc/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 5100 --settings=backend.settings_sqlite