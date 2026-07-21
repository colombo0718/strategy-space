# tts_lines.py — 《雪落之前》旁白逐句合成（labs 本機執行、打 GPT-SoVITS api_v2）
# 前置：api_v2 已在 127.0.0.1:9880 起服務；ref.wav / ref.txt 已備（參考聲）。
import json, time, urllib.request, urllib.parse
from pathlib import Path

BASE = Path(__file__).parent
spec = json.loads((BASE / "frames.json").read_text(encoding="utf-8"))
REF_WAV = str((BASE / "ref.wav").resolve())
REF_TEXT = (BASE / "ref.txt").read_text(encoding="utf-8").strip()

def tts(text: str, out: Path):
    params = {
        "text": text,
        "text_lang": "zh",
        "ref_audio_path": REF_WAV,
        "prompt_text": REF_TEXT,
        "prompt_lang": "zh",
        "text_split_method": "cut5",
        "speed_factor": 1.1,
        "batch_size": 1,
        "media_type": "wav",
        "streaming_mode": "false",
    }
    url = "http://127.0.0.1:9880/tts?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=300) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} ({out.name}): {e.read().decode('utf-8', 'replace')[:500]}")
    if len(data) < 1000:
        raise SystemExit(f"TTS FAIL ({out.name}): {data[:200]!r}")
    out.write_bytes(data)
    print(f"SAVED {out.name} {len(data)} bytes", flush=True)

for f in spec["frames"]:
    out = BASE / f"line_{f['id']:02d}.wav"
    if out.exists():
        print(f"skip {out.name}", flush=True)
        continue
    tts(f["narration"], out)
    time.sleep(0.5)

print("ALL_LINES_DONE", flush=True)
