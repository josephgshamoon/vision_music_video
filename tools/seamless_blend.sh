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
# region and re-opens the seam. Neither is worth it - just accept the shorter
# loop, or generate a longer source so that (source - X) is the length you want.
#
# Usage: seamless_blend.sh <ffmpeg> <in.mp4> <out.mp4> [overlap_seconds]
set -euo pipefail
FF="$1"; IN="$2"; OUT="$3"; X="${4:-0.5}"
D=$("$FF" -i "$IN" -hide_banner 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' \
    | awk -F: '{print ($1*3600)+($2*60)+$3}')
ME=$(python3 -c "print($D-$X)")
"$FF" -y -loglevel error -i "$IN" -filter_complex "\
[0:v]trim=0:${X},setpts=PTS-STARTPTS[h];\
[0:v]trim=${X}:${ME},setpts=PTS-STARTPTS[m];\
[0:v]trim=${ME}:${D},setpts=PTS-STARTPTS[t];\
[h][t]blend=all_expr='A*(T/${X})+B*(1-T/${X})'[b];\
[b][m]concat=n=2:v=1:a=0[c]" \
 -map "[c]" -r 24 -c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p -movflags +faststart -an "$OUT"
echo "$IN (${D}s) - ${X}s overlap -> $OUT ($(python3 -c "print(round($D-$X,2))")s)"
