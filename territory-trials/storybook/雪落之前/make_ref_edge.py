# make_ref_edge.py — 用 edge-tts 台灣男聲(雲哲)生成 SoVITS 參考聲底（labs 執行、需網路）
# 用法：python make_ref_edge.py   （讀同資料夾 ref.txt、產 ref.wav 覆蓋舊聲底）
import asyncio, subprocess
from pathlib import Path
import edge_tts

BASE = Path(__file__).parent
text = (BASE / "ref.txt").read_text(encoding="utf-8").strip()

async def main():
    await edge_tts.Communicate(text, "zh-TW-YunJheNeural", rate="+5%").save(str(BASE / "ref_edge.mp3"))

asyncio.run(main())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(BASE / "ref_edge.mp3"),
                "-ar", "32000", "-ac", "1", str(BASE / "ref.wav")], check=True)
print("REF_EDGE_DONE", flush=True)
