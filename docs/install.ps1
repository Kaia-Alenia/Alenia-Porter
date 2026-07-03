#!/usr/bin/env pwsh
#Requires -Version 5.1

$ErrorActionPreference = 'Stop'

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "       Installing Alenia Porter CLI for Windows...        " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$REPO    = "Kaia-Alenia/Alenia-Porter"
$BIN_DIR = "$env:LOCALAPPDATA\Programs\AleniaPorterCLI"
$BIN     = "$BIN_DIR\porter.exe"

Write-Host "[1/3] Fetching latest release from GitHub..."

$release = Invoke-RestMethod -Uri "https://api.github.com/repos/$REPO/releases/latest" -UseBasicParsing
$version = $release.tag_name

$asset = $release.assets | Where-Object { $_.name -like "*Windows*" } | Select-Object -First 1

if (-not $asset) {
    Write-Error "No Windows asset found in the latest release ($version). Please check https://github.com/$REPO/releases"
    exit 1
}

$zipUrl  = $asset.browser_download_url
$zipFile = "$env:TEMP\AleniaPorter-Windows.zip"

Write-Host "[2/3] Downloading $($asset.name) ($version)..."
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

Write-Host "[3/3] Installing to $BIN_DIR..."
if (Test-Path $BIN_DIR) { Remove-Item $BIN_DIR -Recurse -Force }
New-Item -ItemType Directory -Path $BIN_DIR -Force | Out-Null
Expand-Archive -Path $zipFile -DestinationPath $BIN_DIR -Force

$extractedExe = Get-ChildItem -Path $BIN_DIR -Recurse -Filter "ap.exe" | Select-Object -First 1
if (-not $extractedExe) {
    Write-Error "Could not find ap.exe inside the downloaded archive. Installation failed."
    exit 1
}

if ($extractedExe.FullName -ne $BIN) {
    Copy-Item $extractedExe.FullName $BIN -Force
}

Remove-Item $zipFile -Force

$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$BIN_DIR*") {
    Write-Host "Adding $BIN_DIR to your user PATH..."
    [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$BIN_DIR", "User")
    $env:PATH += ";$BIN_DIR"
    Write-Host "PATH updated. You may need to restart your terminal." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " Installation Complete!" -ForegroundColor Green
Write-Host " Type 'porter' in any new terminal to get started." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
