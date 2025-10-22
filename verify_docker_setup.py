#!/usr/bin/env python3
"""Verify Docker setup and configuration."""
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False

def main():
    """Run Docker setup verification."""
    print("🐳 Docker Setup Verification")
    print("=" * 50)
    
    all_good = True
    
    # Check Docker files
    print("\n📁 Checking Docker files...")
    all_good &= check_file_exists("Dockerfile", "Dockerfile")
    all_good &= check_file_exists("docker-compose.yml", "Docker Compose (production)")
    all_good &= check_file_exists("docker-compose.dev.yml", "Docker Compose (development)")
    all_good &= check_file_exists(".dockerignore", "Docker ignore file")
    
    # Check documentation
    print("\n📚 Checking documentation...")
    all_good &= check_file_exists("DOCKER.md", "Docker deployment guide")
    all_good &= check_file_exists("DOCKER_SETUP.md", "Docker setup summary")
    
    # Check scripts
    print("\n📜 Checking build scripts...")
    all_good &= check_file_exists("docker-build.bat", "Windows build script")
    all_good &= check_file_exists("docker-build.sh", "Linux/Mac build script")
    
    # Check configuration
    print("\n⚙️  Checking configuration files...")
    all_good &= check_file_exists(".env.example", "Environment example file")
    all_good &= check_file_exists("requirements.txt", "Python requirements")
    
    # Check application files
    print("\n🎯 Checking application files...")
    all_good &= check_file_exists("app.py", "Main application")
    all_good &= check_file_exists("src/backend/database/db_manager.py", "Database manager")
    all_good &= check_file_exists("src/backend/database/schema.sql", "Database schema")
    
    # Check app.py for environment variable support
    print("\n🔍 Checking app.py modifications...")
    try:
        with open("app.py", "r") as f:
            content = f.read()
            if "os.getenv('DB_PATH'" in content:
                print("✅ app.py: Environment variable support added")
            else:
                print("❌ app.py: Missing environment variable support")
                all_good = False
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        all_good = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("✅ All Docker files are in place!")
        print("\n🚀 Ready to build and deploy:")
        print("   Windows: docker-build.bat")
        print("   Linux/Mac: ./docker-build.sh")
        print("   Or: docker-compose up -d")
        return 0
    else:
        print("❌ Some files are missing. Please review above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
