# Token Identity Freeze — `-ain` Family Positional Claims
**Date**: 2026-03-19
**Pilot**: ROSETTA3d (pre-execution freeze)
**Purpose**: Establish canonical token identity for all positionally-biased `-ain` tokens before Stolfi ZL replication proceeds. No replication or annex drafting is valid until this freeze is in effect.

---

## 1. Canonical Token Declarations

### Token A: `laiin`
- **Canonical label**: `laiin`
- **EVA/Takahashi H IVTFF representation**: `l` + `a` + `i` + `i` + `n`
- **Aliases accepted**: none — `laiin` ≠ `laiiin` ≠ `laiin` with alternate vowel length
- **Rejected variants**: `lai!n`, `laiin` normalised to `aiin` — **reject**
- **Stem consonant**: `l` (lam prefix hypothesis: l- prepended to -ain suffix)
- **Section profile in corpus**: S=9, H=1, B=1 (total n=11; 82% Stars)
- **Transcription source**: Takahashi H (all 11 occurrences)

#### Canonical positional claim
| Metric | Value |
|--------|-------|
| Analysis | PILOT5 + ROSETTA3c (calibration re-run) |
| Section scope | Stars (S) packets only |
| n (in-packet occurrences) | 5 |
| Mean relative position | 0.875 |
| p-value (vs. H₀: position = 0.5) | 0.007 |
| Direction | **LATE** |
| Status | **CONFIRMED** (re-confirmed by ROSETTA3c) |

#### Claim ID
`P2-CLAIM-011`

#### Paper sections affected
- Paper 2 §5.2 (PILOT5 positional results)
- Paper 2 §9 (future work: `laiin` alignment to Arabic or Latin -ain targets)
- Annex B.7

---

### Token B: `ai!n`
- **Canonical label**: `ai!n`
- **EVA/Takahashi H IVTFF representation**: `a` + `i` + `!` + `n` (the `!` is a glyph-variant marker in Takahashi H IVTFF notation, distinguishing this character from the standard `aiin` sequence)
- **Aliases accepted**: none — `ai!n` ≠ `aiin` ≠ `ain`
- **Rejected variants**: `aiin` (different token, n=444 in corpus — the most common -ain variant)
- **Stem consonant**: ∅ (no consonant prefix; bare -ain morpheme with glyph marker)
- **Section profile in corpus**: S=40, B=8, P=4, H=2, T=1, C=1 (total n=56; 71% Stars, but present in all sections)
- **Transcription source**: Takahashi H (all 56 occurrences)

#### Canonical positional claim
| Metric | Value |
|--------|-------|
| Analysis | NEW_FINDINGS_2026-03-19 (derived from PILOT5 corpus-wide run) |
| Section scope | All sections (corpus-wide) |
| n (in-packet occurrences) | 23 |
| Mean relative position | 0.686 |
| p-value (vs. H₀: position = 0.5) | 0.005 |
| Direction | **LATE** |
| Status | **CONFIRMED** on Takahashi H; **REPLICATION_PENDING** on Stolfi ZL |

#### P-value discrepancy resolution
PILOT5 log table (line 49) reports `ai!n | 19 | 0.668 | 0.023 | marginally LATE`. This is the **Stars-section-only** result. NEW_FINDINGS and Paper 2 text use the **corpus-wide** result (n=23, mean=0.686, p=0.005). These are not contradictory — they measure different scopes:

| Scope | n | Mean position | p-value | Interpretation |
|-------|---|---------------|---------|----------------|
| Stars packets only | 19 | 0.668 | 0.023 | Marginally significant |
| All sections (corpus-wide) | 23 | 0.686 | 0.005 | Significant |

**Canonical figure for the paper**: corpus-wide (n=23, 0.686, p=0.005). This is what appears in Paper 2 text and what is registered as P2-CLAIM-012. The Stars-only figure (n=19, 0.668, p=0.023) is the subordinate result and should be noted where section-specific analysis is discussed.

#### Claim ID
`P2-CLAIM-012`

#### Paper sections affected
- Paper 2 §5.2 (corpus-wide positional bias)
- Paper 2 §5.3 / §10 (three-layer model; terminal entity marker candidate)
- Annex B.7

---

### Token C: `qokain`
- **Canonical label**: `qokain`
- **EVA/Takahashi H IVTFF representation**: `q` + `o` + `k` + `a` + `i` + `n`
- **Aliases accepted**: none — `qokain` ≠ `qokaiin` ≠ `qokai!n`
- **Note**: `qokaiin` (n=much larger) and `qokai!n` are separate tokens. `qokain` (n=7 in Stars packets) is specifically the short-vowel variant.
- **Stem consonant**: `qk` (qok- = INIT prefix + k consonant)
- **Section profile**: primarily Stars and Balneological

#### Canonical positional claim
| Metric | Value |
|--------|-------|
| Analysis | PILOT5 (Stars) + ROSETTA3c (re-confirmed) |
| Section scope | Stars (S) packets |
| n (in-packet occurrences) | 7 |
| Mean relative position | 0.248 |
| p-value (vs. H₀: position = 0.5) | 0.007 |
| Direction | **EARLY** |
| Status | **CONFIRMED** (PILOT5 + ROSETTA3c re-confirmed) |

#### Claim ID
`P2-CLAIM-010`

#### Paper sections affected
- Paper 2 §5.2 (section-specific positional semantics)
- Paper 2 §9 (future alignment target)
- Annex B.7

