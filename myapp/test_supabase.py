#!/usr/bin/env python
"""
Test Supabase database connection
Run this script to test if your Supabase database is accessible
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def test_supabase_connection():
    """Test direct connection to Supabase"""
    
    # Get database URL from environment or use Neon default
    database_url = os.environ.get('DATABASE_URL', "postgresql://neondb_owner:npg_iV1lydOfzuD9@ep-fancy-lake-a181h6u2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
    
    print("🔍 Testing PostgreSQL Database Connection...")
    print(f"Database URL: {database_url}")
    print("-" * 50)
    
    try:
        # Parse the database URL
        parsed = urlparse(database_url)
        
        print(f"Host: {parsed.hostname}")
        print(f"Port: {parsed.port}")
        print(f"Database: {parsed.path[1:]}")  # Remove leading '/'
        print(f"Username: {parsed.username}")
        print("-" * 50)
        
        # Test connection
        print("🔗 Attempting to connect...")
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            sslmode='require',
            connect_timeout=10
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        
        print("✅ SUCCESS! Connected to Supabase PostgreSQL")
        print(f"Database Version: {db_version}")
        
        # Test if we can create a simple table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        cursor.execute("""
            INSERT INTO connection_test (test_message) 
            VALUES ('Connection test successful');
        """)
        
        conn.commit()
        print("✅ Database write test successful")
        
        # Clean up
        cursor.execute("DROP TABLE IF EXISTS connection_test;")
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("✅ All tests passed! Supabase is working correctly.")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection Error: {e}")
        print("\n💡 Possible solutions:")
        print("1. Check your internet connection")
        print("2. Verify Supabase credentials are correct")
        print("3. Check if your IP is allowed in Supabase settings")
        print("4. Try using a VPN if your network blocks external databases")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_django_database():
    """Test Django database configuration"""
    print("\n🔍 Testing Django Database Configuration...")
    print("-" * 50)
    
    try:
        # Add Django project to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        # Configure Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
        
        import django
        django.setup()
        
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        # Test database connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result[0] == 1:
            print("✅ Django database connection successful!")
            
            # Try to run migrations
            print("🔄 Running database migrations...")
            execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
            print("✅ Migrations completed successfully!")
            
            return True
        else:
            print("❌ Django database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Django database error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Supabase Database Connection Test")
    print("=" * 50)
    
    # Test direct connection
    direct_success = test_supabase_connection()
    
    # Test Django connection
    django_success = test_django_database()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"Direct Connection: {'✅ PASS' if direct_success else '❌ FAIL'}")
    print(f"Django Connection: {'✅ PASS' if django_success else '❌ FAIL'}")
    
    if direct_success and django_success:
        print("\n🎉 All tests passed! Your Supabase database is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above and try the suggested solutions.")
