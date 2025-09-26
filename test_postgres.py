#!/usr/bin/env python3
"""
Quick PostgreSQL connection test
"""

def test_postgres():
    """Test PostgreSQL connection"""
    try:
        import psycopg2
        from decouple import config
        
        # Test connection to requests_db
        conn = psycopg2.connect(
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PORT', default='5432'),
            user=config('DB_USER', default='postgres'),
            password=config('DB_PASSWORD', default='root'),
            database=config('DB_NAME', default='requests_db')
        )
        conn.close()
        print("✅ PostgreSQL connection to requests_db successful!")
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed")
        return False
    except Exception as e:
        if "does not exist" in str(e):
            print("❌ Database 'requests_db' does not exist")
            print("💡 Run: python setup_postgres.py")
        else:
            print(f"❌ PostgreSQL connection failed: {e}")
        return False

if __name__ == "__main__":
    test_postgres()