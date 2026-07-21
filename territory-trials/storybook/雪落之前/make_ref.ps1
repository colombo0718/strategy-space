# make_ref.ps1 — 用 Windows 內建 TTS 生 SoVITS 參考聲（labs 執行）
# 說書人聲底暫代版：打通路徑用，正式旁白之後換聲優/自錄。
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$t = (Get-Content -Path "$PSScriptRoot\ref.txt" -Encoding UTF8 -Raw).Trim()
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$voices = $s.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }
Write-Host "VOICES: $($voices -join ', ')"
$zh = $voices | Where-Object { $_ -match 'Hanhan|HuiHui|Yating|Zhiwei|Kangkang|Tracy|TW|CN' } | Select-Object -First 1
if ($zh) { $s.SelectVoice($zh); Write-Host "PICKED: $zh" } else { Write-Host "PICKED: (default)" }
$s.Rate = -1
$s.SetOutputToWaveFile("$PSScriptRoot\ref.wav")
$s.Speak($t)
$s.Dispose()
Write-Host "REF_DONE"
