# Start backend (install deps) and run test POST to /predict
$here = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $here

Write-Host "Installing requirements (may take a while)..."
pip install -r requirements.txt

Write-Host "Starting uvicorn in background..."
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "main:app --reload --port 8000" -WorkingDirectory $here

Write-Host "Waiting 4 seconds for server to start..."
Start-Sleep -Seconds 4

Write-Host "Running test_predict.py..."
python test_predict.py
