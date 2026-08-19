#!/usr/bin/env python3
"""Overlap-blend that only dissolves the part of the frame that needs it.

A plain crossfade dissolves the WHOLE picture, which reads as the shot changing
to another shot - the client's words were "it blends into another screen".

But the frame does not mismatch uniformly. Measured at the loop point:

    sky + globe      5.73/255  (2%)   <- the globe is fixed, so it barely moves
    trees / road    38.10/255  (15%)  <- these scroll, so they mismatch badly

So the sky can take an almost invisible HARD CUT, and only the lower part of the
frame needs a dissolve. Restricting the dissolve to the ground keeps the largest,
most legible element in the picture - the burning planet - rock steady across the
join, which is what stops it reading as a change of scene.

Usage: masked_blend.py <in.mp4> <out.mp4> [overlap_s] [ffmpeg]
"""
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

IN, OUT = sys.argv[1], sys.argv[2]
X = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
FF = sys.argv[4] if len(sys.argv) > 4 else "ffmpeg"
FPS = 24
NB = int(round(X * FPS))

d = tempfile.mkdtemp(); o = tempfile.mkdtemp()
subprocess.run([FF, "-y", "-loglevel", "error", "-i", IN, f"{d}/%05d.png"], check=True)
fs = sorted(os.listdir(d))
n = len(fs)
out_n = n - NB
H, W = np.asarray(Image.open(f"{d}/{fs[0]}")).shape[:2]

# vertical weighting: 0 = hard cut (sky), 1 = full dissolve (ground)
y = np.linspace(0, 1, H)
soft = np.clip((y - 0.42) / 0.22, 0, 1)[:, None, None]   # ramp in across the horizon

for i in range(out_n):
    if i < NB:
        head = np.asarray(Image.open(f"{d}/{fs[i]}"), dtype=np.float32)
        tail = np.asarray(Image.open(f"{d}/{fs[out_n + i]}"), dtype=np.float32)
        t = (i + 1) / (NB + 1)
        w_dissolve = t                       # smooth ramp for the ground
        w_cut = 1.0 if i >= NB // 2 else 0.0  # hard switch for the sky
        w = soft * w_dissolve + (1 - soft) * w_cut
        frame = head * w + tail * (1 - w)
    else:
        frame = np.asarray(Image.open(f"{d}/{fs[i]}"), dtype=np.float32)
    Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(f"{o}/{i:05d}.png")

subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{o}/%05d.png",
                "-r", str(FPS), "-c:v", "libx264", "-preset", "slow", "-crf", "15",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", OUT], check=True)
print(f"{IN} -> {OUT}  ({out_n} frames, {out_n/FPS:.3f}s, {NB}-frame masked blend)")
