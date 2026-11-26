[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$InstallRoot)
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
