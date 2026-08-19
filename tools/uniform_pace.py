#!/usr/bin/env python3
"""Resample a clip so the camera travels at a CONSTANT SPEED.

The problem this solves. Feeding the same image as start and end frame makes the
model decelerate near the end so it can land back on the start frame. That
deceleration is what the client saw as "stopping or moving faster at times". But
the deceleration is also what produces the best loop point in the clip - throwing
those frames away costs a 2.4x join and buys a 4.8x one.

So keep them, and fix the speed instead.

Method: measure how far the ground scrolls between every pair of frames, then
pick output frames at equal intervals of DISTANCE rather than equal intervals of
TIME. Where the camera slowed down, frames get dropped; where it ran normally,
they are kept. The result advances by the same amount every frame.

Why this is safe when the old setpts retime was not. That retime SLOWED the clip,
which duplicates frames, and a duplicated frame is a dead frame - the picture
freezes and jumps. This only ever DROPS frames. Nothing is duplicated, and the
script refuses to run if the resampling would repeat any frame.

Usage: uniform_pace.py <in.mp4> <out.mp4> [start] [end] [ffmpeg]
"""
import os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

IN, OUT = sys.argv[1], sys.argv[2]
S = int(sys.argv[3]) if len(sys.argv) > 3 else 0
E = int(sys.argv[4]) if len(sys.argv) > 4 else -1
FF = sys.argv[5] if len(sys.argv) > 5 else "ffmpeg"

d = tempfile.mkdtemp(); o = tempfile.mkdtemp()
subprocess.run([FF, "-y", "-loglevel", "error", "-i", IN, f"{d}/%05d.png"], check=True)
fs = sorted(os.listdir(d))
if E < 0 or E > len(fs): E = len(fs)
fs = fs[S:E]

small = np.stack([np.asarray(Image.open(f"{d}/{f}").convert("L").resize((480, 270)), dtype=np.float32)
                  for f in fs])
band = small[:, 225:270, :]
road = np.concatenate([band[:, :, 40:170], band[:, :, 310:440]], axis=2)
speed = np.array([np.abs(road[i + 1] - road[i]).mean() for i in range(len(road) - 1)])

dist = np.concatenate([[0.0], np.cumsum(speed)])       # distance travelled by each frame
total = dist[-1]

# Largest output length that never repeats a frame.
M = len(fs)
while M > 8:
    targets = np.linspace(0, total, M, endpoint=False)
    idx = np.searchsorted(dist, targets).clip(0, len(fs) - 1)
    if len(set(idx.tolist())) == len(idx):
        break
    M -= 1
else:
    sys.exit("could not resample without repeating frames")

for k, i in enumerate(idx):
    Image.open(f"{d}/{fs[i]}").save(f"{o}/{k:05d}.png")

subprocess.run([FF, "-y", "-loglevel", "error", "-framerate", "24", "-i", f"{o}/%05d.png",
                "-r", "24", "-c:v", "libx264", "-preset", "slow", "-crf", "15",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", OUT], check=True)
kept = len(idx); dropped = len(fs) - kept
print(f"{IN}[{S}:{E}] {len(fs)} frames -> {OUT} {kept} frames ({kept/24:.3f}s), "
      f"{dropped} dropped, 0 duplicated")
