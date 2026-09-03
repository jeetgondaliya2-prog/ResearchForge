# ResearchForge AI — Start Both Servers
# Run this script from the project root:
#   powershell -ExecutionPolicy Bypass -File start.ps1

Write-Host ""
Write-Host "  ⚡ ResearchForge AI — Starting Servers" -ForegroundColor Magenta
Write-Host "  ========================================" -ForegroundColor DarkGray
Write-Host ""

# --- Start FastAPI backend in a new window ---
Write-Host "  [1/2] Starting FastAPI backend on http://127.0.0.1:8000 ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$PSScriptRoot'; Write-Host '  [Backend] Starting...' -ForegroundColor Cyan; python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"
)

Start-Sleep -Seconds 2

# --- Start Vite frontend in a new window ---
Write-Host "  [2/2] Starting React frontend on http://localhost:5173 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$PSScriptRoot\frontend'; Write-Host '  [Frontend] Starting...' -ForegroundColor Green; npm run dev"
)

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "  ✅ Both servers are starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend  →  http://localhost:5173" -ForegroundColor Yellow
Write-Host "  Backend   →  http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "  API Docs  →  http://127.0.0.1:8000/docs" -ForegroundColor DarkYellow
Write-Host ""
