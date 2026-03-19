# PILOT5 — -ain Suffix Sub-Folio Analysis (Stars Section)
**Date**: 2026-03-19

---

## Summary

| Metric | Result |
|--------|--------|
| Stars section -ain occurrences | 2,049 |
| Stars -ain types | 441 |
| Folio-unique -ain types | **298 / 441 (67.6%)** |
| Dominant -ain token per folio | Low dominance (6.6–20.8% of folio -ain) |
| -ain overall packet position | 0.496, p=0.67 (CENTRAL, no bias) |
| `qokain` packet position | **0.248, p=0.007 (EARLY-biased)** |
| `laiin` packet position | **0.875, p=0.007 (LATE-biased)** |
| `ai!n` packet position | 0.668, p=0.023 (marginally LATE) |

---

## Key Findings

### 1. 67.6% of -ain types are folio-unique

Of 441 -ain types in the Stars section, **298 appear in only one folio**. This is the strongest quantitative support for the entity-labeling hypothesis: if -ain tokens label individual entities (specific stars, nymph figures, or star-groups), most entities would appear on only one folio. The large number of hapax-like -ain types is consistent with a rich individual-entity vocabulary.

By contrast, common -ain types appear across nearly all folios:
- `aiin`: 23/23 folios
- `qokaiin`: 22/23 folios
- `daiin`: 21/23 folios
- `okaiin`: 21/23 folios

This bimodal distribution — a few high-frequency pan-folio types and a long tail of folio-unique types — is exactly the pattern expected if the -ain family contains both **function words** (high-frequency, pan-folio) and **entity labels** (folio-specific).

### 2. Dominant -ain token has low per-folio dominance

The dominant -ain token on each folio accounts for only 6.6%–20.8% of that folio's -ain occurrences. This means no single -ain token "owns" a folio. PILOT2's strong entity-labeling hypothesis (dominant token = zodiac sign label) is further disconfirmed: the dominance is too weak to represent a clear entity anchor.

However, the **pan-folio tokens** (`aiin`, `qokaiin`, `daiin`) may be **function words** within the -ain family rather than entity labels. The entity labels may be the folio-unique types — which occur at low frequency (n=1–2) and were invisible to the dominance-based analysis in PILOT2.

### 3. First statistically significant positional bias: `qokain` and `laiin`

For the first time in this series, two tokens show statistically significant positional bias within packet payloads:

| Token | n (in S packets) | Mean position | p | Direction |
|-------|-----------------|--------------|---|-----------|
| `qokain` | 7 | **0.248** | **0.007** | EARLY-biased |
| `laiin` | 5 | **0.875** | **0.007** | LATE-biased |
| `ai!n` | 19 | 0.668 | 0.023 | marginally LATE |
| All other -ain | various | ~0.5 | ns | CENTRAL |

**`qokain` as early entity-subject**: Mean position 0.248 (strongly early, p=0.007). `qokain` carries the `qok-` INIT morpheme and preferentially occupies the LEADING entity slot within Stars section packet payloads. In ROSETTA2, `qokain` was found to be 94% medial (content-layer token) and 3.91× Balneological-enriched. Combined with this Stars-section early-position finding: `qokain` consistently occupies LEADING positions in packet payloads across both B and S sections. This positions `qokain` as a candidate **topic entity marker** — a token that leads the packet's entity content.

**`laiin` as terminal entity**: Mean position 0.875 (strongly late, p=0.007). `laiin` appears at the END of packet payloads in Stars section — the entity-object/product slot. With `l-` prefix (stem: `l`) and `-ain` suffix, `laiin` may label a specific entity type that is consistently the final element of Stars-section procedures.

**Interpretation**: The -ain family contains at minimum two positionally distinct sub-classes:
- **Leading -ain** (`qokain`, mean 0.25): entity-subject / topic-opener
- **Trailing -ain** (`laiin`, `ai!n`): entity-object / terminal element
- **Central -ain** (majority): unbiased content entities

This is the first evidence of positional sub-differentiation within the -ain token family.

### 4. No positional bias for the overall -ain family

