# IP Blacklist Remover - Automation Script for Windows
# This script runs the full scan and diagnosis suite.

$ProjectDir = Get-Location
$PythonPath = "python" # Ensure python is in your PATH

Write-Host "--- IP Blacklist Remover: Scheduled Scan ---" -ForegroundColor Cyan
Write-Host "Running scan at: $(Get-Date)" -ForegroundColor Gray

# Run the full scan
& $PythonPath "$ProjectDir\main.py" full

Write-Host "--- Scan Finished ---" -ForegroundColor Green

<# 
HOW TO AUTOMATE WITH WINDOWS TASK SCHEDULER:
1. Open 'Task Scheduler'.
2. Click 'Create Basic Task'.
3. Name: 'IP Blacklist Scan'.
4. Trigger: 'Daily' (e.g., 9:00 AM).
5. Action: 'Start a program'.
6. Program/script: 'powershell.exe'
7. Add arguments: '-ExecutionPolicy Bypass -File "C:\Path\To\Your\Project\scheduler.ps1"'
8. Finish.
#>