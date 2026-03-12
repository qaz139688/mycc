$ErrorActionPreference = 'Stop'

$taskName = 'ClaudeCode-SettingsMergeFix'
$scriptPath = 'C:\Users\Cc\.claude\fix-settings.ps1'

if (-not (Test-Path $scriptPath)) {
  throw "Fix script not found: $scriptPath"
}

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

$triggerAtLogon = New-ScheduledTaskTrigger -AtLogOn

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $triggerAtLogon -Settings $settings -Description 'Repair Claude settings.json after cc-switch reset with baseline+merge strategy.' -Force | Out-Null

Write-Output "OK: Scheduled task '$taskName' is registered."
