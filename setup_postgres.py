#!/usr/bin/env python3
"""
PostgreSQL Database Setup Script
Creates the database and runs migrations
"""

import os
import sys
import subprocess
from decouple import config

def create_database():
    """Create the requests_db database"""
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        print("🔄 Connecting to PostgreSQL...")
        
        # Connect to the default postgres database first
        conn = psycopg2.connect(
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PORT', default='5432'),
            user=config('DB_USER', default='postgres'),
            password=config('DB_PASSWORD', default='root'),
            database='postgres'  # Connect to default database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='requests_db'")
        exists = cursor.fetchone()
        
        if not exists:
            print("🔄 Creating database 'requests_db'...")
            cursor.execute("CREATE DATABASE requests_db")
            print("✅ Database 'requests_db' created successfully!")
        else:
            print("✅ Database 'requests_db' already exists!")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'], check=True)
            print("✅ psycopg2-binary installed successfully!")
            return create_database()  # Retry after installation
        except subprocess.CalledProcessError:
            print("❌ Failed to install psycopg2-binary")
            return False
            
    except psycopg2.OperationalError as e:
        if "password authentication failed" in str(e):
            print("❌ Password authentication failed!")
            print("💡 Please set the PostgreSQL password for user 'postgres' to 'root':")
            print("   1. Connect to PostgreSQL as superuser")
            print("   2. Run: ALTER USER postgres PASSWORD 'root';")
        elif "could not connect to server" in str(e):
            print("❌ Could not connect to PostgreSQL server!")
            print("💡 Please ensure PostgreSQL is running:")
            print("   - Windows: Check Services or start PostgreSQL manually")
            print("   - Linux/Mac: sudo systemctl start postgresql")
        else:
            print(f"❌ PostgreSQL connection error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def run_migrations():
    """Run Django migrations"""
    try:
        print("\n🔄 Creating Django migrations...")
        
        # Make migrations for users app
        result = subprocess.run([
            sys.executable, 'manage.py', 'makemigrations', 'users'
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ User migrations created")
        else:
            print("⚠️ User migrations may already exist")
        
        # Make migrations for requests app
        result = subprocess.run([
            sys.executable, 'manage.py', 'makemigrations', 'requests'
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ Request migrations created")
        else:
            print("⚠️ Request migrations may already exist")
        
        # Apply migrations
        print("🔄 Applying migrations...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate'
        ], capture_output=True, text=True, check=True)
        
        print("✅ All migrations applied successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def test_connection():
    """Test the final database connection"""
    try:
        print("\n🔄 Testing database connection...")
        result = subprocess.run([
            sys.executable, 'manage.py', 'check', '--database', 'default'
        ], capture_output=True, text=True, check=True)
        
        print("✅ Database connection successful!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Database check failed: {e}")
        return False

def main():
    print("🐘 PostgreSQL Database Setup")
    print("=" * 40)
    
    # Step 1: Create database
    if not create_database():
        print("\n❌ Database creation failed. Please check PostgreSQL setup.")
        print("\n🔧 Manual setup steps:")
        print("1. Ensure PostgreSQL is running")
        print("2. Connect as superuser: psql -U postgres")
        print("3. Create database: CREATE DATABASE requests_db;")
        print("4. Set password: ALTER USER postgres PASSWORD 'root';")
        return False
    
    # Step 2: Run migrations
    if not run_migrations():
        print("\n❌ Migration failed. Please check the error messages above.")
        return False
    
    # Step 3: Test connection
    if not test_connection():
        print("\n❌ Final connection test failed.")
        return False
    
    print("\n🎉 PostgreSQL setup completed successfully!")
    print("\n🚀 You can now start the server:")
    print("   python manage.py runserver 5100")
    print("\n📚 API Documentation:")
    print("   http://localhost:5100/api/docs/")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💡 Alternative: Use SQLite for development:")
        print("   python manage.py runserver 5100 --settings=backend.settings_sqlite")
    
    input("\nPress Enter to continue...")