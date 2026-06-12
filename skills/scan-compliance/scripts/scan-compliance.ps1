param(
    [string]$Path = "$HOME\.mavis\agents",
    [string]$OutputFormat = "table"
)

$ErrorActionPreference = "SilentlyContinue"

$results = @()
$totalScanned = 0
$lawerdCount = 0
$clawicCount = 0
$anthropicCount = 0
$noSkillCount = 0
$compliantCount = 0
$issueCount = 0

if (-not (Test-Path $Path)) {
    Write-Host "Error: Path not found: $Path" -ForegroundColor Red
    exit 1
}

$agentDirs = Get-ChildItem -Path $Path -Directory -Force | Where-Object {
    Test-Path "$($_.FullName)\skills"
}

foreach ($agentDir in $agentDirs) {
    $skillsDir = "$($agentDir.FullName)\skills"
    $agentName = $agentDir.Name

    foreach ($skillDir in Get-ChildItem -Path $skillsDir -Directory -Force) {
        $totalScanned++
        $skillName = $skillDir.Name
        $skillFile = "$($skillDir.FullName)\SKILL.md"

        if (-not (Test-Path $skillFile)) {
            $noSkillCount++
            $results += [PSCustomObject]@{
                Agent = $agentName
                Name = $skillName
                Source = "?"
                Status = "FAIL"
                Issue = "SKILL.md missing"
            }
            continue
        }

        $content = Get-Content $skillFile -Raw

        # Extract frontmatter by splitting on --- with limit 3
        $parts = $content -split '---', 3
        $fm = if ($parts.Length -ge 2) { $parts[1] } else { "" }

        # Detect third-party skills (check FRONTMATTER only)
        $isClawic = ($fm -match '(?m)slug:') -or
                    ($fm -match '(?m)homepage:\s*https://clawic\.com') -or
                    ($fm -match '(?i)clawhub') -or
                    ($fm -match '(?i)skillhub') -or
                    ($fm -match '(?i)ClawdHub')

        $isAnthropic = ($fm -match '(?i)Claude') -or
                       ($fm -match '(?i)Anthropic') -or
                       ($fm -match 'extends Claude')

        $isThirdParty = $isClawic -or $isAnthropic
        $source = if ($isClawic) { "clawic 3rd-party" }
                  elseif ($isAnthropic) { "Anthropic official" }
                  else { "lawerd" }

        if ($isThirdParty) {
            if ($isClawic) { $clawicCount++ } else { $anthropicCount++ }
            $results += [PSCustomObject]@{
                Agent = $agentName
                Name = $skillName
                Source = $source
                Status = "SKIP"
                Issue = "third-party, not maintained by lawerd"
            }
            continue
        }

        $lawerdCount++

        # Compliance checks (no ^ anchor: some files lack trailing LF)
        $issues = @()
        if (-not ($content -match '(?m)author:'))      { $issues += "missing author" }
        if (-not ($content -match '(?m)version:'))     { $issues += "missing version" }
        if (-not ($content -match '(?m)license:'))     { $issues += "missing license" }
        if (-not ($content -match '(?m)description:')) { $issues += "missing description" }

        if (-not (Test-Path "$($skillDir.FullName)\LICENSE.txt")) {
            $issues += "missing LICENSE.txt"
        }

        if (-not (Test-Path "$($skillDir.FullName)\CHANGELOG.md")) {
            $issues += "missing CHANGELOG.md"
        }

        if ($content -match '## Mavis .* .* .*说明') {
            $issues += "trailing Mavis section not migrated"
        }

        if ($issues.Count -eq 0) {
            $compliantCount++
            $issueText = "all compliant"
        } else {
            $issueCount++
            $issueText = $issues -join "; "
        }

        $results += [PSCustomObject]@{
            Agent = $agentName
            Name = $skillName
            Source = $source
            Status = if ($issues.Count -eq 0) { "OK" } else { "FAIL" }
            Issue = $issueText
        }
    }
}

switch ($OutputFormat) {
    "json" { $results | ConvertTo-Json -Depth 3 }
    "csv"  { $results | ConvertTo-Csv -NoTypeInformation }
    default {
        Write-Host ""
        Write-Host "========= lawerD Skill Compliance Report =========" -ForegroundColor Cyan
        Write-Host "Scan time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        Write-Host "Scan path: $Path"
        Write-Host ""
        $results | Format-Table -AutoSize -Wrap
        Write-Host ""
        Write-Host "========= Summary =========" -ForegroundColor Cyan
        Write-Host "Total scanned:        $totalScanned"
        Write-Host "lawerD (in scope):   $lawerdCount  (compliant: $compliantCount, with issues: $issueCount)" -ForegroundColor $(if ($issueCount -eq 0) { "Green" } else { "Yellow" })
        Write-Host "Clawic 3rd-party:     $clawicCount  (skipped)"
        Write-Host "Anthropic official:   $anthropicCount  (skipped)"
        Write-Host "No SKILL.md:          $noSkillCount"
        Write-Host ""
    }
}
