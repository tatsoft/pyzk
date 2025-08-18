# Activate the virtual environment
$venvPath = Join-Path $PSScriptRoot 'venv\Scripts\Activate.ps1'
if (Test-Path $venvPath) {
	& $venvPath
} else {
	Write-Host 'Python virtual environment not found!'
	exit 1
}


# Start backend (FastAPI) from project root using module syntax
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn attendance_api.main:app --host 0.0.0.0 --port 8000"

# Wait a few seconds to let backend start
Start-Sleep -Seconds 3

# Start frontend (Vite dev server)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
