# gen_frames.py — 《雪落之前》分鏡逐幀出圖（labs 本機執行、仿 gen_tt_cover.py）
# 用法：C:\worker\sd\venv\Scripts\python.exe gen_frames.py
import json, torch
from pathlib import Path
from diffusers import DiffusionPipeline

BASE = Path(__file__).parent
spec = json.loads((BASE / "frames.json").read_text(encoding="utf-8"))

# 顯存守衛：labs 是生產機。顯存不足就中止、絕不擠爆別人的服務。
free, total = torch.cuda.mem_get_info()
print(f"VRAM free {free/1e9:.1f}GB / {total/1e9:.1f}GB", flush=True)
if free / 1e9 < 55:
    raise SystemExit(f"ABORT: 只剩 {free/1e9:.1f}GB free、需 ~55GB。不冒險擠生產服務。")

pipe = DiffusionPipeline.from_pretrained("Qwen/Qwen-Image", torch_dtype=torch.bfloat16)
pipe = pipe.to("cuda")

for f in spec["frames"]:
    out = BASE / f"frame_{f['id']:02d}.png"
    if out.exists():
        print(f"skip {out.name}", flush=True)
        continue
    img = pipe(
        prompt=spec["style_prefix"] + ", " + f["prompt"],
        negative_prompt=spec["negative"],
        width=spec["width"], height=spec["height"],
        num_inference_steps=30,
        true_cfg_scale=4.0,
        generator=torch.Generator("cuda").manual_seed(f["seed"]),
    ).images[0]
    img.save(out)
    print(f"SAVED {out.name}", flush=True)

print("ALL_FRAMES_DONE", flush=True)
