#!/usr/bin/env python3
"""
Django Backend Setup Script
This script helps set up the Django backend with PostgreSQL
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stderr:
            print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def setup_with_venv():
    """Setup with virtual environment"""
    print("🚀 Setting up Django Backend with Virtual Environment")
    print("=" * 60)
    
    # Check if virtual environment exists
    venv_exists = os.path.exists('venv') or os.path.exists('.venv')
    
    if not venv_exists:
        print("\n📦 Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            print("❌ Failed to create virtual environment. Trying alternative setup...")
            return False
    
    # Determine activation command
    if os.name == 'nt':  # Windows
        if os.path.exists('venv\\Scripts\\activate.bat'):
            activate_cmd = "venv\\Scripts\\activate.bat && "
        elif os.path.exists('venv\\Scripts\\Activate.ps1'):
            activate_cmd = "powershell -ExecutionPolicy Bypass -File venv\\Scripts\\Activate.ps1 && "
        else:
            print("❌ Virtual environment activation script not found")
            return False
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate && "
    
    # Install dependencies
    if not run_command(f"{activate_cmd}pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies with virtual environment")
        return False
    
    # Create and run migrations
    commands = [
        (f"{activate_cmd}python manage.py makemigrations users", "Creating user migrations"),
        (f"{activate_cmd}python manage.py makemigrations requests", "Creating request migrations"),
        (f"{activate_cmd}python manage.py migrate", "Running migrations")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print(f"❌ Failed at: {desc}")
            return False
    
    # Create superuser (optional)
    print("\n👤 Would you like to create a superuser? (y/n): ", end="")
    if input().lower() == 'y':
        run_command(f"{activate_cmd}python manage.py createsuperuser", "Creating superuser")
    
    return True

def setup_without_venv():
    """Setup without virtual environment (direct pip install)"""
    print("🚀 Setting up Django Backend (Direct Installation)")
    print("=" * 55)
    
    # Install dependencies directly
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Create and run migrations
    commands = [
        ("python manage.py makemigrations users", "Creating user migrations"),
        ("python manage.py makemigrations requests", "Creating request migrations"),
        ("python manage.py migrate", "Running migrations")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print(f"❌ Failed at: {desc}")
            return False
    
    # Create superuser (optional)
    print("\n👤 Would you like to create a superuser? (y/n): ", end="")
    if input().lower() == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    return True

def main():
    print("🐍 Django Backend Setup")
    print("Choose your setup method:")
    print("1. With virtual environment (recommended)")
    print("2. Direct installation (if venv fails)")
    print("3. Manual setup instructions")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    success = False
    
    if choice == '1':
        success = setup_with_venv()
    elif choice == '2':
        success = setup_without_venv()
    elif choice == '3':
        print_manual_instructions()
        return
    else:
        print("❌ Invalid choice. Please run the script again.")
        return
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 To start the server:")
        if choice == '1':
            if os.name == 'nt':
                print("   venv\\Scripts\\activate")
            else:
                print("   source venv/bin/activate")
        print("   python manage.py runserver 5100")
        print("\n📚 Access API Documentation:")
        print("   Swagger UI: http://localhost:5100/api/docs/")
        print("   ReDoc:      http://localhost:5100/api/redoc/")
        print("\n📝 Don't forget to:")
        print("- Update your .env file with correct database credentials")
        print("- Ensure PostgreSQL is running")
    else:
        print("\n❌ Setup failed. Please try manual setup or check the error messages above.")
        print("Run with choice '3' for manual instructions.")

def print_manual_instructions():
    """Print manual setup instructions"""
    print("\n📋 Manual Setup Instructions")
    print("=" * 40)
    print("\n1. Create virtual environment (optional but recommended):")
    if os.name == 'nt':
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate")
    else:
        print("   python -m venv venv")
        print("   source venv/bin/activate")
    
    print("\n2. Install dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n3. Create migrations:")
    print("   python manage.py makemigrations users")
    print("   python manage.py makemigrations requests")
    
    print("\n4. Run migrations:")
    print("   python manage.py migrate")
    
    print("\n5. Create superuser (optional):")
    print("   python manage.py createsuperuser")
    
    print("\n6. Start server:")
    print("   python manage.py runserver 5100")
    
    print("\n📚 Documentation URLs:")
    print("   http://localhost:5100/api/docs/")
    print("   http://localhost:5100/api/redoc/")

if __name__ == "__main__":
    main()