#!/bin/bash
# Overlap-blend a near-loop into a true seamless loop, retimed to exactly 10.000s.
# out(t) = head(t)*(t/X) + tail(t)*(1-t/X)  for 0<=t<X  -> both ends land on frame(D-X)
FF="$1"; IN="$2"; OUT="$3"; X=1.0
D=$("$FF" -i "$IN" -hide_banner 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' \
    | awk -F: '{print ($1*3600)+($2*60)+$3}')
MIDEND=$(echo "$D - $X" | bc -l)
NEWD=$(echo "$D - $X" | bc -l)
RATIO=$(echo "10.0 / $NEWD" | bc -l)
"$FF" -y -loglevel error -i "$IN" -filter_complex "\
[0:v]trim=0:${X},setpts=PTS-STARTPTS[head];\
[0:v]trim=${X}:${MIDEND},setpts=PTS-STARTPTS[mid];\
[0:v]trim=${MIDEND}:${D},setpts=PTS-STARTPTS[tail];\
[head][tail]blend=all_expr='A*(T/${X})+B*(1-T/${X})'[bl];\
[bl][mid]concat=n=2:v=1:a=0[cat];\
[cat]setpts=PTS*${RATIO},fps=24[final]" \
 -map "[final]" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -an "$OUT"
echo "$IN: D=${D}s -> blended ${NEWD}s -> retimed x${RATIO} -> $OUT"
