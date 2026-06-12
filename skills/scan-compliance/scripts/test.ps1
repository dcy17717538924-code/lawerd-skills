$content = Get-Content '{{HOME_WIN}}\.mavis\agents\codex-engineer\skills\skill-dev-guide\SKILL.md' -Raw
$parts = $content -split '---', 3
$fm = if ($parts.Length -ge 2) { $parts[1] } else { '' }
Write-Host '=== FM RAW (replacing LF with \n) ==='
Write-Host ($fm -replace "`n", "\n")
Write-Host '=== CHECKS ==='
Write-Host "has version (line start): $($fm -match '(?m)^version:')"
Write-Host "has version (any): $($fm -match 'version:')"
Write-Host "length: $($fm.Length)"
