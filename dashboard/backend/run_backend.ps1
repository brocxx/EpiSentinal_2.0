# Run backend: installs requirements (if needed) and starts uvicorn
param(
    [switch]$Install = $false
)

$here = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $here

if ($Install) {
    Write-Host "Installing requirements..."
    pip install -r requirements.txt
}

Write-Host "Starting uvicorn on port 8000 (non-blocking)..."
# Start uvicorn in a new window so the script can return
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "main:app --reload --port 8000" -WorkingDirectory $here
Write-Host "uvicorn started. Visit http://127.0.0.1:8000/docs to verify endpoints."