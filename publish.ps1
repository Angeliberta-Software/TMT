$version = "1.0.0"

$publishPath = "publish"
$manifestPath = "manifest.ini"
$chartReaderBuild = ".\\build.bat"
$chartReaderExe = "ChartReader\dist\ChartReader.exe"
$targetExe = Join-Path $publishPath "ChartReader.exe"

function Check-Success {
    param ([string]$message)
    if (-not $?) {
        Write-Host "Error: $message"
        exit 1
    }
}

if (Test-Path $publishPath) {
    Remove-Item $publishPath -Recurse -Force
    Check-Success "Failed to remove existing folder publish."
}

New-Item -ItemType Directory -Path $publishPath
Check-Success "Failed to create folder publish."

Copy-Item "doc" -Destination $publishPath -Recurse
Check-Success "Failed to copy doc."

Copy-Item "locale" -Destination $publishPath -Recurse
Check-Success "Failed to copy locale."

Copy-Item $manifestPath -Destination $publishPath
Check-Success "Failed to copy manifest.ini."

$manifestFile = Join-Path $publishPath "manifest.ini"
(Get-Content $manifestFile) | ForEach-Object {
    if ($_ -match '^\s*version\s*=\s*".*"\s*$') {
        'version = "' + $version + '"'
    }
    else {
        $_
    }
} | Set-Content $manifestFile
Check-Success "Failed to modify version in manifest.ini."

$initTargetDir = Join-Path $publishPath "appModules\terminal64"
New-Item -ItemType Directory -Path $initTargetDir -Force
Check-Success "Failed to create appModules\terminal64."

Copy-Item "appModules\terminal64\__init__.py" -Destination $initTargetDir
Check-Success "Failed to copy __init__.py."

Push-Location "ChartReader"
& $chartReaderBuild
Check-Success "ChartReader build.bat failed."
Pop-Location


Copy-Item $chartReaderExe -Destination $targetExe
Check-Success "Failed to copy ChartReader.exe to publish."

$zipName = "release-$version.zip"
$addonName = "TMT-v$version.nvda-addon"

Compress-Archive -Path "$publishPath\*" -DestinationPath $zipName
Check-Success "Failed to create archive $zipName."

if (Test-Path $addonName) {
    Remove-Item $addonName -Force
    Check-Success "Failed to remove old .nvda-addon."
}

Rename-Item -Path $zipName -NewName $addonName
Check-Success "Failed to rename  $zipName to $addonName."

Write-Host "publish success. $archiveName"
