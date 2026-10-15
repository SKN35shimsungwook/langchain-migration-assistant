[Console]::OutputEncoding = [Text.Encoding]::UTF8
$res = 'C:\sk-encore\SKN35-3rd-4Team\eval\results'
$total = 50
function Count($name) { $p = Join-Path $res "raw_$name.jsonl"; if (Test-Path $p) { (Get-Content $p -Encoding UTF8 | Where-Object { $_.Trim() }).Count } else { 0 } }
function Bar($n) { $w = 30; $f = [math]::Floor($w * $n / $total); ('#' * $f) + ('.' * ($w - $f)) }
while ($true) {
  $b = Count 'bot'; $l = Count 'llm'; $r = Count 'route'
  Clear-Host
  Write-Host '=== 평가 진행 상황 (3초마다 새로고침, Ctrl+C로 닫기) ===' -ForegroundColor Cyan
  Write-Host ''
  Write-Host ('① 우리 챗봇   [{0}] {1,2}/{2}' -f (Bar $b), $b, $total)
  Write-Host ('② 일반 LLM    [{0}] {1,2}/{2}' -f (Bar $l), $l, $total)
  Write-Host ('③ 분류 3회    [{0}] {1,2}/{2}' -f (Bar $r), $r, $total)
  Write-Host ''
  $pass = 0; $fail = 0; $other = 0
  if (Test-Path "$res\raw_bot.jsonl") {
    foreach ($line in Get-Content "$res\raw_bot.jsonl" -Encoding UTF8) {
      if (-not $line.Trim()) { continue }
      $o = $line | ConvertFrom-Json
      if ($o.classification -ne 'migration') { $other++ } elseif ($o.verify_result.passed) { $pass++ } else { $fail++ }
    }
  }
  Write-Host ('챗봇 결과: 검증 통과 {0} · 검증 실패 {1} · 변환 안 함(검색/일반 답) {2}' -f $pass, $fail, $other) -ForegroundColor Yellow
  Write-Host ''
  Write-Host '--- 최근 처리한 질문 ---' -ForegroundColor Cyan
  Get-Content "$res\run_log.txt" -Encoding UTF8 | Where-Object { $_ -match '^\s+\[(bot|llm|route)\]' } | Select-Object -Last 8 | ForEach-Object {
    $t = $_.Trim()
    if ($t -match 'True') { Write-Host $t -ForegroundColor Green } elseif ($t -match 'False') { Write-Host $t -ForegroundColor Red } else { Write-Host $t }
  }
  if ($r -ge $total) { Write-Host ''; Write-Host '=== 실행 끝! 채점과 보고서는 Claude가 이어서 만듭니다 ===' -ForegroundColor Green; break }
  Start-Sleep -Seconds 3
}
