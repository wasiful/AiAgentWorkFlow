Write-Host "=== Hermes Full Environment Setup (Python + Tkinter + UV + Hermes) ===" -ForegroundColor Cyan

# -----------------------------
# 1. CHECK PYTHON
# -----------------------------
Write-Host "`n[1/8] Checking Python installation..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Installing Python 3.12..." -ForegroundColor Yellow

    winget install -e --id Python.Python.3.12

    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "ERROR: Python installation failed." -ForegroundColor Red
        exit
    }
} else {
    Write-Host "Python is installed." -ForegroundColor Green
}

# -----------------------------
# 2. CHECK TKINTER SUPPORT
# -----------------------------
Write-Host "`n[2/8] Checking Tkinter GUI support..."

$tkTest = python - << 'EOF'
import tkinter
print("OK")
EOF

if ($tkTest -match "OK") {
    Write-Host "Tkinter is available." -ForegroundColor Green
} else {
    Write-Host "ERROR: Tkinter is missing. Reinstall Python from python.org or Winget." -ForegroundColor Red
    exit
}

# -----------------------------
# 3. CHECK PIP
# -----------------------------
Write-Host "`n[3/8] Checking pip..."

try {
    python -m pip --version | Out-Null
    Write-Host "pip is installed." -ForegroundColor Green
} catch {
    Write-Host "pip missing. Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# -----------------------------
# 4. INSTALL PYTHON PACKAGES REQUIRED BY ui.py
# -----------------------------
Write-Host "`n[4/8] Installing required Python packages for ui.py..."

python -m pip install --upgrade pip setuptools wheel
python -m pip install subprocess.run 2>$null
python -m pip install tk 2>$null

Write-Host "Python GUI dependencies installed." -ForegroundColor Green

# -----------------------------
# 5. CHECK UV
# -----------------------------
Write-Host "`n[5/8] Checking UV package manager..."

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "UV not found. Installing UV..." -ForegroundColor Yellow
    irm https://astral.sh/uv/install.ps1 | powershell -
} else {
    Write-Host "UV is installed." -ForegroundColor Green
}

# -----------------------------
# 6. CHECK / CREATE HERMES ENV
# -----------------------------
Write-Host "`n[6/8] Checking Hermes virtual environment..."

$envPath = "$env:USERPROFILE\hermes-env"

if (-not (Test-Path $envPath)) {
    Write-Host "Hermes environment not found. Creating..." -ForegroundColor Yellow
    uv venv $envPath
} else {
    Write-Host "Hermes environment exists." -ForegroundColor Green
}

# -----------------------------
# 7. ACTIVATE ENV + INSTALL/UPDATE HERMES
# -----------------------------
Write-Host "`n[7/8] Activating environment and installing/updating Hermes..."

$env:VIRTUAL_ENV = $envPath
$env:PATH = "$envPath\Scripts;$env:PATH"

try {
    uv pip install --upgrade hermes-agent
    Write-Host "Hermes installed/updated successfully." -ForegroundColor Green
} catch {
    Write-Host "ERROR: Hermes installation failed." -ForegroundColor Red
    exit
}

# -----------------------------
# 8. REFRESH GLOBAL HERMES COMMAND
# -----------------------------
Write-Host "`n[8/8] Refreshing global Hermes command..."

$source = "$envPath\Scripts\hermes.exe"
$target = "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\hermes.cmd"

if (Test-Path $source) {
    Copy-Item $source $target -Force
    Write-Host "Global 'hermes' command refreshed." -ForegroundColor Green
} else {
    Write-Host "WARNING: hermes.exe missing in environment." -ForegroundColor Yellow
}

Write-Host "`n=== All prerequisites installed and Hermes is ready ===" -ForegroundColor Cyan

try {
    hermes --version
} catch {
    Write-Host "Hermes installed but terminal restart required." -ForegroundColor Yellow
}
