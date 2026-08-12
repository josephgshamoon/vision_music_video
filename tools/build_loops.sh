#!/usr/bin/env bash
# Rebuild every delivered loop in loops/ from scratch, and verify each one.
#
#   tools/build_loops.sh            # fetch (if needed), blend, verify
#   tools/build_loops.sh --refetch  # re-download the sources first
#
# Sources are the Higgsfield generations listed in tools/sources.json. They are
# NOT committed - they are ~27MB of intermediate that the manifest can recover.
# Only the finished loops are committed, because those are the deliverable.
#
# ON DURATION. Seedance returns 241 frames (10.041667s) for a 10s request, and
# the 0.5s overlap blend costs 12 of them, so the delivered loops are 9.541667s
# (229 frames), not 10.000s. That is not a rounding slip, it is the honest
# result of refusing to retime - see the warning in seamless_blend.sh.
#
# To get a true 10.000s / 240-frame loop, regenerate the sources at >= 10.5s
# (Seedance 2.0 accepts 4-15s) and pass a target:
#   seamless_blend.sh ffmpeg src.mp4 out.mp4 0.5 10.0
# The window is trimmed to 10.5s first and blended down to exactly 10.0s, so
# every frame stays unique. Worth doing once the BPM is known and the loop
# length is actually locked to the bar - until then 9.54s is not costing us
# anything, because 10.000s is not yet a real requirement.
set -euo pipefail
cd "$(dirname "$0")/.."

FF="${FFMPEG:-ffmpeg}"
OVERLAP=0.5
REFETCH=""
[ "${1:-}" = "--refetch" ] && REFETCH=1

command -v "$FF" >/dev/null || { echo "ffmpeg not found; set FFMPEG=/path/to/ffmpeg" >&2; exit 1; }
python3 -c "import PIL, numpy" 2>/dev/null || { echo "need Pillow and numpy: pip install Pillow numpy" >&2; exit 1; }

mkdir -p build/src loops

ids=$(python3 -c "import json;print(' '.join(c['id'] for c in json.load(open('tools/sources.json'))['clips']))")

for id in $ids; do
  url=$(python3 -c "
import json
print(next(c['url'] for c in json.load(open('tools/sources.json'))['clips'] if c['id']=='$id'))")
  src="build/src/$id.mp4"
  if [ -n "$REFETCH" ] || [ ! -f "$src" ]; then
    echo "fetch  $id"
    curl -fsSL -o "$src" "$url"
  fi
  bash tools/seamless_blend.sh "$FF" "$src" "loops/$id.mp4" "$OVERLAP"
  "$FF" -y -loglevel error -i "loops/$id.mp4" -frames:v 1 -q:v 3 "loops/$id.jpg"
done

echo
echo "=== verification ==="
fail=0
for id in $ids; do
  echo "--- $id"
  python3 tools/verify_loop.py "loops/$id.mp4" || fail=1
done
exit $fail
