# ralph.ps1 — mdcheck Ralph Loop Runner & Verifier
param(
    [int]$MaxIterations = 10
)

$ErrorActionPreference = "Stop"

foreach ($required in @("PRD.md", "PROMPT.md", "progress.md", "docs/designs/mdcheck.md")) {
    if (-not (Test-Path $required)) {
        Write-Error "필수 파일을 찾을 수 없습니다: $required"
        exit 1
    }
}

for ($i = 1; $i -le $MaxIterations; $i++) {
    Write-Host "`n=== Ralph Iteration $i / $MaxIterations ===" -ForegroundColor Cyan

    # PRD.md에 미완료 태스크(- [ ])가 없으면 루프 종료 및 최종 검증
    if (-not (Select-String -Path "PRD.md" -Pattern "- \[ \]" -Quiet)) {
        Write-Host "모든 태스크 완료! 최종 검증을 실행합니다..." -ForegroundColor Green
        break
    }

    $prompt = Get-Content -Raw -Encoding UTF8 "PROMPT.md"
    agy -p $prompt --output-format text

    if ($LASTEXITCODE -ne 0) {
        Write-Warning "agy 실행이 비정상 종료되었습니다 (ExitCode=$LASTEXITCODE)."
    }

    Start-Sleep -Seconds 2
}

Write-Host "`n=== Final Verification ===" -ForegroundColor Cyan
if (Test-Path "tests") {
    python -m pytest
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "최종 pytest 검증에서 실패가 발생했습니다."
    }
}

Write-Host "`n=== Git Commit History ===" -ForegroundColor Cyan
git log --oneline -n 10
