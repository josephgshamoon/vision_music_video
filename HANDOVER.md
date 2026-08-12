# HANDOVER — read this first

You are picking up an in-progress job. **Read `LOCKED_SPEC.md` immediately after this file.**
Between them they contain every decision. Nothing below needs re-deriving, re-proposing or
re-litigating — it is all settled with the client.

**Do not spend credits without an explicit go-ahead.** The client has been careful about money
throughout and has asked repeatedly to approve before anything is generated.

Written: 2026-08-12

---

## Where the job actually is

**UPDATED 2026-08-12 — the raised-camera keyframe is DONE and CHOSEN.**

The client picked **`keyframes/CANDIDATE_RAISED_v10_bigfullball.png`** (job
`73c2c7a3-a529-41f3-a6a9-8f931165b5fe`) — *"This one is my favourite."* Ten candidates got
there; 22 credits spent; balance **198.14**. See LOCKED_SPEC for the accepted trade-offs on
that frame and the loop risk it introduces.

So steps 1–3 below are complete. **The immediate next action is step 4, and it needs an
explicit go-ahead that has not yet been given.**

1. ~~Generate the raised-camera keyframe~~ — done, v1–v10
2. ~~Show the client, get their pick~~ — done, v10 chosen
3. ~~Wait for explicit approval~~ — given, on the frame
4. ~~Render the video (90 credits)~~ — done, job `3baf176f-0ce4-4441-ab01-4c012cc2122f`
5. ~~Blend + run the QC gate~~ — done, **PASS**
6. **Show them the clip and the numbers** ← next

**Delivered:** `loops/BURN_last_road.mp4` — 229 frames, 9.541667s, 24fps, 1920×1080, silent.

| Check | Raw | Blended | Gate |
|---|---|---|---|
| Frozen frames | 0 | **0** | must be 0 ✅ |
| Loop seam ratio | 5.22× | **1.25×** | < ~1.5× ✅ |
| Loop jump | 9.92/255 | **2.36/255** | ✅ |
| Motion spikes | 0 | **0** | ✅ |

The raw render was a hard fail at 5.22× — a clearly visible jolt at the wrap. The 0.5s
overlap blend is what closed it. Nothing was retimed.

**The one thing still needing human eyes: the walk.** Silhouette area is stable across the
clip (±3%, no drift), so there is no push-in, and shin width oscillates 36–79px, so the legs
genuinely move. But the cycle is irregular rather than a clean stride, and no measurement
settles whether it *reads* as walking. Watch `loops/BURN_last_road_QC3x.mp4` (3× loop,
gitignored — rebuild with `ffmpeg -stream_loop 2 -i loops/BURN_last_road.mp4 -c copy out.mp4`).

Balance after the render: **104.14** — one full 90-credit retry still covered.

Note the connector drops mid-session and comes back. It is authenticated at org level but
toggles off per chat (`enabledInChat: false`); if the Higgsfield tools vanish, that is why, and
the client has to re-enable it in this chat's connector settings.

`tools/seamless_blend.sh` was broken on this branch and is now fixed — it parsed duration from
`ffmpeg -i` stderr, which exits non-zero and killed the script under its own `set -o pipefail`.
Step 5 would have failed on arrival. Verified working.

---

## Credits

- Balance: **~222** (client topped up 200; ~12 spent on keyframes since)
- Video render: **90 credits exactly** for 10s / 1080p / `std` — this is **verified by preflight**,
  not estimated
- Keyframes: 2 credits each
- Plan: 1 render (90) + a full retry held in reserve

Preflight with `get_cost: true` before any spend — it is free and the client was promised it.

---

## Image inventory — `keyframes/`

| File | What it is |
|---|---|
| `APPROVED_G1_original.png` | The frame the client's friend originally chose. Warm, GTA-styled, full globe, cypress avenue, couple walking away. **This is the composition everything descends from.** |
| `CANDIDATE_FIRE2_full_globe.png` | Current front-runner. Unreal-photoreal, cool blue night, complete sphere visible with continents veined in molten fire, figures clean. **Recommended base.** |
| `CANDIDATE_FIRE1_cropped_globe.png` | Same treatment but the globe is cropped by the top of frame, with heavier smoke plumes. Client did not pick this. |
| `A_PhoenixHour.png`, `B_AshGarden.png`, `C_Frequencies.png`, `D_Rising_unused.png` | Earlier, superseded direction (cel-shaded illustration). **Historical only — do not use.** |

