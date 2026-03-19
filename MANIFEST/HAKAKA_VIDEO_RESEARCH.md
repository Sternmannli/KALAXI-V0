# HAKAKA VIDEO SCRIPT — AI Video Generation Research

> Researched: 2026-03-19 by V-002
> Directive: V-001 tried once to make the Hakaka story as 10-second AI-generated video segments
> Status: RESEARCH COMPLETE. Execution awaits V-001 GO.

---

## THE APPROACH (One Sentence)

Generate 53 key frames in Midjourney V7 first (total visual control), then animate each with Hailuo/Minimax ($0.52 per clip) or Luma Ray3 (painterly quality). Never go text-to-video directly — image-to-video via curated stills gives far more consistent results for a 53-chapter series.

---

## TOOL RANKING FOR HAKAKA (mythic, primal, painterly, stone-and-bone)

### Tier 1 — Strongest Fit

| Tool | Why | Cost | Limitation |
|------|-----|------|-----------|
| **Minimax/Hailuo 2.3** | Explicit illustration/ink wash style support. Cheapest API ($0.52/clip). | Free tier + $9.99/mo standard | 768p max resolution |
| **Pika** | 27 creative styles, non-photorealistic by design. | $10/mo (700 credits) | Max 5s per generation (chain clips) |
| **Luma Ray3.14** | Painterly output, keyframe control, 20s clips, HDR. | $30/mo (~120 generations) | Higher tier needed for production |
| **Seedance 2.0** (ByteDance) | Style transfer from reference images — feed one Hakaka key image, carries aesthetic forward. | ~Half the cost of Veo 3 | Newer, less tested for series |

### Tier 2 — Good with Prompting

| Tool | Why | Cost | Limitation |
|------|-----|------|-----------|
| Runway Gen-4.5 | Reference image character consistency. Top benchmark (1,247 Elo). | $28/mo Pro | Leans cinematic/photorealistic |
| Sora 2 | Style presets + character lock. | $200/mo Pro for 1080p | Not budget-friendly |

### Tier 3 — Possible

| Tool | Why | Cost | Limitation |
|------|-----|------|-----------|
| Kling AI | Good motion, 3-min clips. | $10/mo | Photorealism bias |
| Open source (Wan/ComfyUI) | Free, LoRA training for style lock. | GPU costs only | Steep learning curve, slower |

---

## RECOMMENDED WORKFLOW

### Phase A — Still Frames (1-2 days)

Midjourney V7 ($10/mo). Generate 53 key frames, one per chapter. Each frame captures the core image in target style (mythic, painterly, ash/stone/river/knot). These become the visual bible.

### Phase B — Animation

**Path 1 (Budget — ~$40 total for all 53):**
Midjourney stills → Hailuo/Minimax animation. 53 clips × $0.52 = ~$28. Plus $10 Midjourney. Under $40 for the entire series.

**Path 2 (Quality — ~$40-50/mo):**
Midjourney stills → Luma Ray3.14. Standard plan ($30/mo) gives ~120 generations. All 53 in one month with room for re-rolls.

**Path 3 (Maximum control — no recurring cost):**
Midjourney stills → ComfyUI + Wan/HunyuanVideo locally. Train a LoRA on Hakaka reference images. Requires GPU.

### Phase C — Post-Production

DaVinci Resolve (free). Sequence clips. Add audio separately. Uniform color grading across all 53.

---

## MAINTAINING CONSISTENCY ACROSS 53 SEGMENTS

1. **Visual bible:** 5-10 reference images defining the Hakaka world (stone textures, ash palette, river, knot, the girl, the cocoon)
2. **Frame-to-frame chaining:** Last frame of each clip = reference for the next. Prevents drift.
3. **Short shots:** 5-10s per chapter. Shorter = less drift.
4. **Consistent prompting:** Same base descriptors, same palette words, same camera behavior across all 53.
5. **Style locking:** Seedance style transfer, or Runway character reference, or LoRA training.
6. **Never change model mid-series.**

---

## COST SUMMARY

| Path | Total Cost | Quality | Effort |
|------|-----------|---------|--------|
| Midjourney + Hailuo | ~$40 one-time | Good (illustration native) | Low |
| Midjourney + Luma | ~$40-50/month × 1 | High (painterly) | Medium |
| Midjourney + local (ComfyUI) | ~$10/mo + GPU | Variable | High |
| Midjourney + Sora Pro | ~$210/month | High | Medium |

---

## SOURCES

- Pinggy: Best Video Generation AI Models 2026
- Pxz.ai: Veo 3.1 vs Top AI Video Generators 2026
- DataCamp: Runway Gen 4.5
- Minimax.io: Hailuo 2.3 Announcement
- LumaLabs.ai: Ray3
- WaveSpeed.ai: Sora 2 Complete Guide 2026
- Neolemon: How to Create Consistent Characters in AI Videos
- LongStories.ai: Maintaining Style Across AI-Generated Video Series
- OpenCreator.io: Seedance vs Veo vs Sora vs Wan Comparison

---

*[V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]*
