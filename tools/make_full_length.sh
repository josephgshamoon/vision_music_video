#!/usr/bin/env bash
# Build a continuous full-length video by repeating the seamless cycle.
#
#   tools/make_full_length.sh <cycle.mp4> <seconds> <out.mp4> [crf] [scale]
#
# Example - the full 3:22 track at full quality:
#   tools/make_full_length.sh loops/BURN_last_road.mp4 202 build/BURN_full.mp4
#
# No credits, no generation: this only repeats footage that already exists.
# Repeat count is ceil(seconds / cycle) and the result is cut to the exact
# length, so the final cycle is allowed to land mid-way. That is fine - it is
# a loop, there is nothing to land on.
set -euo pipefail
IN="$1"; SECS="$2"; OUT="$3"; CRF="${4:-20}"; SCALE="${5:-}"
CYCLE=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$IN")
N=$(python3 -c "import math;print(math.ceil($SECS/$CYCLE))")
VF="${SCALE:+scale=$SCALE}"
ffmpeg -y -loglevel error -stream_loop $((N-1)) -i "$IN" -t "$SECS" \
  ${VF:+-vf "$VF"} -r 24 -c:v libx264 -preset slow -crf "$CRF" \
  -pix_fmt yuv420p -movflags +faststart -an "$OUT"
echo "$IN (${CYCLE}s) x${N} -> $OUT ($(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT")s)"