### The client's stated preferences, in order

1. Cool blue night over warm/reddish — they said "I prefer the second one which is less reddish"
2. Globe must read as **violently burning**, not merely lit
3. Figures must be **clean dark silhouettes**, never on fire
4. Camera **raised** — the one outstanding change

---

## Ready-to-run image prompt (raised camera)

Model `nano_banana_pro`, aspect `16:9`. This is `CANDIDATE_FIRE2` plus the raised camera.

```
Photorealistic Unreal Engine 5 cinematic frame, game-engine realism, filmic GTA grade. Cold
blue night, fire confined to the planet and the valley.

THIRD-PERSON GTA-STYLE CAMERA: raised roughly 3-4 metres above the road and several metres
behind the pair, angled gently downward, like the over-the-shoulder chase camera in a modern
open-world game. The two people sit in the LOWER THIRD of frame, seen from behind and slightly
above. The dirt road surface, its ruts and dust, is clearly visible stretching away ahead of
them to a distant vanishing point. The cypresses are seen slightly from above, their tops near
eye level.

TWO people walk AWAY from camera, SIDE BY SIDE and in step, down the centre of the road. No
faces.

CRITICAL - THE PEOPLE ARE NOT BURNING. Zero flames, zero fire, zero glowing patches, zero
embers on their bodies, clothes, skin or hair. Clean solid dark silhouettes, fully in shadow,
matte black clothing with no lit surfaces. A single thin crisp rim-light outlines only the
extreme edge of their shoulders, arms and her hair.

LEFT - a man, broad and heavily built, plain black t-shirt, dark trousers, closely cropped hair
with a HIGH SKIN FADE and sharp line-up at the temple visible in silhouette.
RIGHT - a slim woman, long dark hair down her back drifting in the updraft, dark jacket and
trousers.

Filling the upper two thirds of frame: PLANET EARTH ENGULFED IN FIRE. Every continent ablaze -
immense webs of white-hot and molten orange fire crawling across all landmasses, entire regions
glowing like a furnace, colossal firestorms churning on the surface. Oceans reflect the blaze
in dark molten bronze. Columns of black smoke spiral off the surface. A blinding incandescent
atmospheric rim burns along the planet's curve. The complete sphere is visible.

Tall dark cypress trees line both sides of the road at perfectly even regular intervals,
receding to the vanishing point.

Burning valley on both flanks, distant towns alight, smoke columns climbing. Glowing embers
float through the AIR across the frame, large and softly out of focus in the foreground, never
landing on the people.

Sky deep cold blue-black, shadows cool and blue. The ONLY warmth comes from the burning planet,
the valley fires and the embers. Strong cold-versus-hot contrast. No overall red or sepia wash.

Unreal Engine 5 path-traced cinematic, physically based rendering, ray-traced global
illumination, volumetric fog and god rays, realistic bark and foliage, suspended ash, sharp
micro-detail, shallow depth of field, high dynamic range.

NOT cel shaded, NOT painterly, NOT cartoon, NOT anime. No text, no watermark, no HUD, no UI,
no lettering.
```

---

## Ready-to-run video settings

Model `seedance_2_0` · duration `10` · aspect `16:9` · resolution `1080p` · mode `std` ·
`generate_audio: false`

**Pass the chosen keyframe as BOTH `start_image` AND `end_image`.** Same image, both roles.
This is what forces the loop closed and is the single most important setting in the job.

Note: Seedance may return a `preset_recommendation` instead of submitting. If so, resubmit with
`declined_preset_id` set to the returned preset id.

