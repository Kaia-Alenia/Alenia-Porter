$ErrorActionPreference = "Stop"

Write-Host "Installing Alenia Porter for Windows..." -ForegroundColor Cyan

$zipUrl = "https://github.com/Kaia-Alenia/Alenia-Porter/releases/latest/download/AleniaPorter-Windows.zip"
$tempDir = Join-Path $env:TEMP "porter_install_temp"
$installDir = Join-Path $env:LOCALAPPDATA "AleniaPorter"
$zipFile = Join-Path $tempDir "AleniaPorter.zip"

if (Test-Path $tempDir) { Remove-Item -Recurse -Force $tempDir }
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

Write-Host "Downloading latest release..."
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile

Write-Host "Extracting..."
Expand-Archive -Path $zipFile -DestinationPath $tempDir -Force

$extractedDir = $tempDir
$innerDirs = Get-ChildItem -Path $tempDir -Directory
if ($innerDirs.Count -eq 1) {
    $extractedDir = $innerDirs[0].FullName
}

Write-Host "Installing to $installDir..."
if (Test-Path $installDir) { Remove-Item -Recurse -Force $installDir }
New-Item -ItemType Directory -Path $installDir -Force | Out-Null
Copy-Item -Path "$extractedDir\*" -Destination $installDir -Recurse -Force

$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notmatch [regex]::Escape($installDir)) {
    Write-Host "Adding $installDir to user PATH..."
    [Environment]::SetEnvironmentVariable("PATH", "$userPath;$installDir", "User")
    Write-Host "You may need to restart your terminal for the PATH changes to take effect." -ForegroundColor Yellow
}

Remove-Item -Recurse -Force $tempDir

Write-Host "Alenia Porter installed successfully!" -ForegroundColor Green
Write-Host "You can now run 'ap' or 'AleniaPorter' from the command line."
