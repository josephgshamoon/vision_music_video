#!/usr/bin/env python3
"""Verify a video loops cleanly.

The useful test is not "is the last frame identical to the first" - in a correct
loop it should NOT be identical, it should be exactly one frame of motion away.
So we compare the wrap-around jump against the clip's own median frame-to-frame
motion. A ratio near 1.0 means the loop point is indistinguishable from any
other frame boundary.

Usage: verify_loop.py <video.mp4> [ffmpeg_path]
"""
import os, subprocess, sys, tempfile
from PIL import Image
import numpy as np

def analyse(path, ff="ffmpeg"):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", path,
                        "-vf", "scale=320:180", f"{d}/%04d.png"], check=True)
        fs = sorted(os.listdir(d))
        arr = np.stack([np.asarray(Image.open(f"{d}/{f}").convert("RGB"), dtype=np.float32)
                        for f in fs])
    diffs = np.array([np.abs(arr[i+1] - arr[i]).mean() for i in range(len(arr)-1)])
    wrap = float(np.abs(arr[0] - arr[-1]).mean())
    med = float(np.median(diffs))
    ratio = wrap / med if med else float("inf")
    spikes = [i for i, x in enumerate(diffs) if x > med * 4]
    print(f"frames            {len(arr)}")
    print(f"median motion     {med:.3f}")
    print(f"loop-point jump   {wrap:.3f}/255")
    print(f"ratio             {ratio:.2f}x")
    print(f"mid-clip spikes   {spikes or 'none'}")
    # absolute jump matters too: a low-motion clip can score a high ratio while
    # still being visually clean.
    print("verdict          ", "PASS" if (wrap < 2.5 and ratio < 2.2) else "CHECK")

if __name__ == "__main__":
    analyse(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ffmpeg")
