# Prerequisites for the Hands-on Lab

## Required Software

### Code Editor
- **VS Code** (recommended) or any similar code editor
- [Download VS Code](https://code.visualstudio.com/)

### Python
- **Python 3.12**

> **Note:** You don't need to install Python manually! UV will automatically download Python 3.12 when you run the lab modules if it's not already on your system.

## Package Manager Installation

### UV Package Manager

UV is a fast Python package manager that we'll use throughout this lab. It will automatically manage Python versions for you.

#### macOS

**Option 1: Install via Homebrew (Recommended)**

First, install Homebrew if you don't have it:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install UV:
```bash
brew install uv
```

**Option 2: Standalone Installation**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows

**Standalone Installation**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Linux

**Standalone Installation**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Verification

After installing UV, verify the installation:

```bash
# Check UV installation
uv --version
```

## Testing Your Setup

Once UV is installed run the following commands to verify everything is working correctly:

### Step 1: Install Dependencies

```bash
cd 0_prerequisites
uv sync
```

This command will:
- Automatically download Python 3.12 if not already installed
- Install all required packages (ibm-watsonx-ai, python-dotenv, streamlit)
- Create a virtual environment in `.venv`

### Step 2: Run the Verification Script

```bash
uv run main.py
```

This will test that all dependencies are installed correctly. You should see output like:

```
Hello, this will test if all pre-requisites have been installed correctly!!

Running installation verification...

============================================================
Testing Prerequisites Installation
============================================================

✓ Python version: 3.12.x
✓ IBM watsonx.ai SDK is installed
✓ python-dotenv is installed
✓ Streamlit is installed
✓ Pydantic is installed
✓ Requests is installed

============================================================
SUCCESS! All prerequisites are installed correctly.
You're ready to proceed with the hands-on lab!
============================================================
```

If you see any `✗` marks or errors, run `uv sync` again to ensure all packages are installed.

## Next Steps

Once you have completed the prerequisites and verified your setup, proceed to the first lab module.