---

## 2. Token Separation Proof

These three tokens are distinct glyph sequences in the Takahashi H transliteration:

| Token | Corpus count | Stars count | Is subset of another? |
|-------|-------------|-------------|----------------------|
| `aiin` | 444 | ? | No — separate token |
| `ai!n` | 56 | 40 | No — `!` distinguishes it from `aiin` |
| `laiin` | 11 | 9 | No — `l` prefix distinguishes it from `aiin` |
| `qokain` | ~7 (Stars packets) | ~7 | No — `qok` prefix distinguishes it |

**Ruling**: `laiin` and `ai!n` are NOT aliases. They must not be merged, treated as transcription variants of each other, or referred to interchangeably. They support different claims (P2-CLAIM-011 vs P2-CLAIM-012) with different evidence bases.

---

## 3. Consistency Audit

### Paper 2 TeX — status after v0.94
| Location | Token used | Claim | Assessment |
|----------|-----------|-------|------------|
| §5.2 (line ~379) | `ai!n` n=23, mean=0.686, p=0.005 | P2-CLAIM-012 | **Correct** (corpus-wide) |
| §5.2 (line ~493) | `ai!n` n=23, mean=0.686, p=0.005 | P2-CLAIM-012 | **Correct** |
| §7.3 (line ~518) | `ai!n` mean=0.686, p=0.005 | P2-CLAIM-012 | **Correct** |
| §9 (line ~562) | `qokain` EARLY + `ai!n` LATE | P2-CLAIM-010 + 012 | **Correct** |
| §9 (line ~564) | `qokain` EARLY + `laiin` LATE (Stars) | P2-CLAIM-010 + 011 | **Correct** (Stars-specific pairing) |
| §10 (line ~584) | `qokain` EARLY + `ai!n` LATE | P2-CLAIM-010 + 012 | **Correct** |
| Appendix (line ~677) | `ai!n` LATE corpus-wide | P2-CLAIM-012 | **Correct** |
| CLAIM_TAG block | `laiin LATE Stars` (011) + `ai!n LATE corpus-wide` (012) | Both | **Correct** |

**Assessment**: Paper 2 v0.94 correctly distinguishes `laiin` (Stars-specific) from `ai!n` (corpus-wide). No correction required in the TeX.

### Paper 1 TeX
- No occurrences of `laiin` or `ai!n` in the text. No action required.

### CLAIM_REGISTRY.md
- P2-CLAIM-011: `laiin` LATE Stars (n=5, 0.875, p=0.007) — **correct**
- P2-CLAIM-012: `ai!n` LATE corpus-wide (n=23, 0.686, p=0.005) — **correct**
- Note: p-value in registry should explicitly note that Stars-only result is p=0.023 (n=19) — add as a sub-note.

### PAPER_TO_REPO_MAP.md (§5.2)
- Entry: `laiin LATE (0.875, p=0.007)` — **correct**
- Entry: `ai!n LATE (0.686, p=0.005)` — **correct** (corpus-wide)
- Pending replication table lists both — **correct**

### Pilot logs
- PILOT5 log table (p=0.023 for ai!n): **correct** for Stars-only scope — no edit needed, scope must be labelled
- ROSETTA3c_results.md: lists `laiin LATE` confirmed — **correct**
- NEW_FINDINGS: lists `ai!n` corpus-wide — **correct**

---

## 4. Required Fix: CLAIM_REGISTRY.md P2-CLAIM-012

The claim registry entry for P2-CLAIM-012 should note the scope distinction:

> Stars-only result: n=19, mean=0.668, p=0.023 (marginally significant).
> Corpus-wide result: n=23, mean=0.686, p=0.005 (significant).
> Paper 2 uses corpus-wide figure. Stolfi replication should test both scopes.

---

## 5. Frozen Canonical Values for Replication

The following values are frozen as the EVA/Takahashi H ground truth. Any Stolfi ZL replication must report its own values separately and compare explicitly:

| Claim | Token | n | Mean position | p-value | Scope | Status |
|-------|-------|---|---------------|---------|-------|--------|
| P2-CLAIM-010 | `qokain` EARLY | 7 | 0.248 | 0.007 | Stars packets | CONFIRMED |
| P2-CLAIM-011 | `laiin` LATE | 5 | 0.875 | 0.007 | Stars packets | CONFIRMED |
| P2-CLAIM-012 | `ai!n` LATE | 23 | 0.686 | 0.005 | All sections | CONFIRMED (Takahashi H) |
| P2-CLAIM-012 | `ai!n` LATE | 19 | 0.668 | 0.023 | Stars only | Subordinate result |

---

## 6. Gate Condition

> **Replication and annex drafting may now proceed.**
> Token identity is frozen. All three positional claims are distinct, non-overlapping, and correctly documented in Paper 2 v0.94 and CLAIM_REGISTRY.md. The Stolfi ZL replication task (STOLFI_ZL_POSITIONAL_REPLICATION.md) is cleared to begin.

---

## 7. Affected Claims Summary

| Claim ID | Token | Fix required? |
|----------|-------|--------------|
| P2-CLAIM-010 | `qokain` EARLY Stars | None — identity clear |
| P2-CLAIM-011 | `laiin` LATE Stars | None — identity clear |
| P2-CLAIM-012 | `ai!n` LATE corpus-wide | Add scope note to CLAIM_REGISTRY.md entry |
