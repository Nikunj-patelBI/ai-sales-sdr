# Schedule the daily sales pipeline to run every morning via Windows Task Scheduler.
#
# Run this ONCE (in an elevated PowerShell) to register the task:
#     powershell -ExecutionPolicy Bypass -File scripts\schedule_daily.ps1
#
# To remove the task later:
#     Unregister-ScheduledTask -TaskName "AnalyticsGearSalesPipeline" -Confirm:$false

$ErrorActionPreference = "Stop"

# --- Config ---
$TaskName  = "AnalyticsGearSalesPipeline"
$ProjectDir = "C:\analyticsgear\sales_pipeline"
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$RunTime   = "08:00"   # 8 AM daily

# --- Build the action: run the daily pipeline module ---
$action = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "-m src.pipeline.daily_runner" `
    -WorkingDirectory $ProjectDir

# --- Trigger: every day at $RunTime ---
$trigger = New-ScheduledTaskTrigger -Daily -At $RunTime

# --- Settings: wake to run, retry on failure, don't stop if on battery ---
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries `
    -RestartCount 2 `
    -RestartInterval (New-TimeSpan -Minutes 5)

# --- Register (runs as the current user) ---
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Runs the AnalyticsGear AI sales pipeline daily: loads new leads, scores them, drafts emails, writes the daily report." `
    -Force

Write-Host ""
Write-Host "Scheduled '$TaskName' to run daily at $RunTime." -ForegroundColor Green
Write-Host "Test it now with:  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host "Check status with: Get-ScheduledTask -TaskName '$TaskName'"