```
Ambient continuous motion. Nothing happens once, nothing enters or leaves.

The two people walk steadily forward the entire time, side by side, straight ahead, legs
cycling in a natural unhurried stride. They advance only a short distance - about one
cypress-spacing. They NEVER turn, never look back, never turn their heads. Seen from behind
throughout. No faces at any point.

The cypress trees drift slowly toward camera and past the frame edges, each advancing exactly
one position, and sway very slightly in the heat. The dirt road surface slides slowly beneath
them.

The planet does NOT rotate - it stays completely fixed in the sky. On its surface, many small
explosions flare and fade continuously all over the globe at a constant steady rate, never one
large explosion. Black smoke drifts and curls continuously across the surface at constant
density.

Glowing embers drift through the air at constant unchanging density, fading softly in and out,
never popping into existence. Valley fires flicker steadily. Smoke columns rise at a constant
rate. Her long hair drifts gently; his t-shirt ripples faintly.

Light level stays perfectly constant. No flares, no surges, no gusts.

CAMERA: locked off, tracking forward at exactly their walking pace. No zoom, no push-in, no
dolly, no pan, no tilt, no cuts.

Seamless perfect loop. Constant particle density throughout.
```

**Negative prompt:**

```
text, watermark, logo, HUD, UI, camera zoom, push-in, rapid motion, cuts, transitions, figures
turning, visible faces, blinking, exposure flicker, brightness ramp, strobing, morphing
geometry, warping trees, extra limbs, deformed hands, oversaturated, lens flare pops
```

---

## Post-processing — do this every time

```bash
tools/seamless_blend.sh <ffmpeg> <in.mp4> <out.mp4> 0.5
tools/verify_loop.py <out.mp4> <ffmpeg>
```

0.5s overlap, **no retime**. Output is `(source - 0.5)` long, i.e. **9.54s** from a 10.04s
source, 229 frames at 24fps.

**The client accepted 9.54s over 10.000s deliberately**, to buy a full second attempt within
budget. Do not "fix" the length by stretching — see below.

### The bug that must not recur

**Never retime a blended clip with `setpts`.** Slowing a clip that way duplicates frames, and a
duplicated frame is a dead frame — motion freezes then jumps. On fire it reads unmistakably as
the picture cutting and resuming. Two clips shipped to this client with 26 and 35 frozen frames,
**and they spotted it.**

It slipped through because verification only measured the loop seam, and duplicated frames have
near-zero frame-to-frame difference — so they scored *better* on seam smoothness while looking
broken.

Frame interpolation (`minterpolate`) was tested as an alternative and **rejected**: it keeps
frames unique but re-synthesises the blended region and re-opens the seam (2.99× versus 1.35×
for a plain blend).

If a specific round duration is ever required, **generate a longer source** — never stretch.

---

## QC gate — all must pass before showing the client

| Check | Pass condition |
|---|---|
| Frozen frames | Exactly **zero**. Hard fail. |
| Loop seam ratio | < ~1.5× the clip's own median frame-to-frame motion |
| Motion spikes | None beyond what exists in the source |
| Ember popping | No particle appearing or vanishing abruptly |
| Geometry | No warping cypresses, no morphing continents |
| Anatomy | No extra limbs, no melting hands |
| Exposure | No brightness pumping across the cycle |

Report the actual numbers to the client — they have engaged with them throughout and expect
them. Also produce a **3× QC copy** (`-stream_loop 2 -c copy`) so they can watch the loop point
themselves.

---

## How this client works

- They pay for this personally and have said so. **Never spend without explicit approval.**
- They want problems raised **before** they cost money, not explained afterwards.
- They notice defects. They caught the frame-duplication stutter unprompted.
- They respond well to being told the honest risk — the walking loop is the highest-risk element
  in the job and they know it.
- They ask for questions to be posed **interactively** (option pickers) rather than as long
  prose lists.
- There is a **friend/client above them** who makes final calls on imagery.

---

## Do not resurrect

- Rooftop at golden hour with wine glasses — rejected as "too romantic"
- Three "fierier rooftop" variants — all rejected
- Slow Earth rotation — explicitly reversed, now out
- Trees static / walking on the spot — rejected in favour of one-tree travel
- Three videos — narrowed to one
- 9:16 vertical — deferred, not cancelled
- Restyling the approved frame to match others — declined
