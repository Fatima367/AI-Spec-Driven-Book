#!/bin/bash
set -e  # Exit on any error

# Upgrade pip
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Optional: Run any additional build steps here
echo "Backend dependencies installed successfully"