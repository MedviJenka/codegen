# PowerShell script to set up and run the Python application in a virtual environment

# Ensure PowerShell allows execution of this script for the current session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Get the script directory dynamically (so it works for any user)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $scriptDir "venv"
$pythonScript = Join-Path $scriptDir "main.py"
$requirementsFile = Join-Path $scriptDir "requirements.txt"

# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed. Please install Python and try again." -ForegroundColor Red
    exit 1
}

# Create and activate virtual environment only if it doesn't exist
if (-Not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    py -m venv $venvPath
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
& $activateScript

# Install dependencies from requirements.txt if it exists
if (Test-Path $requirementsFile) {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Green
    pip install -r $requirementsFile
} else {
    Write-Host "No requirements.txt found. Skipping dependency installation." -ForegroundColor Yellow
}

# Check if Playwright is installed, install it if necessary
$playwrightInstalled = pip show playwright -q
if (-not $playwrightInstalled) {
    Write-Host "Playwright not found. Installing Playwright..." -ForegroundColor Yellow
    pip install playwright
    Write-Host "Installing Playwright browsers..." -ForegroundColor Green
    playwright install
} else {
    Write-Host "Playwright is already installed." -ForegroundColor Green
}

# Run the Python script
Write-Host "Running the Python script: $pythonScript" -ForegroundColor Magenta
python $pythonScript
