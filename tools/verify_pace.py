#!/usr/bin/env python3
"""Verify that forward travel happens at a CONSTANT speed.

Why this exists as a separate check. verify_loop.py measures the loop seam and
duplicate frames. A clip can pass all of that and still be wrong in the way a
viewer notices first: the walkers speeding up and slowing down. That is exactly
what happened - the loop scored 1.25x with zero frozen frames, and the client's
first note was "they look like they are stopping or moving faster at times".

The cause is structural, not random. Feeding the same image as both the first
and last frame forces the model to land back where it began. When the subject is
also walking continuously, the model resolves that conflict the cheapest way it
can: it eases the motion off near the ends and runs faster through the middle.
So this defect is a PREDICTABLE consequence of the loop technique, and it needs
its own gate.

Method. Take a strip of road that contains no figures, no fire and no sky - just
ground texture scrolling toward camera. Its frame-to-frame difference is a proxy
for travel speed. Constant pace gives a flat series; easing gives a bowl or a
dome; stopping gives a trough.

Reported:
  cv          coefficient of variation of the speed series. Lower is steadier.
  ends/middle ratio of mean speed in the outer thirds to the middle third.
              ~1.00 is even. Below ~0.85 is the ease-in/ease-out signature.
  min/median  the deepest stall relative to typical speed.

Usage: verify_pace.py <video.mp4> [ffmpeg_path]
"""
import os, subprocess, sys, tempfile
from PIL import Image
import numpy as np


def analyse(path, ff="ffmpeg"):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", path,
                        "-vf", "scale=480:270", f"{d}/%04d.png"], check=True)
        frames = sorted(os.listdir(d))
        arr = np.stack([np.asarray(Image.open(f"{d}/{f}").convert("L"), dtype=np.float32)
                        for f in frames])

    # Road only: bottom band, and the outer thirds of it so the walkers are excluded.
    band = arr[:, 225:270, :]
    road = np.concatenate([band[:, :, 40:170], band[:, :, 310:440]], axis=2)

    speed = np.array([np.abs(road[i + 1] - road[i]).mean() for i in range(len(road) - 1)])
    med = float(np.median(speed))
    cv = float(speed.std() / speed.mean()) if speed.mean() else float("inf")

    n = len(speed)
    third = n // 3
    ends = float(np.concatenate([speed[:third], speed[-third:]]).mean())
    middle = float(speed[third:-third].mean())
    em = ends / middle if middle else float("inf")
    dip = float(speed.min()) / med if med else 0.0

    print(f"frames          {len(arr)}")
    print(f"median speed    {med:.3f}")
    print(f"cv              {cv:.3f}   (steadier is lower; < 0.25 is good)")
    print(f"ends/middle     {em:.2f}x   (1.00 is even; < 0.85 = ease in/out)")
    print(f"min/median      {dip:.2f}x   (deepest stall; > 0.55 is good)")
    q = [float(speed[i * n // 8]) for i in range(8)]
    print("profile         " + " ".join(f"{x:.2f}" for x in q))

    ok = cv < 0.25 and em > 0.85 and dip > 0.55
    print("verdict        ", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    sys.exit(0 if analyse(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ffmpeg") else 1)
