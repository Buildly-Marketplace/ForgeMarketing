"""
Simple smoke test runner without pytest.

Provides basic smoke tests that can run without pytest installed.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_environment_variables():
    """Check that required environment variables are set."""
    print("Testing environment variables...")
    
    required_vars = ["FLASK_ENV", "OLLAMA_HOST"]
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            print(f"  ❌ Missing: {var}")
        else:
            print(f"  ✓ {var}={os.getenv(var)}")
    
    if missing:
        print(f"\n⚠️  Missing required environment variables: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in the values.")
        return False
    
    return True


def test_required_files():
    """Check that required files exist."""
    print("\nTesting required files...")
    
    required_files = [
        "BUILDLY.yaml",
        "LICENSE.md",
        "SUPPORT.md",
        "requirements.txt"
    ]
    
    missing = []
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for filename in required_files:
        filepath = os.path.join(project_root, filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename}")
        else:
            missing.append(filename)
            print(f"  ❌ Missing: {filename}")
    
    if missing:
        print(f"\n⚠️  Missing required files: {', '.join(missing)}")
        return False
    
    return True


def test_documentation():
    """Check that documentation exists."""
    print("\nTesting documentation...")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    devdocs_dir = os.path.join(project_root, "devdocs")
    required_docs = ["SETUP.md", "OPERATIONS.md", "REFERENCE.md"]
    
    missing = []
    for doc in required_docs:
        doc_path = os.path.join(devdocs_dir, doc)
        if os.path.exists(doc_path):
            print(f"  ✓ devdocs/{doc}")
        else:
            missing.append(doc)
            print(f"  ❌ Missing: devdocs/{doc}")
    
    if missing:
        print(f"\n⚠️  Missing documentation files: {', '.join(missing)}")
        return False
    
    return True


def test_deployment_files():
    """Check that deployment files exist."""
    print("\nTesting deployment files...")
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ops_dir = os.path.join(project_root, "ops")
    deployment_files = ["Dockerfile", "docker-compose.yml"]
    
    missing = []
    for file in deployment_files:
        file_path = os.path.join(ops_dir, file)
        if os.path.exists(file_path):
            print(f"  ✓ ops/{file}")
        else:
            missing.append(file)
            print(f"  ❌ Missing: ops/{file}")
    
    if missing:
        print(f"\n⚠️  Missing deployment files: {', '.join(missing)}")
        return False
    
    return True


def main():
    """Run all smoke tests."""
    print("=" * 60)
    print("ForgeMark Smoke Tests")
    print("=" * 60)
    
    tests = [
        test_environment_variables,
        test_required_files,
        test_documentation,
        test_deployment_files
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ All {total} smoke tests passed!")
        print("\nNext steps:")
        print("  1. Start Ollama: ollama serve")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Run the app: python -m automation.run_unified_outreach")
        return 0
    else:
        print(f"❌ {total - passed} out of {total} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
