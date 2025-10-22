"""Quick test to verify all imports work correctly."""
import sys
import os

print("=" * 50)
print("Project Setup Verification")
print("=" * 50)
print()

# Test imports
errors = []

try:
    print("✓ Testing database imports...")
    from database.db_manager import DatabaseManager
    print("  - DatabaseManager imported successfully")
except Exception as e:
    errors.append(f"Database import error: {e}")
    print(f"  ✗ Error: {e}")

try:
    print("✓ Testing utils imports...")
    from utils.helpers import (
        get_status_color,
        get_status_emoji,
        validate_required_field
    )
    print("  - Helper functions imported successfully")
except Exception as e:
    errors.append(f"Utils import error: {e}")
    print(f"  ✗ Error: {e}")

try:
    print("✓ Testing pages imports...")
    from pages import (
        dashboard,
        handover_log,
        positions,
        operations,
        issues_alerts,
        market,
        comments
    )
    print("  - All page modules imported successfully")
except Exception as e:
    errors.append(f"Pages import error: {e}")
    print(f"  ✗ Error: {e}")

try:
    print("✓ Testing database initialization...")
    import tempfile
    fd, temp_db = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    db = DatabaseManager(temp_db)
    print("  - Database initialized successfully")
    
    # Test a simple operation
    log_id = db.create_handover_log("Test Trader", "2024-01-15", "Test notes")
    logs = db.get_all_handover_logs()
    
    if len(logs) == 1 and logs.iloc[0]['trader_name'] == "Test Trader":
        print("  - Database operations working correctly")
    else:
        errors.append("Database operation test failed")
        print("  ✗ Database operation test failed")
    
    # Cleanup
    os.unlink(temp_db)
except Exception as e:
    errors.append(f"Database initialization error: {e}")
    print(f"  ✗ Error: {e}")

print()
print("=" * 50)

if errors:
    print("❌ Setup verification completed with errors:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
else:
    print("✅ All checks passed! The project is ready to use.")
    print()
    print("To start the application, run:")
    print("  streamlit run app.py")
    print()
    print("Or use the quick start script:")
    print("  start.bat (Windows)")
    sys.exit(0)
