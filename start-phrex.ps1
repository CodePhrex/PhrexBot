$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (!(Test-Path '.env') -or !(Test-Path '.venv\Scripts\python.exe')) { throw 'Phrex configuration or virtual environment missing' }
Get-Content .env | ForEach-Object {
    if ($_ -match '^([A-Z_][A-Z0-9_]*)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2].Trim(), 'Process')
    }
}
& .\.venv\Scripts\python.exe -u bot.py
exit $LASTEXITCODE
