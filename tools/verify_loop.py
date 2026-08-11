#!/usr/bin/env python3
"""Verify a video loops cleanly.

Three checks, because any one of them alone can be passed by a broken clip:

1. LOOP JUMP, absolute. How different the last frame is from the first.

2. LOOP RATIO. That jump measured against the clip's own median frame-to-frame
   motion. This matters because absolute size alone is misleading: a very slow
   clip can post a small absolute jump that is still several times its normal
   motion, and reads as a jolt. Correct loops sit near 1.0 - the loop boundary
   should look like any other frame boundary, NOT like a frozen duplicate.

3. FROZEN FRAMES. Frames whose motion is near zero, i.e. duplicates. This is the
   check that matters most and the easiest to forget, because duplicates make a
   clip score BETTER on checks 1 and 2 while looking obviously broken. They are
   what a setpts slowdown inserts. Any nonzero count here is a fail.

Spikes are also reported, but compare them against the source before treating
them as defects - rhythmic content (a pulsing element) produces them legitimately.

Usage: verify_loop.py <video.mp4> [ffmpeg_path]
"""
import os, subprocess, sys, tempfile
from PIL import Image
import numpy as np


def analyse(path, ff="ffmpeg"):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", path,
                        "-vf", "scale=320:180", f"{d}/%04d.png"], check=True)
        frames = sorted(os.listdir(d))
        arr = np.stack([np.asarray(Image.open(f"{d}/{f}").convert("RGB"), dtype=np.float32)
                        for f in frames])

    motion = np.array([np.abs(arr[i + 1] - arr[i]).mean() for i in range(len(arr) - 1)])
    med = float(np.median(motion))
    jump = float(np.abs(arr[0] - arr[-1]).mean())
    ratio = jump / med if med else float("inf")
    frozen = [i for i, x in enumerate(motion) if x < med * 0.10]
    spikes = [i for i, x in enumerate(motion) if x > med * 4]

    print(f"frames          {len(arr)}  ({len(arr)/24:.2f}s @24fps)")
    print(f"median motion   {med:.3f}")
    print(f"loop jump       {jump:.2f}/255")
    print(f"loop ratio      {ratio:.2f}x")
    print(f"frozen frames   {len(frozen)}{' ' + str(frozen[:12]) if frozen else ''}")
    print(f"spikes          {len(spikes)}{' ' + str(spikes[:12]) if spikes else ''}")

    ok = jump < 2.5 and ratio < 2.2 and not frozen
    print("verdict        ", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    sys.exit(0 if analyse(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ffmpeg") else 1)
