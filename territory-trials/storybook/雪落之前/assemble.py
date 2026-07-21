# assemble.py — 《雪落之前》組裝：Ken Burns 推拉＋旁白＋字幕（labs 執行、需 ffmpeg 在 PATH）
# 用法：python assemble.py   （cwd 不限；輸出 final.mp4 於本資料夾）
import json, subprocess, os
from pathlib import Path

BASE = Path(__file__).parent
os.chdir(BASE)  # ass 濾鏡用相對路徑、避開 Windows 冒號跳脫地獄
spec = json.loads(Path("frames.json").read_text(encoding="utf-8"))
FPS = 24
PAD = 0.8  # 每幀旁白後留白秒數
W, H = spec["width"], spec["height"]

def run(cmd):
    print(">>", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run(cmd, check=True)

def wav_dur(p):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())

def ts(sec):  # ass 時間格式 h:mm:ss.cs
    cs = int(round(sec * 100))
    return f"{cs//360000}:{cs%360000//6000:02d}:{cs%6000//100:02d}.{cs%100:02d}"

segs, subs, t0 = [], [], 0.0
for i, f in enumerate(spec["frames"]):
    img, wav = f"frame_{f['id']:02d}.png", f"line_{f['id']:02d}.wav"
    dur = wav_dur(wav) + PAD
    frames = int(dur * FPS)
    zin = i % 2 == 0  # 奇偶幀交替推近/拉遠
    z = (f"1+0.08*on/{frames-1}") if zin else (f"1.08-0.08*on/{frames-1}")
    seg = f"seg_{f['id']:02d}.mp4"
    fade = f"fade=t=in:st=0:d=0.5,fade=t=out:st={dur-0.5:.3f}:d=0.5"
    # 4 倍超取樣再 zoompan：把整數捨入誤差壓到次像素、消除鏡頭抖動
    run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", img,
         "-i", wav, "-filter_complex",
         f"[0:v]scale={W*4}:{H*4}:flags=lanczos,zoompan=z='{z}':d={frames}"
         f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},{fade},format=yuv420p[v];"
         f"[1:a]apad[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-c:a", "aac", "-b:a", "192k", "-ar", "44100", seg])
    segs.append(seg)
    subs.append((t0 + 0.2, t0 + dur - 0.2, f["narration"]))
    t0 += dur

Path("list.txt").write_text("".join(f"file '{s}'\n" for s in segs), encoding="utf-8")
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "merged.mp4"])

ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, "
       "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: N,Microsoft JhengHei,44,&H00FFFFFF,&H00101010,&H80000000,1,2,1,2,60,60,42,1", "",
       "[Events]", "Format: Layer, Start, End, Style, Text"]
for a, b, txt in subs:
    ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},N,{txt}")
Path("subs.ass").write_text("\n".join(ass), encoding="utf-8-sig")

run(["ffmpeg", "-y", "-i", "merged.mp4", "-vf", "ass=subs.ass",
     "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "copy", "final.mp4"])
run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
     "-of", "default=noprint_wrappers=1", "final.mp4"])
print("ASSEMBLE_DONE", flush=True)
