@echo off
echo 🐘 PostgreSQL Database Setup
echo ============================

echo.
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo 🔧 Setting up PostgreSQL database...
python setup_postgres.py

pause