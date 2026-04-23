param(
    [string]$SourcePath = (Join-Path $PSScriptRoot '..\files'),
    [string]$OutputPath = (Join-Path $PSScriptRoot '..\dist\tupian.zip')
)

$resolvedSource = Resolve-Path -LiteralPath $SourcePath -ErrorAction Stop
$outputDirectory = Split-Path -Parent $OutputPath

if (-not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
}

$items = Get-ChildItem -LiteralPath $resolvedSource -Force | Where-Object { $_.Name -ne '.gitkeep' }

if (-not $items) {
    Write-Error "No files found in '$resolvedSource'. Put files in the files folder first."
    exit 1
}

if (Test-Path -LiteralPath $OutputPath) {
    Remove-Item -LiteralPath $OutputPath -Force
}

$paths = $items | ForEach-Object { $_.FullName }
Compress-Archive -Path $paths -DestinationPath $OutputPath -Force
Write-Host "Created package: $OutputPath"
