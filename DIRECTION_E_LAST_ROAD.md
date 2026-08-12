# E — LAST ROAD

**Status:** lead direction, superseding A as primary. Keyframe not yet generated.
**Source:** artist-supplied reference frame (photoreal, 1386×786).

---

## Why this one

It keeps the grammar the whole concept rests on — *a tiny human against something
enormous* — and swaps the colossal object from an eye (album motif, not this song's)
to a **burning Earth** (this song's, exactly). It is continuous with Phoenix Hour
rather than a departure: same cypresses, same Mediterranean hill villages, same
backs-to-camera staging.

It also solves the problem that has been quietly shaping every direction so far:
**silhouettes have no face to keep consistent** across 229 frames.

## The frame

| Element | Description |
|---|---|
| Register | Photoreal cinematic. High contrast, deep crush, anamorphic wide. |
| Foreground | Pale road, one-point perspective, long shadows thrown toward camera. |
| Figures | Two, centre, backs to camera, silhouetted. Man left, woman right. |
| Framing | Cypress avenue converging left and right — a natural vignette. |
| Midground | Hill villages burning on both flanks. |
| Sky object | Colossal Earth on the horizon, continents traced in fire, mushroom-cloud plumes, bright rim-arc along the upper limb. |
| Air | Embers throughout. Smoke columns rising and leaning. |
| Key light | From ahead, behind the Earth — hence the backlit silhouettes. |

## Palette

Continuous with the release: `#F0785A` coral, `#FFB25C` gold, `#1E1813` bitumen for
the silhouettes and cypresses, with the sky pushed to a colder teal-black than A uses.
The pale road is the only high-value surface in frame and does the work of separating
the figures from the ground.

---

## Loop engineering — read before generating motion

### What loops for free

Embers, smoke, fire flicker in the continents and the villages, cypress sway. All
high-entropy, low-structure, constant-density. This frame is unusually rich in it.

### What will break the loop

| Risk | Why | Handling |
|---|---|---|
| **The figures are mid-stride** | Walking is a one-time action. They arrive, or they treadmill. | See the two options below. This is the open decision. |
| **Push-in down the road** | One-point perspective invites a dolly. A push cannot close. | Zoom and dolly disabled, hard, in the prompt. |
| **Symmetry** | A centred vanishing point makes *any* drift legible the moment it slides off-centre. | **Locked-off camera.** This frame does not want the elliptical float. |
| **The Earth is rigid geometry** | Unlike smoke, the eye can track a hard edge. Any rotation is a clock. | Earth fixed. Motion lives in the fire *on* it, not in the body of it. |

### The walking decision

**Option 1 — they stand.** Backs to camera, still, watching it burn. Identical staging
to A_PhoenixHour, which verified at 1.07×. Lowest risk, known to work. Costs the
"walking toward it" narrative.

**Option 2 — the tracking treadmill.** Camera tracks with them at exactly their pace;
the cypress avenue scrolls past; the Earth, being at infinity, stays fixed. Loops if
the period matches the cypress spacing, because the avenue is self-similar. The
metaphor is the strongest in the project — *forever walking toward the end of the
world and never arriving* is a loop that has a reason to be a loop. Higher risk: the
model must hold the parallax relationship (trees move, Earth does not) and must not
drift, and any error compounds across the shot.

**Recommendation:** ship Option 1. Spend one generation testing Option 2, because if
it lands it is the better piece.

Note that **the keyframe is very nearly the same still either way** — the only
difference is legs mid-stride versus standing. That is why the still can be locked
before this is settled.
