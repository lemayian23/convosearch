#!/usr/bin/env python3
"""
Quick installation test to verify all dependencies work
"""
import sys
import importlib


def test_import(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: {e}")
        return False


def main():
    print("Testing ConvoSearch dependencies...")
    print("=" * 40)

    required_modules = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "chromadb",
        "langchain",
        "openai",
        "psycopg2",
        "dotenv",
        "sklearn",
        "numpy",
        "requests",
        "aiofiles",
        "jinja2"
    ]

    results = []
    for module in required_modules:
        results.append(test_import(module))

    print("=" * 40)
    if all(results):
        print("🎉 All dependencies installed successfully!")
        print("\nNext: Run 'make build' to build the Docker containers")
    else:
        print("❌ Some dependencies failed. Please check requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()