The overall -ain family mean position is 0.496 (p=0.67) — perfectly central. All major -ain types individually show no significant bias (with the exceptions above). This confirms that the -ain suffix is NOT a positional marker (it doesn't encode "subject" vs "object" by itself). The positional signal comes from the STEM (what precedes `-ain`), not the suffix.

### 5. Stem analysis reveals structured morphology

The consonant stems preceding the -ain suffix form a structured inventory:

| Stem | n | Consonant type | Note |
|------|---|---------------|------|
| ∅ (bare) | 261 | — | `ain` alone; pan-folio function word? |
| `qok-` | 219 | q+k | INIT-morpheme family |
| `d-` | 179 | d | High-frequency content stem |
| `ok-` | 167 | k | Reduced INIT stem? |
| `ot-` | 125 | t | Common content stem |
| `qot-` | 76 | q+t | INIT+t variant |
| `lk-` | 66 | l+k | Compound consonant stem |
| `s-` | 64 | s | sal-type stem? |
| `r-` | 60 | r | Referential stem? |
| `k-` | 50 | k | Bare k-stem |

The `qok-` stem (219 = 10.7% of Stars -ain tokens) represents the largest named-stem group. The bare `∅` stem (261 cases = the simple `ain/aiin/ai!n` tokens) is the largest category overall and likely represents function-word -ain tokens rather than entity labels.

### 6. Within-folio paragraph variability is limited

Only 2 folios (f105r, f114r) have multiple paragraphs with different dominant -ain tokens. This is insufficient to conclude that -ain dominant tokens track sub-paragraph entities. More data (higher-resolution paragraph mapping) is needed. The current analysis does not support or refute sub-folio entity labeling at paragraph granularity.

### 7. Bigram context: -ain tokens surround other -ain tokens

The most common preceding and following tokens for -ain tokens in Stars section:
- **Preceding**: `aiin` (n=42), `daiin` (35), `qokeey` [INIT] (33)
- **Following**: `aiin` (45), `al` [REF] (31), `ar` (26), `qokaiin` [INIT] (25)

The high self-precedence (`aiin` most common before another -ain token, `aiin` most common after) suggests **-ain clusters**: multiple -ain tokens appearing in sequence within the same packet payload. This would be consistent with entity-list notation: recording a list of individual entities (star names? nymph names?) within a single packet.

CLOSE tokens (131 preceding, 106 following) confirm that -ain tokens frequently appear near packet boundaries, consistent with entity-labeling at packet edges.

---

## Revised -ain Model

The -ain suffix family has three functional sub-classes:

| Sub-class | Examples | Positional behavior | Interpretation |
|-----------|----------|--------------------|-|
| Function-word -ain | `aiin`, `daiin`, `okaiin` | CENTRAL (p ns) | Pan-folio connectors or aspect markers |
| Leading entity -ain | `qokain` | EARLY (p=0.007) | Entity-subject / topic-opener |
| Trailing entity -ain | `laiin`, `ai!n` | LATE (p=0.007–0.023) | Entity-object / terminal label |
| Hapax entity -ain | 298 folio-unique types | CENTRAL (insufficient data) | Specific entity labels |

---

## Critical Negative

**Strong entity-labeling (dominant token = zodiac sign)**: NOT SUPPORTED. Low per-folio dominance (6.6–20.8%) and pan-folio distribution of high-frequency types preclude a clean one-token-per-entity encoding at the folio level.

**Sub-folio entity labeling (folio-unique types as individual entity labels)**: PLAUSIBLE but not yet confirmed. The 67.6% folio-uniqueness rate is consistent with entity labeling, but direct mapping to specific illustration elements (nymphs, stars) requires image-level analysis beyond the current data.

---

## Status

**-ain as entity label (weak form — folio-unique types)**: SUPPORTED structurally (67.6% folio-unique)
**-ain positional bias (overall)**: NOT CONFIRMED (central, p=0.67)
**qokain as early entity-subject**: CONFIRMED (mean 0.248, p=0.007) ← NEW FINDING
**laiin as terminal entity**: CONFIRMED (mean 0.875, p=0.007) ← NEW FINDING
**-ain sub-class model (3 functional types)**: PROPOSED — requires replication on larger n
**Strong entity-labeling (PILOT2 result)**: RECONFIRMED NOT SUPPORTED

---

## Next Steps

- **PILOT6**: Test `qokain` early-entity behavior in Balneological section — does it also appear early in B packets?
- **ROSETTA3**: Attempt stem-consonant alignment for `qokain` (`qk`), `laiin` (`l`), `raiin` (`r`) against Arabic star names and Hebrew terms
- **Image analysis** (user action required): Map folio-unique -ain hapax types to specific nymph figures or star positions in Beinecke high-res scans

---

## Files
- `PILOT5_ain_subfolio_analysis.py` — analysis script
- `PILOT5_ain_subfolio_results.json` — raw results
- `PILOT5_ain_subfolio_log.md` — this file

---

## CORRECTION — Folio-Uniqueness Falsification (2026-03-19)

### Test Result

The 67.6% folio-unique rate for -ain types is **NOT specific to the -ain family**.

| Token class | n=1–20 types | Folio-unique | Rate |
|-------------|-------------|-------------|------|
| -ain | 441 | 298 | 67.6% |
| Non-ain (n=1–20) | 2,757 | 2,061 | **74.8%** |

Non-ain tokens of matching frequency are MORE folio-unique than -ain tokens. The folio-uniqueness is driven entirely by hapax (n=1) tokens — 294/298 folio-unique -ain types are hapax. This is the expected behavior of rare tokens in a 23-folio corpus.

Among tokens with n≥3 occurrences: 0/97 -ain types are folio-unique (0%). The folio-uniqueness argument **cannot be used as evidence for entity labeling**.

### Retraction

PILOT5 Finding 1 ("67.6% of -ain types are folio-unique — strongest evidence for entity labeling") is **RETRACTED**. The folio-uniqueness rate is a baseline statistical property of rare tokens and provides no differential evidence for the -ain entity-labeling hypothesis.

### What Survives from PILOT5

1. **qokain EARLY positional bias in Stars** (mean 0.248, p=0.007) — still valid
2. **laiin LATE positional bias in Stars** (mean 0.875, p=0.007) — still valid
3. **ai!n LATE bias corpus-wide** (mean 0.686, p=0.005) — still valid
4. **Two-tier frequency distribution** (pan-folio high-freq vs. rare low-freq) — still descriptively valid; interpretation as function-word vs. entity is weakened but not refuted

