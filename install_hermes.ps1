Write-Host "=== Hermes Agent Windows Installer (UV Method) ===" -ForegroundColor Cyan

# 1. Ensure UV is installed
Write-Host "`n[1/6] Checking for UV..."
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "UV not found. Installing UV..." -ForegroundColor Yellow
    irm https://astral.sh/uv/install.ps1 | powershell -
} else {
    Write-Host "UV already installed." -ForegroundColor Green
}

# 2. Create Hermes virtual environment
Write-Host "`n[2/6] Creating Hermes virtual environment..."
$envPath = "$env:USERPROFILE\hermes-env"
uv venv $envPath

# 3. Activate environment for this script
Write-Host "`n[3/6] Activating environment..."
$env:VIRTUAL_ENV = $envPath
$env:PATH = "$envPath\Scripts;$env:PATH"

# 4. Install Hermes Agent inside UV environment
Write-Host "`n[4/6] Installing Hermes Agent..."
uv pip install hermes-agent

# 5. Add Hermes to PATH globally (WindowsApps)
Write-Host "`n[5/6] Making Hermes globally accessible..."
$target = "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\hermes.cmd"
$source = "$envPath\Scripts\hermes.exe"

if (Test-Path $source) {
    Copy-Item $source $target -Force
    Write-Host "Hermes is now globally available as 'hermes'." -ForegroundColor Green
} else {
    Write-Host "ERROR: hermes.exe not found inside environment." -ForegroundColor Red
}

# 6. Final test
Write-Host "`n[6/6] Testing Hermes installation..."
try {
    hermes --version
    Write-Host "`nHermes installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "`nHermes installation completed, but command not recognized." -ForegroundColor Yellow
    Write-Host "Try restarting your terminal."
}

Write-Host "`n=== Installation Complete ===" -ForegroundColor Cyan
