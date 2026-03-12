$ErrorActionPreference = 'Stop'

$claudeDir = 'C:\Users\Cc\.claude'
$settingsPath = Join-Path $claudeDir 'settings.json'
$baselinePath = Join-Path $claudeDir 'settings.baseline.json'
$installedPluginsPath = Join-Path $claudeDir 'plugins\installed_plugins.json'
$debugDir = Join-Path $claudeDir 'debug'
$logPath = Join-Path $debugDir 'fix-settings.log'
$lastGoodPath = Join-Path $claudeDir 'settings.last-good.json'

if (-not (Test-Path $debugDir)) {
  New-Item -Path $debugDir -ItemType Directory -Force | Out-Null
}

function Write-Log {
  param([string]$Message)
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [fix-settings] $Message"
  Add-Content -Path $logPath -Value $line
}

function Read-JsonObject {
  param([string]$Path)
  if (-not (Test-Path $Path)) { return $null }
  $raw = Get-Content -Path $Path -Raw -Encoding UTF8
  if ([string]::IsNullOrWhiteSpace($raw)) { return $null }
  return $raw | ConvertFrom-Json
}

function Set-Prop {
  param(
    [Parameter(Mandatory = $true)]$Object,
    [Parameter(Mandatory = $true)][string]$Name,
    [Parameter(Mandatory = $true)]$Value
  )
  if ($Object.PSObject.Properties.Name -contains $Name) {
    $Object.$Name = $Value
  } else {
    $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value
  }
}

try {
  if (-not (Test-Path $baselinePath)) {
    throw "Baseline file missing: $baselinePath"
  }

  $baseline = Read-JsonObject -Path $baselinePath
  if ($null -eq $baseline) {
    throw "Baseline file is empty or invalid JSON: $baselinePath"
  }

  $settings = $null
  $settingsRaw = $null
  $settingsParseOk = $false

  if (Test-Path $settingsPath) {
    $settingsRaw = Get-Content -Path $settingsPath -Raw -Encoding UTF8
    try {
      if (-not [string]::IsNullOrWhiteSpace($settingsRaw)) {
        $settings = $settingsRaw | ConvertFrom-Json
        $settingsParseOk = $true
      }
    } catch {
      Write-Log "settings.json parse failed, will fallback to last-good backup. Error=$($_.Exception.Message)"
    }
  }

  if ($settingsParseOk) {
    $looksReset = $false
    if ($baseline.PSObject.Properties.Name -contains 'enabledPlugins' -and -not ($settings.PSObject.Properties.Name -contains 'enabledPlugins')) {
      $looksReset = $true
    }
    if ($baseline.PSObject.Properties.Name -contains 'statusLine' -and -not ($settings.PSObject.Properties.Name -contains 'statusLine')) {
      $looksReset = $true
    }

    if ($looksReset) {
      Write-Log 'Detected reset-like settings.json (missing protected keys); will merge on top of last-good when available.'
      $lastGoodCandidate = Read-JsonObject -Path $lastGoodPath
      if ($null -ne $lastGoodCandidate) {
        if ($settings.PSObject.Properties.Name -contains 'model') {
          Set-Prop -Object $lastGoodCandidate -Name 'model' -Value $settings.model
        }
        if ($settings.PSObject.Properties.Name -contains 'env' -and $null -ne $settings.env) {
          Set-Prop -Object $lastGoodCandidate -Name 'env' -Value $settings.env
        }
        $settings = $lastGoodCandidate
      }
    }
  }

  if (-not $settingsParseOk -or $null -eq $settings) {
    $settings = Read-JsonObject -Path $lastGoodPath
    if ($null -eq $settings) {
      $settings = [pscustomobject]@{}
      Write-Log 'No valid current settings and no last-good backup; starting from empty object.'
    } else {
      Write-Log 'Recovered settings object from settings.last-good.json.'
    }
  }

  # 1) env: merge baseline protected keys into current env
  $envObj = $null
  if ($settings.PSObject.Properties.Name -contains 'env' -and $null -ne $settings.env) {
    $envObj = $settings.env
  } else {
    $envObj = [pscustomobject]@{}
  }

  if ($baseline.PSObject.Properties.Name -contains 'env' -and $null -ne $baseline.env) {
    foreach ($p in $baseline.env.PSObject.Properties) {
      Set-Prop -Object $envObj -Name $p.Name -Value $p.Value
    }
    Set-Prop -Object $settings -Name 'env' -Value $envObj
  }

  # 2) enabledPlugins: rebuild from installed_plugins.json, fallback to baseline
  $pluginMap = [ordered]@{}
  $installed = Read-JsonObject -Path $installedPluginsPath
  if ($null -ne $installed -and $installed.PSObject.Properties.Name -contains 'plugins' -and $null -ne $installed.plugins) {
    foreach ($p in $installed.plugins.PSObject.Properties) {
      $pluginMap[$p.Name] = $true
    }
  }

  if ($baseline.PSObject.Properties.Name -contains 'enabledPlugins' -and $null -ne $baseline.enabledPlugins) {
    foreach ($p in $baseline.enabledPlugins.PSObject.Properties) {
      if (-not $pluginMap.Contains($p.Name)) {
        $pluginMap[$p.Name] = [bool]$p.Value
      }
    }
  }

  if ($pluginMap.Count -gt 0) {
    $enabledPluginsObj = [pscustomobject]@{}
    foreach ($k in $pluginMap.Keys) {
      $enabledPluginsObj | Add-Member -NotePropertyName $k -NotePropertyValue $pluginMap[$k]
    }
    Set-Prop -Object $settings -Name 'enabledPlugins' -Value $enabledPluginsObj
  }

  # 3) statusLine: keep existing value; only restore from baseline when missing
  $hudInstalled = $pluginMap.Contains('claude-hud@claude-hud')
  $hasStatusLine = $settings.PSObject.Properties.Name -contains 'statusLine'
  if (-not $hasStatusLine -and $hudInstalled -and $baseline.PSObject.Properties.Name -contains 'statusLine') {
    Set-Prop -Object $settings -Name 'statusLine' -Value $baseline.statusLine
  }

  # 4) write with backup
  if (Test-Path $settingsPath) {
    $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backupPath = Join-Path $claudeDir "settings.pre-fix.$timestamp.json"
    Copy-Item -Path $settingsPath -Destination $backupPath -Force
    Write-Log "Created pre-fix backup: $backupPath"
  }

  $output = $settings | ConvertTo-Json -Depth 100
  Set-Content -Path $settingsPath -Value $output -Encoding UTF8
  $output | Set-Content -Path $lastGoodPath -Encoding UTF8

  Write-Log 'Merge repair completed successfully.'
  Write-Output 'OK: settings.json repaired via baseline+merge strategy.'
} catch {
  Write-Log "Repair failed: $($_.Exception.Message)"
  Write-Error $_
  exit 1
}
