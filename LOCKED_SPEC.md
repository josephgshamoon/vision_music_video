# BURN — Visualizer: LOCKED SPEC

**This file is the single source of truth.** It captures decisions made in conversation that
were previously never written down. If you are a new session picking this up: read this file
first, and do not re-derive or re-litigate anything below. It is all decided.

Last updated: 2026-08-12

---

## Project

One **single** seamless looping video for the track **BURN** — SWITCH O × THE VISION, from the
album *Blind But Now I See*.

Not three videos. **One.** (Scope was narrowed from 3 → 1.)

---

## The image — LOCKED, do not regenerate

The approved keyframe is the "last road" composition:

- Two figures walking **away from camera**, side by side, down a pale dirt road running dead
  straight to a distant vanishing point
- **Cypress trees** lining both sides at perfectly even, regular intervals
- An **enormous burning planet Earth** filling the sky above the vanishing point
- A **valley on fire** on both flanks — towns ablaze, smoke columns
- A **storm of embers** rising through the frame

Higgsfield job id of the approved frame: `a76a79ca-ce50-4857-925c-16200fe9ef37`
Local copy: `keyframes/` (also `G1` in session notes)

The client picked this specific frame. **Do not restyle or regenerate it without explicit
approval.** An earlier concern about "black letterbox bars" on it was measured and found to be
**false** — there are no bars; those are dark sky. Nothing needs fixing.

---

## Style — "Unreal Engine realistic, but like GTA"

**This is a LOOK TO PROMPT FOR. It is NOT an actual UE5 render pipeline.**

No game engine is involved anywhere in this project. Everything is generated through
Higgsfield (`nano_banana_pro` for stills, `seedance_2_0` for video). "Unreal Engine" is prompt
language describing the desired surface quality, nothing more.

Concretely it means:

- Photoreal fidelity: physically based materials, ray-traced global illumination, firelight
  bouncing off the road surface, volumetric smoke and god rays, realistic bark and foliage
  detail, airborne dust and particulate, wide dynamic range, sharp micro-contrast
- Graded like a GTA cutscene: rich saturated warmth against deep charcoal, strong filmic
  contrast, subtle anamorphic bloom, slight chromatic aberration, fine grain
- **Not** cel shaded, **not** painterly brushwork, **not** cartoon, **not** anime

The project moved through three style eras. Current is the third:
cel-shaded illustration → painterly matte painting → **Unreal/GTA photoreal**.

---

## Motion spec — LOCKED

### The two figures
- They **walk continuously** for the entire clip, side by side, straight ahead
- They **never turn, never look back, never turn their heads**
- Seen **from behind at all times**. **No faces, ever.**
- Deliberate decision: back view only. No face means nothing can morph between frames, which is
  the main way AI video breaks. This is a loop-safety choice, not an aesthetic one.
- Her long dark hair drifts and lifts gently in the hot updraft; his t-shirt ripples faintly

### The walk and the trees — the load-bearing decision
- Over the loop, the pair advance **exactly ONE cypress-spacing**
- The cypresses **do move** — they drift toward camera and past the frame edges, each advancing
  exactly one position
- Because the spacing is even, the avenue therefore looks **identical at the end as at the
  start**, which is what closes the loop
- The cypresses also **sway slightly** in the heat
- This is NOT "trees static / walking on the spot" (that option was offered and rejected)
- This is NOT free-running forward travel over several tree-spacings (that breaks the loop)

**The cypress spacing IS the loop period.** Getting the travel distance wrong breaks the loop
rather than merely looking off.

### The Earth
- **FIXED. NO ROTATION.** The client initially wanted very slow rotation; this was **reversed**
  and rotation is now explicitly out.
- Reason: a globe rotating continuously can never return to its exact starting angle, so it
  cannot loop. Removing it makes every element in the shot mathematically loopable.
- All motion on the Earth lives in the **fire on its surface**, not in the body of it:
  - **Small explosions**, many of them, flaring and fading **continuously** across the globe at
    a constant rate. Each is small and short-lived. **Never one big explosion** — a single blast
    blooms once and stamps a recognisable timestamp on the cycle.
  - **Black smoke** drifting and curling continuously over the surface at constant density.
    **Not** one growing plume.
- The principle: constant-rate, many-small effects are statistically identical at every instant,
  so they loop for free. This is the same reason the ember streams work.

### Everything else
- **Embers**: constant density, rising and drifting, **fading softly in and out — never popping**
- **Valley fires**: steady flicker; smoke columns rise at a constant rate
- **Camera**: locked, tracking forward at exactly the walkers' pace. No zoom, push-in, dolly,
  pan, tilt or cuts
- **Light**: perfectly constant. No flares, no surges, no gusts

---

## Delivery

| Setting | Value |
|---|---|
| Clips | 1 |
| Resolution | Native 1920×1080 |
| Mode | `std` (not `fast`) |
| Frame rate | 24 fps |
| Audio | Silent — music sits on top |
| Aspect | 16:9 only (9:16 deferred) |
| Length | **9.54s** (229 frames) |
| Model | `seedance_2_0` |
| Conditioning | Same keyframe as **BOTH** `start_image` **AND** `end_image` |

