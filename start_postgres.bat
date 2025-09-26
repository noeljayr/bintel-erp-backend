@echo off
echo 🐘 Starting Django with PostgreSQL
echo ==================================

echo.
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo 🔍 Testing PostgreSQL connection...
python test_postgres.py

if errorlevel 1 (
    echo.
    echo 🔧 Setting up PostgreSQL database...
    python setup_postgres.py
    
    if errorlevel 1 (
        echo.
        echo ❌ PostgreSQL setup failed. Using SQLite instead...
        echo 🚀 Starting with SQLite...
        python manage.py runserver 5100 --settings=backend.settings_sqlite
    ) else (
        echo.
        echo 🚀 Starting server with PostgreSQL on http://localhost:5100/
        echo.
        echo 📚 API Documentation:
        echo    Swagger UI: http://localhost:5100/api/docs/
        echo    ReDoc:      http://localhost:5100/api/redoc/
        echo.
        echo Press Ctrl+C to stop the server
        echo.
        python manage.py runserver 5100
    )
) else (
    echo.
    echo 🚀 Starting server with PostgreSQL on http://localhost:5100/
    echo.
    echo 📚 API Documentation:
    echo    Swagger UI: http://localhost:5100/api/docs/
    echo    ReDoc:      http://localhost:5100/api/redoc/
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    python manage.py runserver 5100
)