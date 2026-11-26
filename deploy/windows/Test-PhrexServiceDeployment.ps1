[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$InstallRoot,
 [Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-fA-F]{64}
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($InstallRoot)
$required = @('PhrexIntelligence.exe','PhrexIntelligence.xml','runtime\Scripts\python.exe','app\service_entry.py','app\bot.py','app\runtime_paths.py','app\service_config.py','app\runtime_lock.py','app\runtime_launcher.py')
$files = @($required | ForEach-Object { [pscustomobject]@{ RelativePath = $_; Exists = (Test-Path -LiteralPath (Join-Path $root $_) -PathType Leaf) } })
$wrapper = Join-Path $root 'PhrexIntelligence.exe'
$hashMatches = $false
if (Test-Path -LiteralPath $wrapper -PathType Leaf) {
 $hashMatches = ((Get-FileHash -LiteralPath $wrapper -Algorithm SHA256).Hash -ieq $ExpectedWrapperSha256)
}
$service = Get-Service -Name 'PhrexIntelligence' -ErrorAction SilentlyContinue
$task = Get-ScheduledTask -TaskName 'CodePhrex - Phrex AI' -TaskPath '\' -ErrorAction SilentlyContinue
[pscustomobject]@{
 InstallRoot = $root
 RequiredFiles = $files
 WrapperHashMatches = $hashMatches
 ServiceState = $(if ($service) { [string]$service.Status } else { 'Not found or inaccessible' })
 ScheduledTaskState = $(if ($task) { [string]$task.State } else { 'Not found or inaccessible' })
 RequiredFilesPresent = (@($files | Where-Object { -not $_.Exists }).Count -eq 0)
 InstallationAuthorized = $false
 PendingChecks = @('Independent wrapper provenance and trusted digest acquisition','Service identity and ACLs','Runtime compatibility','Credential provisioning','Exclusive activation','Recovery and rollback validation')
} | ConvertTo-Json -Depth 5
)][string]$ExpectedWrapperSha256)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($InstallRoot)
$required = @('PhrexIntelligence.exe','PhrexIntelligence.xml','runtime\Scripts\python.exe','app\runtime_launcher.py')
$files = @($required | ForEach-Object { [pscustomobject]@{ RelativePath = $_; Exists = (Test-Path -LiteralPath (Join-Path $root $_) -PathType Leaf) } })
$service = Get-Service -Name 'PhrexIntelligence' -ErrorAction SilentlyContinue
$task = Get-ScheduledTask -TaskName 'CodePhrex - Phrex AI' -TaskPath '\' -ErrorAction SilentlyContinue
[pscustomobject]@{
 InstallRoot = $root
 RequiredFiles = $files
 ServiceState = $(if ($service) { [string]$service.Status } else { 'Not found or inaccessible' })
 ScheduledTaskState = $(if ($task) { [string]$task.State } else { 'Not found or inaccessible' })
 RequiredFilesPresent = (@($files | Where-Object { -not $_.Exists }).Count -eq 0)
 InstallationAuthorized = $false
 PendingChecks = @('Wrapper provenance and hash','Service identity and ACLs','Runtime compatibility','Credential provisioning','Exclusive activation','Recovery and rollback validation')
} | ConvertTo-Json -Depth 5
