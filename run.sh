#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Exit on error
set -e

print_info "Starting setup process..."

# Step 1: Check if Python 3 is installed
print_info "Checking for Python 3 installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH."
    print_error "Please install Python 3.6 or higher from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python 3 found: $PYTHON_VERSION"

# Step 2: Create or verify local virtual environment
VENV_DIR=".venv"

if [ -d "$VENV_DIR" ]; then
    print_warning "Virtual environment already exists at $VENV_DIR"
else
    print_info "Creating virtual environment in $VENV_DIR..."
    if ! python3 -m venv "$VENV_DIR"; then
        print_error "Failed to create virtual environment."
        print_error "Make sure venv module is available: python3 -m venv"
        exit 1
    fi
    print_success "Virtual environment created successfully"
fi

# Step 3: Activate virtual environment
print_info "Activating virtual environment..."
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    print_error "Virtual environment activation script not found at $VENV_DIR/bin/activate"
    exit 1
fi

source "$VENV_DIR/bin/activate"
print_success "Virtual environment activated"

# Step 4: Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    print_info "Installing dependencies from requirements.txt..."
    if ! pip install --upgrade pip setuptools wheel > /dev/null 2>&1; then
        print_warning "Failed to upgrade pip tools, attempting to continue..."
    else
        print_success "pip tools upgraded"
    fi
    
    if ! pip install -r requirements.txt; then
        print_error "Failed to install dependencies from requirements.txt"
        print_error "Please check requirements.txt and ensure all packages are available"
        exit 1
    fi
    print_success "Dependencies installed successfully"
else
    print_warning "requirements.txt not found - skipping dependency installation"
fi

# Step 5: Run main.py
print_info "Launching application..."
if [ ! -f "main.py" ]; then
    print_error "main.py not found in the current directory"
    exit 1
fi

print_success "Setup complete! Running application..."
python3 main.py

# Deactivate virtual environment when the script exits
deactivate 2>/dev/null || true
print_info "Application closed. Virtual environment deactivated."
