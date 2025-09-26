#!/usr/bin/env python3
"""
Check if API documentation generates without warnings
"""

import os
import sys
import subprocess
import tempfile

def check_schema_generation():
    """Test schema generation for warnings"""
    print("🔍 Checking API schema generation for warnings...")
    
    try:
        # Generate schema and capture output
        result = subprocess.run([
            sys.executable, 'manage.py', 'spectacular', '--color', '--file', 'schema.yml'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Schema generated successfully!")
            
            # Check for warnings in stderr
            if result.stderr:
                warning_lines = [line for line in result.stderr.split('\n') if 'Warning' in line]
                if warning_lines:
                    print(f"⚠️ Found {len(warning_lines)} warnings:")
                    for warning in warning_lines[:5]:  # Show first 5 warnings
                        print(f"   {warning}")
                    if len(warning_lines) > 5:
                        print(f"   ... and {len(warning_lines) - 5} more warnings")
                else:
                    print("✅ No warnings found!")
            else:
                print("✅ No warnings found!")
            
            # Clean up generated file
            if os.path.exists('schema.yml'):
                os.remove('schema.yml')
                
            return len(warning_lines) if result.stderr else 0
            
        else:
            print(f"❌ Schema generation failed: {result.stderr}")
            return -1
            
    except subprocess.TimeoutExpired:
        print("❌ Schema generation timed out")
        return -1
    except Exception as e:
        print(f"❌ Error checking schema: {e}")
        return -1

def main():
    print("📋 API Documentation Warning Checker")
    print("=" * 45)
    
    # Check if we're using SQLite settings for testing
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_sqlite')
    
    warning_count = check_schema_generation()
    
    if warning_count == 0:
        print("\n🎉 All warnings have been resolved!")
        print("Your API documentation is clean and professional.")
    elif warning_count > 0:
        print(f"\n⚠️ Found {warning_count} warnings.")
        print("These are cosmetic issues and won't affect functionality.")
    else:
        print("\n❌ Could not check for warnings due to errors.")
    
    print("\n💡 To see the documentation:")
    print("   Start server: python manage.py runserver 5100")
    print("   Visit: http://localhost:5100/api/docs/")

if __name__ == "__main__":
    main()