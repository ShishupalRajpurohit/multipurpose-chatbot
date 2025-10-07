"""
Database testing and initialization script
Run this after setting up your PostgreSQL database
"""

from database.database import engine, init_db, test_connection
from sqlalchemy import text, inspect


def check_tables():
    """Check which tables exist in the database"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n📋 Existing tables:")
    if tables:
        for table in tables:
            print(f"  ✓ {table}")
    else:
        print("  (No tables found)")
    
    return tables


def test_postgresql_version():
    """Test PostgreSQL connection and get version"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"\n✅ PostgreSQL connected successfully!")
            print(f"📊 Version: {version[:50]}...")
            return True
    except Exception as e:
        print(f"\n❌ PostgreSQL connection error:")
        print(f"   {str(e)}")
        return False


def create_test_user():
    """Create a test user to verify database works"""
    from database.models import User
    from database.database import get_db_session
    from werkzeug.security import generate_password_hash
    
    db = get_db_session()
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter_by(username='testuser').first()
        if existing_user:
            print("\n⚠️ Test user already exists, skipping...")
            return
        
        # Create test user
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('testpassword123')
        )
        db.add(test_user)
        db.commit()
        print("\n✅ Test user created successfully!")
        print(f"   Username: testuser")
        print(f"   Email: test@example.com")
        print(f"   Password: testpassword123")
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error creating test user: {e}")
    finally:
        db.close()


def main():
    """Main testing workflow"""
    print("="*60)
    print("🧪 MULTIPURPOSE CHATBOT - DATABASE TEST")
    print("="*60)
    
    # Step 1: Test connection
    print("\n[1/4] Testing PostgreSQL connection...")
    if not test_postgresql_version():
        print("\n⚠️ Fix your database connection and try again")
        print("   Check your .env file and PostgreSQL service")
        return
    
    # Step 2: Check existing tables
    print("\n[2/4] Checking existing tables...")
    existing_tables = check_tables()
    
    # Step 3: Create/update tables
    print("\n[3/4] Creating/updating database schema...")
    try:
        init_db()
        print("   ✅ All tables created/updated successfully")
    except Exception as e:
        print(f"   ❌ Error creating tables: {e}")
        return
    
    # Step 4: Verify tables were created
    print("\n[4/4] Verifying tables...")
    new_tables = check_tables()
    
    expected_tables = [
        'users', 'chats', 'messages', 'files',
        'embeddings_metadata', 'usage_logs', 'feedback'
    ]
    
    missing_tables = [t for t in expected_tables if t not in new_tables]
    if missing_tables:
        print(f"\n⚠️ Missing tables: {', '.join(missing_tables)}")
    else:
        print("\n✅ All required tables exist!")
    
    # Optional: Create test user
    print("\n[BONUS] Creating test user...")
    try:
        create_test_user()
    except ImportError:
        print("⚠️ Skipping test user (werkzeug not installed)")
        print("   Run: poetry add werkzeug")
    
    print("\n" + "="*60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("="*60)
    print("\n📝 Next steps:")
    print("   1. Update your .env file with correct credentials")
    print("   2. Run: python run.py (to start Flask)")
    print("   3. Run: chainlit run chainlit_app/app.py (to start chat)")
    print("\n")


if __name__ == "__main__":
    main()