$ErrorActionPreference = 'Stop'
$service = Get-CimInstance Win32_Service -Filter "Name='PhrexIntelligence'"
$expected = 'NT SERVICE\PhrexIntelligence'
$result = [ordered]@{
    ServiceName = 'PhrexIntelligence'
    ExpectedIdentity = $expected
    ServicePresent = ($null -ne $service)
    IdentityMatches = $false
    State = 'NotInstalled'
    InstallationAuthorized = $false
}
if ($null -ne $service) {
    $result.IdentityMatches = ($service.StartName -ieq $expected)
    $result.State = $service.State
}
$result | ConvertTo-Json
