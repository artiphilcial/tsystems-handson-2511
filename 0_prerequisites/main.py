import sys


def test_imports():
    """Test if all required packages are installed correctly."""
    print("=" * 60)
    print("Testing Prerequisites Installation")
    print("=" * 60)
    
    # Check Python version
    print(f"\n✓ Python version: {sys.version}")
    
    required_packages = [
        ("ibm_watsonx_ai", "IBM watsonx.ai SDK"),
        ("dotenv", "python-dotenv"),
        ("streamlit", "Streamlit"),
        ("pydantic", "Pydantic"),
        ("requests", "Requests"),
    ]
    
    all_passed = True
    
    for package_name, display_name in required_packages:
        try:
            __import__(package_name)
            print(f"✓ {display_name} is installed")
        except ImportError:
            print(f"✗ {display_name} is NOT installed")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("SUCCESS! All prerequisites are installed correctly.")
        print("You're ready to proceed with the hands-on lab!")
    else:
        print("FAILED! Some packages are missing.")
        print("Please run: uv sync")
    print("=" * 60)
    
    return all_passed


def main():
    print("Hello, this will test if all pre-requisites have been installed correctly!")
    print("\nRunning installation verification...\n")
    
    success = test_imports()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
