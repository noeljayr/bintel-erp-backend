# 🚀 Quick Start Guide

## Option 1: Automated Setup (Windows)

### Batch File (Recommended for Windows)

```cmd
setup.bat
```

### PowerShell Script

```powershell
# You may need to enable script execution first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run:
.\setup.ps1
```

### Python Script (Cross-platform)

```bash
python setup.py
```

## Option 2: Manual Setup

### 1. Install Dependencies

```bash
# Option A: With virtual environment (recommended)
python -m venv venv

# Windows:
venv\Scripts\activate

# Unix/Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Option B: Direct installation
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create migrations
python manage.py makemigrations users
python manage.py makemigrations requests

# Run migrations
python manage.py migrate
```

### 3. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### 4. Start Server

```bash
python manage.py runserver 5100
```

## 📚 Access Your API

Once the server is running:

- **API Base**: http://localhost:5100/
- **Swagger UI**: http://localhost:5100/api/docs/
- **ReDoc**: http://localhost:5100/api/redoc/
- **Admin Panel**: http://localhost:5100/admin/

## 🔧 Configuration

Update your `.env` file with your database settings:

```env
JWT_SECRET=your-secret-key
SECRET_KEY=your-django-secret
DEBUG=True
DB_NAME=requests_db
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432
```

## 🧪 Test Your Setup

```bash
# Test API endpoints
python test_api.py

# Test documentation
python test_docs.py
```

## 🐳 Docker Alternative

If you prefer Docker:

```bash
# Start with PostgreSQL
docker-compose up -d

# Access at http://localhost:5100/
```

## ❓ Troubleshooting

### Virtual Environment Issues

- Try direct installation: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.8+)

### Database Issues

- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Create database manually if needed

### Permission Issues (Windows)

- Run as Administrator
- Enable PowerShell execution: `Set-ExecutionPolicy RemoteSigned`

### Import Errors

- Ensure all dependencies installed: `pip list`
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

## 📞 Need Help?

1. Check the error messages in the console
2. Verify your Python and pip versions
3. Ensure PostgreSQL is installed and running
4. Check the main README.md for detailed information
