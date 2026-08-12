#!/usr/bin/env bash
# Turn a near-loop into a true seamless loop by overlap-blending.
#
#   out(t) = head(t)*(t/X) + tail(t)*(1-t/X)   for 0 <= t < X
#
# Both ends then land on the same source frame, so the loop closes.
# Output duration is (source - X). That shortening is deliberate.
#
# DO NOT retime the result back up to a round duration with setpts. Slowing a
# clip that way DUPLICATES frames, and a duplicated frame is a dead frame: the
# motion freezes and jumps. On slow ambient footage it is subtle; on fire and
# embers it reads as the picture cutting and resuming. Frame-interpolating
# instead (minterpolate) keeps every frame unique but re-synthesises the blended
# region and re-opens the seam. Neither is worth it.
#
# To land on an exact duration, do it the other way round: pass TARGET and
# generate a source at least (TARGET + X) long. The source is trimmed to a
# centred (TARGET + X) window FIRST, then blended down to exactly TARGET. Every
# frame stays unique because nothing is retimed - the length comes out of the
# trim, not out of the clock. A 15s Seedance source with X=0.5 yields a true
# 10.000s / 240-frame loop.
#
# Duration comes from ffprobe, not from parsing `ffmpeg -i` stderr. `ffmpeg -i`
# with no output file exits non-zero, which under `set -o pipefail` killed this
# script before it did any work.
#
# Usage: seamless_blend.sh <ffmpeg> <in.mp4> <out.mp4> [overlap_s] [target_s]
set -euo pipefail
FF="$1"; IN="$2"; OUT="$3"; X="${4:-0.5}"; TARGET="${5:-}"
FP="${FF%ffmpeg}ffprobe"; command -v "$FP" >/dev/null 2>&1 || FP=ffprobe

SRC=$("$FP" -v error -show_entries format=duration -of default=nw=1:nk=1 "$IN")
mkdir -p "$(dirname "$OUT")"

# Offset into the source, and the length of the window we blend down from.
if [ -n "$TARGET" ]; then
  WIN=$(python3 -c "print($TARGET+$X)")
  python3 -c "import sys; sys.exit(0 if $SRC >= $WIN - 1e-6 else 1)" || {
    echo "source is ${SRC}s; need >= ${WIN}s to deliver ${TARGET}s with a ${X}s overlap" >&2
    exit 1; }
  OFF=$(python3 -c "print(round(($SRC-$WIN)/2, 6))")
else
  WIN="$SRC"; OFF=0
fi
END=$(python3 -c "print(round($OFF+$WIN, 6))")     # end of the window in the source
MID=$(python3 -c "print(round($OFF+$X, 6))")      # end of head / start of middle
TL=$(python3 -c "print(round($END-$X, 6))")       # start of tail / end of middle

# head (X) blended with tail (X), then the middle (WIN-2X): total = WIN - X.
"$FF" -y -loglevel error -i "$IN" -filter_complex "\
[0:v]trim=${OFF}:${MID},setpts=PTS-STARTPTS[h];\
[0:v]trim=${MID}:${TL},setpts=PTS-STARTPTS[m];\
[0:v]trim=${TL}:${END},setpts=PTS-STARTPTS[t];\
[h][t]blend=all_expr='A*(T/${X})+B*(1-T/${X})'[b];\
[b][m]concat=n=2:v=1:a=0[c]" \
 -map "[c]" -r 24 -c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p -movflags +faststart -an "$OUT"

OUTD=$("$FP" -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT")
echo "$(basename "$IN") ${SRC}s -${X}s overlap-> $(basename "$OUT") ${OUTD}s"