**Why 9.54s and not 10.000s:** a true 10.000s output requires a 12s source, costing ~108 per
render. At 90 per render, choosing 9.54s buys a **complete second attempt** within the same
budget. On an endlessly repeating loop the 0.46s difference is imperceptible, and there is no
tempo sync riding on it. Two full attempts beat one attempt plus a stranded remainder.

**Tempo:** not synced. Flat length chosen deliberately; BPM was never needed.

### Cost — verified, not estimated
- **90 credits** exactly per 10s / 1080p / `std` render (confirmed via preflight)
- Balance at time of writing: **234 credits**
- Plan: 1 render (90) + at least one retry held in reserve

---

## THE CRITICAL BUG — do not repeat

**Never retime a blended clip with `setpts` to stretch it back to a round duration.**

Slowing a clip that way **duplicates frames**. A duplicated frame is a dead frame: motion
freezes for a beat and then jumps. On slow ambient footage it is subtle; on fire and embers it
reads unmistakably as the picture *cutting and resuming*. Two clips shipped with **26 and 35
frozen frames** before this was caught — and the client spotted it.

It slipped through because the verification at the time only measured the loop seam. Duplicated
frames have near-zero frame-to-frame difference, so they made the clip score **better** on seam
smoothness while looking plainly broken.

**Correct approach:** generate at the source length and blend down, accepting the shorter
result. If a specific round duration is required, generate a **longer source** instead.

**Frame interpolation was tested as an alternative and REJECTED.** `minterpolate` keeps every
frame unique but re-synthesises the blended region and re-opens the seam (measured 2.99× on the
phoenix clip, versus 1.35× for a plain blend).

---

## Post pipeline

`tools/seamless_blend.sh` — overlap blend, **0.5s**, no retime:

```
out(t) = head(t)*(t/X) + tail(t)*(1-t/X)   for 0 <= t < X
```

Both ends then land on the same source frame, so the loop closes. Output is
`(source - overlap)` long. 0.5s was tuned as the shortest overlap that passes on every clip
tested, preserving the most duration.

---

## QC gate — every check must pass

`tools/verify_loop.py`

| Check | Pass condition |
|---|---|
| **Frozen frames** | Exactly **zero**. Hard fail. |
| **Loop seam ratio** | Jump < ~1.5× the clip's own median frame-to-frame motion |
| **Motion spikes** | None beyond what exists in the source |
| **Ember popping** | No particle appearing or vanishing abruptly |
| **Geometry** | No warping cypresses, no morphing continents |
| **Anatomy** | No extra limbs, no melting hands |
| **Exposure** | No brightness pumping across the cycle |

**Why three separate metrics.** Any one alone can be passed by a broken clip:

- Absolute jump alone is misleading — a slow clip can post a small absolute jump that is still
  4.5× its normal motion, which reads as a jolt.
- Ratio alone is fooled by duplicate frames, which score as perfectly smooth.
- So: absolute jump, ratio against the clip's own motion, **and** a frozen-frame count.

Correct loops sit near 1.0 on the ratio — the loop boundary should look like any other frame
boundary, **not** like a frozen duplicate.

Compare spikes against the source before treating them as defects: rhythmic content produces
them legitimately.

---

## Characters

**Him** (the artist, from supplied reference photos):
- Broad, heavily built, early thirties
- Short black hair, **high skin fade** at the sides, **sharp straight line-up** at the temple —
  this reads clearly in silhouette and is the main likeness cue
- Full thick dark beard and matte black wayfarer sunglasses (not visible in back view, but part
  of his identity if a profile is ever considered)
- Plain black crew-neck t-shirt, dark trousers
- **Dark tattoo sleeves on both forearms**, catching the firelight

**Her:**
- Slim, similar height
- **Long dark hair** falling down her back, lifting in the updraft
- Dark jacket and trousers
- Deliberately anonymous unless told otherwise

---

## Rejected — do not resurrect

- **Rooftop at golden hour with wine glasses** — rejected as "too romantic"
- **Three "fierier rooftop" variants** (standing defiant / low angle / epic scale) — all rejected
- **Slow Earth rotation** — reversed, now explicitly out
- **Trees static, walking on the spot** — offered and rejected in favour of one-tree travel
- **Three videos** — narrowed to one
- **9:16 vertical** — deferred, not cancelled
- **Restyling the approved frame to match others** — declined; leave it as the client picked it

---

## Order of operations

1. Verify pricing (free preflight) before any spend
2. Unreal-look keyframe comparison — done; awaiting client pick between the approved frame and
   the two new Unreal-style variants
3. **Client sign-off on the chosen frame**
4. Render the video
5. Run the QC gate
6. Show the client the result **with the numbers**
7. Re-roll from reserve if anything fails

Never spend without an explicit go-ahead.
