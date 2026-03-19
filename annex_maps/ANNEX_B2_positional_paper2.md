# Annex B.2 — Positional Claims, Paper 2
**Table**: Proof table for all token-level and family-level within-packet positional claims (Paper 2).
**Source**: `docs/CLAIM_REGISTRY.md`; `pilots/ROSETTA3d_20260319/STOLFI_ZL_POSITIONAL_REPLICATION.md`
**Primary paper**: Mumin (2026b) — Transition Grammar and Cognitive Domain Profiles

---

## B.2a — Token-level positional bias tests (PILOT5 + ROSETTA3c)

Packet-internal position is defined as: `slot_index / (packet_length - 1)` where 0 = immediately after R1 (EARLY) and 1 = immediately before R2 (LATE). Packets with length ≤ 1 (no payload) are excluded.

**Test**: Wilcoxon signed-rank vs H₀ = 0.5 (central/unbiased).
**Null model**: Packet-internal position = 0.5 (random placement within payload).
**n**: Stars-section complete R1→payload→R2 packets (ROSETTA3c consistent FSA reconstruction).

| Claim ID | Level | Token | Stars n | Mean pos. | p | Direction | Status | TC | Interpretation Bound | Repo Artifact |
|----------|-------|-------|---------|-----------|---|-----------|--------|-----|---------------------|---------------|
| P2-CLAIM-010 | TOKEN-LEVEL | `qokain` (no `!`) | 7 | 0.248 | 0.007 | EARLY | `PROVISIONAL` | `TRANSCRIPTION-BOUND` | Signal confined to n=7 rare no-`!` variant. Larger `qokai!n` (n=39) CENTRAL (p=0.841). Full qok-ain family (n=106) CENTRAL (p=0.365). **Cannot test in ZL Eva-**: ZL collapses `qokain`+`qokai!n` → different token. Requires 3rd transliteration encoding `!` separately. | `scripts/ROSETTA3c_qotaiin_positional.py` + `scripts/ROSETTA3d_stolfi_zl_replication.py` |
| P2-CLAIM-011 | TOKEN-LEVEL | `laiin` | 5 | 0.875 | 0.007 | LATE | `CONFIRMED` + `CROSS-TRANSCRIPTION_PENDING` | `NOT_TESTABLE_ACROSS_ZL` | ROSETTA3c re-confirmed. ZL has 0 `laiin` in Stars packet payloads (token-splitting in ZL paragraph conventions). Absence in ZL payloads ≠ falsification — it is a packet-structure accessibility mismatch. | `scripts/ROSETTA3c_qotaiin_positional.py` |
| P2-CLAIM-012 | TOKEN-LEVEL | `ai!n` | 19 (Stars) / 23 (corpus-wide) | 0.668 (Stars) / 0.686 (corpus-wide) | 0.023 (Stars) / 0.005 (corpus-wide) | LATE | `CONFIRMED` + `CROSS-TRANSCRIPTION_PENDING` | `NOT_TESTABLE_ACROSS_ZL` | **Corpus-wide figure** (n=23, p=0.005) is the canonical Paper 2 result. `ai!n` ≠ `aiin` (n=444) ≠ `laiin` (n=11). The `!` marker is Eva-T-specific. ZL has 0 `ai!n` occurrences. Cross-transcription testing requires Eva-T compatible source. | `scripts/PILOT5_ain_subfolio_analysis.py` |
| P2-CLAIM-020 | TOKEN-LEVEL | `qotaiin` | 16 | 0.543 | 0.388 | CENTRAL | `CONFIRMED` (null) | `DIRECT` | No positional slot detected. Tier 3 assignment: consonant selectivity only. No positional evidence for entity-label or temporal function. | `scripts/ROSETTA3c_qotaiin_positional.py` → `results/ROSETTA3c_qotaiin_positional_results.json` |
| P2-CLAIM-021 | TOKEN-LEVEL | `lkaiin` | 15 | 0.506 | 0.943 | CENTRAL | `CONFIRMED` (null) | `DIRECT` | No positional slot. Tier 2: lk consonant stem ambiguous between Arabic astro and Latin *lacus*. Positional evidence does not discriminate. See RETRACTED-004 for retracted *lacus* primary reading. | `scripts/ROSETTA3c_qotaiin_positional.py` |

---

## B.2b — qok-ain family positional summary (token-level vs. family-level)

This table shows the full qok-ain family breakdown, making explicit which claim level applies to each result.

| Token | Level | Stars n | Mean pos. | p | Direction | Status | Note |
|-------|-------|---------|-----------|---|-----------|--------|------|
| `qokain` (no `!`) | TOKEN-LEVEL | 7 | 0.248 | 0.007 | EARLY | PROVISIONAL | The claim in P2-CLAIM-010; transcription-bound; signal fragile |
| `qokai!n` (`!`-marked) | TOKEN-LEVEL | 39 | 0.517 | 0.841 | CENTRAL | CONFIRMED (null) | Larger variant; CENTRAL in Stars |
| `qokaiin` (double-i) | TOKEN-LEVEL | 60 | ~0.50 | ~0.36 | CENTRAL | CONFIRMED (null) | Most frequent qok-ain variant |
| `qok-ain` family (all three) | FAMILY-LEVEL | 106 | ~0.496 | 0.365 | CENTRAL | CONFIRMED (null) | Family-level null: EARLY signal is variant-specific only |

**Key finding**: The EARLY bias is a property of the specific no-`!` `qokain` variant (n=7), not of the qok-ain family. Family-level and larger-n tests are CENTRAL.

---

## B.2c — qol first-payload positional claim

| Claim ID | Level | Token | Scope | n | Test | Control | Observed | p | Status | TC | Bound | Repo |
|----------|-------|-------|-------|---|------|---------|----------|---|--------|-----|-------|------|
| P2-CLAIM-006 | TOKEN-LEVEL | `qol` | B-section packets (first-payload slot) | B packets | Fisher exact (first-payload slot rate) | Section-specific baseline rates across H, S, P | OR = 7.83 for B first-payload slot vs. other sections | p < 0.01 | `CONFIRMED` | `DIRECT` | `qol` is inner-packet function word in B; leads payload content. Not a lexical entity per se. Distinguished from structural `ol` (R6) by positional context. | `scripts/DECODE3_qol_cluster.py` → `results/DECODE3_qol_results.json` |

---

## Notes on this table

1. **Token identity freeze**: `ai!n` ≠ `aiin` ≠ `laiin` in Takahashi H. These are three distinct token strings with distinct counts (56, 444, 11 total corpus occurrences respectively). See `pilots/ROSETTA3d_20260319/TOKEN_IDENTITY_FREEZE.md`.

2. **ZL boundary test**: The ZL replication (ROSETTA3d) was a boundary test on token comparability, not a direct null replication. See `docs/TRANSCRIPTION_SENSITIVITY_METHOD.md` for the three failure modes and the full taxonomy.

3. **Packet reconstruction method**: ROSETTA3c consistent FSA reconstruction: payload stops only at R2 (not R1); INIT-bleed tokens (qok- tokens appearing in payload) are included in the payload and counted in positional analysis. This is consistent with P2-CLAIM-010 having n=7 despite qok- being primarily an R1 token (it appears in Stars payloads at low rate).

4. **p-value scope (P2-CLAIM-012)**: Stars-only scope (n=19, p=0.023) is marginal. Corpus-wide scope (n=23, p=0.005) is the canonical figure in Paper 2. Both scopes should be reported in any replication attempt.
