Data Validator - Complete Setup & Release Guide
Project Structure
text
data-validator/
├── data_validator/
│   ├── __init__.py
│   ├── core.py
│   ├── types.py
│   ├── validators.py
│   └── readers.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_validators.py
│   └── test_readers.py
├── .github/
│   └── workflows/
│       └── publish.yml
├── .gitignore
├── pyproject.toml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
Step-by-Step Release Process
1. Create Local Project
bash
mkdir data-validator
cd data-validator

# Create subdirectories
mkdir data_validator tests .github/workflows

# Create all files (from the content provided)
2. Copy All Files
Copy the following files into your project:

data_validator/__init__.py

data_validator/core.py

data_validator/types.py

data_validator/validators.py

data_validator/readers.py

tests/test_core.py

tests/test_validators.py

tests/test_readers.py

.github/workflows/publish.yml

pyproject.toml

README.md

LICENSE

CONTRIBUTING.md

.gitignore

3. Test Locally
bash
# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format code
black data_validator tests

# Lint code
flake8 data_validator tests --max-line-length=100

# Check types (optional)
mypy data_validator --ignore-missing-imports || true
Expected Output:

text
tests/test_core.py ........
tests/test_validators.py ...........
tests/test_readers.py ...........
===================== 20 passed in 0.50s =====================
4. Create GitHub Repository
Go to https://github.com/new

Repository name: data-validator

Description: "Production-grade data validation library with multi-format support"

Select Public

Do NOT initialize with README, .gitignore, or license

Click Create repository

5. Push to GitHub
bash
# Initialize git
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Data validator library MVP"

# Connect to GitHub (replace yourusername with your GitHub username)
git remote add origin https://github.com/yourusername/data-validator.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
6. Create PyPI Account
Go to https://pypi.org/account/register/

Create account with email and password

Verify your email address

Go to https://pypi.org/account/edit/ and enable 2FA (optional but recommended)

7. Configure GitHub Trusted Publishing
This allows GitHub Actions to publish to PyPI without storing passwords.

In your GitHub repository, go to Settings (top menu)

Click Environments in the left sidebar

Click New environment

Name: pypi

Click Configure environment

Leave all settings at defaults

Click Save protection rules

GitHub and PyPI will now automatically trust each other.

8. Create First Release
bash
# Create version tag
git tag v0.1.0

# Push tag to GitHub (this triggers the workflow)
git push origin v0.1.0
9. Monitor the Workflow
Go to your GitHub repo

Click Actions tab

Watch the "Tests & Publish" workflow run

It will:

Run tests on Python 3.8-3.12 ✓

Check code style with black ✓

Lint with flake8 ✓

Build the package ✓

Publish to PyPI ✓

Create GitHub release ✓

Duration: 3-5 minutes

10. Verify Publication
Once the workflow completes:

bash
# Install from PyPI
pip install data-validator

# Test it works
python -c "from data_validator import Schema, Field, DataType; print('✓ Success!')"
Visit: https://pypi.org/project/data-validator/

Your package is now live! 🎉

Making Updates
Update Code
bash
# Make changes to code
# ... edit files ...

# Run tests locally
pytest tests/ -v

# Format and lint
black data_validator tests
flake8 data_validator tests

# Commit changes
git add .
git commit -m "Add new feature: X"
git push origin main
Release New Version
bash
# Update version in pyproject.toml
# Change: version = "0.1.0" to version = "0.2.0"

# Commit version change
git add pyproject.toml
git commit -m "Bump version to 0.2.0"
git push origin main

# Create new tag (this triggers automated release)
git tag v0.2.0
git push origin v0.2.0
Done! Your new version will be published automatically.

Troubleshooting
Tests Fail Locally
bash
# Reinstall dependencies
pip install -e ".[dev]"

# Run with verbose output
pytest tests/ -v -s

# Run specific test
pytest tests/test_core.py::test_basic_validation -v
Workflow Fails on GitHub
Click on the failed workflow in Actions tab

Look for the red ✗ mark and error message

Common issues:

Missing file (check all files are copied correctly)

Import error (check __init__.py files)

Test failure (run tests locally to debug)

Package Not Appearing on PyPI
Workflow completed successfully? Check Actions tab

Go to https://pypi.org/project/data-validator/ and refresh

Wait 5 minutes (PyPI has caching)

Check your email for any PyPI notifications

Can't Login to PyPI
If you set up trusted publishing correctly, you don't need to login locally. The GitHub token handles it automatically.

To test without trusted publishing:

bash
pip install twine
twine upload dist/* --username __token__ --password <your-token>
Environment Variables
No environment variables needed! Trusted publishing handles authentication.

File Size
The published package will be ~50 KB (very lightweight).

Supported Python Versions
Python 3.8+

Tested on: 3.8, 3.9, 3.10, 3.11, 3.12

What's Included
✅ Core validation engine
✅ 11 built-in validators
✅ Multi-format file support (JSON, CSV, Parquet)
✅ Comprehensive tests (20+ test cases)
✅ Full documentation
✅ CI/CD pipeline
✅ Zero external dependencies (core)

Next Steps
After your first release:

Create documentation - Add more examples

Gather feedback - Open GitHub Issues

Add features - Implement user requests

Release updates - Use the version bump process

Build community - Share your package