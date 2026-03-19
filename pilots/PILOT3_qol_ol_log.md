# PILOT3 — qol/ol Inner-Packet Doublet Test
**Phase 2 Step 6**
**Date**: 2026-03-19

---

## Summary

| Metric | Result |
|--------|--------|
| Complete packets detected (R1→payload→R2) | 941 |
| Corpus tokens in packet payloads | 10,131 (27.3%) |
| qol total occurrences | 145 |
| qol inside packet payloads | 55 (37.9%) |
| qol expected inside (if random) | 39.7 |
| **qol payload enrichment** | **1.39×** |
| qol mean relative position in payload | 0.558 (central, no bias; p=0.23) |
| qol + ol paragraph co-occurrence | OR=64.6, **p<0.0001** |

---

## Layer 2 Variant Comparison

| Token | Total | In payload | Rate | vs baseline | Classification |
|-------|-------|-----------|------|------------|---------------|
| `qol` | 145 | 55 | 0.379 | **1.39×** | Inner-packet function word ✓ |
| `kal` | 22 | 7 | 0.318 | 1.16× | Borderline |
| `kol` | 35 | 4 | 0.114 | **0.42×** | NOT inner-packet |
| `okol` | 75 | 15 | 0.200 | **0.73×** | NOT inner-packet |
| `ol` (structural R6) | 504 | 195 | 0.387 | **1.41×** | Reference (classified structural) |

---

## Key Findings

### 1. qol is elevated inside packet payloads (1.39×)
`qol` appears in packet payloads at 1.39× the rate expected by chance. The structural R6 token `ol` is elevated at 1.41× — nearly identical. This near-equality is the most striking finding: `qol` behaves inside packets the same way the classified structural `ol` does.

### 2. qol + ol paragraph co-occurrence is highly significant
Of 923 paragraphs, 36 contain both `qol` and `ol`. Fisher exact test: OR=64.6, p<0.0001. This is not a co-occurrence by proximity (they are not adjacent within packets); it is a paragraph-level distribution pattern. Both tokens prefer the same paragraphs.

### 3. qol is not positionally biased within payloads
Mean relative position = 0.558 (not significantly different from 0.5; t-test p=0.23). `qol` is not a packet-initial or packet-final function word — it appears throughout the payload.

### 4. kol and okol are DEPLETED inside packets
Despite their Hebrew `kol` alignment, `kol` (0.42×) and `okol` (0.73×) are actually less common inside packets than expected. They are NOT inner-packet function words by this criterion. Only `qol` (and marginally `kal`) qualify.

---

## Verdict

**qol as inner-packet function word: SUPPORTED**

The evidence is consistent with `qol` being a content-layer functional doublet of structural `ol`:
- Both are elevated inside packet payloads at nearly identical rates (1.39× vs 1.41×)
- Both concentrate in the same paragraphs (OR=64.6, p<0.0001)
- Both concentrate in the Balneological section (77% for `qol`; `ol` is R6-REF)
- `qol` appears throughout packet payloads (not biased to start or end)

**The proposed phonological alignment (qol = Hebrew kol, all/every) remains a hypothesis** — the within-packet enrichment is consistent with a function-word interpretation but does not confirm the specific Hebrew reading. `kol` and `okol` (also Hebrew kol candidates) are depleted inside packets, which complicates the Hebrew kol identification.

**Three-layer model: SUPPORTED at structural level**
- Layer 1 (frame): `ol` (R6-classified) — 1.41× inside packets
- Layer 2 (inner-function): `qol` (content-classified) — 1.39× inside packets
- The binary structural/content boundary is insufficient; `qol` crosses it

---

## Status

**qol inner-packet enrichment**: CONFIRMED (1.39×, vs baseline 1.0)
**qol/ol paragraph co-occurrence**: CONFIRMED (OR=64.6, p<0.0001)
**qol positional bias**: NOT CONFIRMED (central, p=0.23)
**Hebrew kol alignment for qol specifically**: CANDIDATE (structural support only)
**kol/okol as inner-packet function words**: NOT SUPPORTED (depleted)

---

## Files
- `PILOT3_qol_ol_doublet.py` — analysis script
- `PILOT3_qol_ol_results.json` — raw results
- `PILOT3_qol_ol_log.md` — this file
