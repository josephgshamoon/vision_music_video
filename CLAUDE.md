# BURN — music visualizer

A set of seamless looping visualizers for **BURN** (SWITCH O × THE VISION, from
*BLIND BUT NOW I SEE*).

## Working rules

**Images first. Always.** Lock a still before spending anything on motion. Video
generation is the expensive, slow, low-control step; a keyframe is cheap to iterate
and it is also the thing that makes the loop work at all (it gets fed as both the
first and last frame). Never generate video off an unapproved still.

**Never retime a clip to hit a round duration.** `setpts` slowdown duplicates frames,
and a duplicated frame reads as the picture freezing and jumping — badly, on fire and
ember content. If a length is required, generate a longer source and let the trim
absorb the difference. See the warning block in `tools/seamless_blend.sh`.

**A loop is not verified until `tools/verify_loop.py` passes.** Eyeballing misses the
failure that matters: duplicated frames make a clip score *better* on seam smoothness
while looking obviously broken. The seam ratio should sit near **1.0×**, not near zero.

## Layout

| Path | What |
|---|---|
| `concept_page.html` | **The live concept** (PHOENIX HOUR, v2). Start here. |
| `CONCEPT_BURN_10S_LOOP.md` | v1, superseded — but §5 loop mechanics is still the reference. |
| `keyframes/` | Approved stills, one per direction. Source of every loop. |
| `loops/` | Delivered loops + poster frames. Built, not hand-made. |
| `tools/build_loops.sh` | Rebuilds `loops/` from nothing. The entry point. |
| `tools/seamless_blend.sh` | Overlap-blend that closes the loop. |
| `tools/verify_loop.py` | Seam / ratio / frozen-frame measurement. |
| `tools/sources.json` | Provenance: which Higgsfield generation each loop came from. |
| `reference/` | Album art the palette was sampled from. |

`build/` is intermediate and gitignored; sources re-download from `tools/sources.json`.

## Environment

Needs `ffmpeg` plus Python `Pillow` and `numpy` — none are preinstalled in a fresh
web session:

```sh
apt-get install -y ffmpeg && pip install Pillow numpy
```

Then `bash tools/build_loops.sh` should rebuild and pass all four.
