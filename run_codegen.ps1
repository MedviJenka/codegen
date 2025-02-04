# Set PowerShell execution policy for this session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Get the script directory dynamically
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $scriptDir "venv"
$pythonScript = Join-Path $scriptDir "engine/codegen.py"
$requirementsFile = Join-Path $scriptDir "requirements.txt"

# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed. Please install Python and try again." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (-Not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    py -m venv $venvPath
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
& $activateScript

# Install dependencies if requirements.txt exists
if (Test-Path $requirementsFile) {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Green
    pip install -r $requirementsFile
} else {
    Write-Host "No requirements.txt found. Skipping dependency installation." -ForegroundColor Yellow
}

# Check and install Playwright if necessary
$playwrightInstalled = pip show playwright -q
if (-not $playwrightInstalled) {
    Write-Host "Playwright not found. Installing Playwright..." -ForegroundColor Yellow
    pip install playwright
    Write-Host "Installing Playwright browsers..." -ForegroundColor Green

} else {
    Write-Host "Playwright is already installed." -ForegroundColor Green
}

playwright install

# 🔥 Fix Module Import Error by Setting PYTHONPATH
$env:PYTHONPATH = $scriptDir

# Run the Python script
Write-Host "Running the Python script: $pythonScript" -ForegroundColor Magenta
python $pythonScript
