# ROSETTA3d: Stolfi ZL Positional Replication
**Date**: 2026-03-19
**Pilot**: ROSETTA3d
**Script**: `scripts/ROSETTA3d_stolfi_zl_replication.py`
**ZL Source**: `data/ZL3b-n.txt` (voynich.nu, version 3b of 13/05/2025, Eva- alphabet)
**Output**: `results/ROSETTA3d_stolfi_zl_results.json`
**Claims tested**: P2-CLAIM-010 (`qokain` EARLY), P2-CLAIM-011 (`laiin` LATE), P2-CLAIM-012 (`ai!n` LATE)

---

## 1. Corpus Comparison

| Property | Takahashi H (IT) | ZL (Zandbergen-Landini) |
|----------|-----------------|--------------------------|
| Alphabet | Eva-T (with `!` glyph markers) | Eva- (standard, no `!`) |
| Total tokens | 37,045 | 37,649 |
| Stars section | ~10,681 | 10,888 |
| Stars packets | 341 | 330 |
| B packets | 374 | 392 |
| Total packets | 896 | 886 |

The ZL corpus has similar scale to Takahashi H, validating section boundary assignments.

---

## 2. Transcription Divergence: The `!` Marker Problem

The Takahashi H (Eva-T) transliteration encodes a glyph-level distinction using `!`. In ZL (Eva-), this distinction is not encoded. This causes systematic token mapping differences:

| Takahashi H token | ZL token | Evidence |
|-------------------|----------|---------|
| `qokai!n` (n=92 Stars) | `qokain` | f111v count: Takahashi `qokai!n`=24, ZL `qokain`=24 — exact match |
| `qokain` (n=12 Stars) | absorbed into ZL `qokain` | No ZL-separable equivalent |
| `ai!n` (n=56 corpus) | does not exist in ZL | Count=0 in ZL |
| `okai!n`, `lkai!n`, etc. | `okain`, `lkain`, etc. | Pattern holds throughout |

**Critical result**: ZL `qokain` = Takahashi H `qokai!n`, not Takahashi H `qokain`. The two are conflated in ZL.

---

## 3. Token-Level Positional Analysis (Takahashi H, Stars packets, n=341)

Run before ZL comparison to establish the full family picture:

| Token | n in Stars pkts | Mean position | p (t-test vs 0.5) | Direction |
|-------|-----------------|---------------|-------------------|-----------|
| `qokain` (no !, P2-CLAIM-010) | **7** | **0.248** | **0.007** | **EARLY** |
| `qokai!n` (! variant) | 39 | 0.510 | 0.841 | CENTRAL |
| `qokaiin` (double-i) | 60 | 0.476 | 0.550 | CENTRAL |
| qok-ain family (all three) | **106** | **0.473** | **0.365** | **CENTRAL** |
| `laiin` (P2-CLAIM-011) | **5** | **0.875** | **0.007** | **LATE** |
| `ai!n` (P2-CLAIM-012) | 19 | 0.668 | 0.023 | LATE (marginal) |

**Internal family test**: The qok-ain grouped test (n=106) is CENTRAL (p=0.365). The EARLY bias in `qokain` (n=7) does not generalize to the `qokai!n` variant (n=39, CENTRAL) or the full family.

---

## 4. ZL Positional Test Results

### Test 1: P2-CLAIM-010 — `qokain` EARLY in Stars

| | Takahashi H | ZL |
|--|-------------|-----|
| Token | `qokain` (no !) | `qokain` (= Takahashi `qokai!n`) |
| n in Stars packets | 7 | 22 |
| Mean position | 0.248 | 0.605 |
| p-value | 0.007 | 0.234 |
| Direction | EARLY | CENTRAL |

**Verdict**: `TRANSCRIPTION_MISMATCH`

Reason: ZL `qokain` corresponds to Takahashi H `qokai!n` (confirmed by f111v count match), NOT to Takahashi H `qokain`. The ZL test is testing a different token. The Takahashi H `qokain` (no `!`) has no isolable ZL equivalent. Cross-transcription test is not possible.

### Test 2: P2-CLAIM-011 — `laiin` LATE in Stars

| | Takahashi H | ZL |
|--|-------------|-----|
| Token | `laiin` | `laiin` |
| Total in corpus | 11 | 13 |
| In Stars section (total) | 9 | 7 |
| In Stars packet payloads | 5 | **0** |
| Mean position | 0.875 | N/A |
| p-value | 0.007 | N/A |

**Verdict**: `TRANSCRIPTION_MISMATCH / INSUFFICIENT_N`

Reason: ZL has 7 `laiin` tokens in Stars section but none appear in packet payloads. Investigation shows ZL sometimes splits `laiin` into `l` + `aiin` (f111v: `l`=11 separately, vs Takahashi H `laiin`-derived tokens). The different paragraph boundary and word-split conventions in ZL render `laiin` undetectable in packet contexts. Cross-transcription test is not possible.

### Test 3: P2-CLAIM-012 — `ai!n` LATE corpus-wide

| | Takahashi H | ZL |
|--|-------------|-----|
| Token | `ai!n` | does not exist |
| Count | 56 | 0 |

**Verdict**: `TRANSCRIPTION_MISMATCH`

Reason: `!` is a Takahashi H Eva-T glyph marker with no ZL Eva- equivalent. ZL `aiin` (n=489) is a different token.

---

## 5. Internal Signal Fragility — P2-CLAIM-010

The qok-ain family analysis reveals that the `qokain` EARLY signal is confined to the rare no-`!` variant (n=7) and does not appear in the larger `qokai!n` variant (n=39, CENTRAL). This creates a methodological concern:

- If `qokain` and `qokai!n` represent the same underlying glyph with a scribal variant (the `!` being a spacing or stroke marker rather than a meaningful distinction), then the EARLY bias is a small-sample artifact.
- If the `!` encodes a meaningful phonological or morphological distinction, the EARLY bias is valid for the specific variant.
- The ZL transcription, which makes no such distinction, provides circumstantial evidence for the first interpretation.

**Conclusion**: P2-CLAIM-010 should be downgraded from `CONFIRMED` to `PROVISIONAL` pending:
1. Clarification of what the `!` marker encodes in Takahashi H (is it a meaningful distinction or a formatting artifact?)
2. A transcription that preserves the distinction with independent glyph-level annotation

---

## 6. Summary Table

| Claim | EVA result | ZL result | Verdict | Status change |
|-------|-----------|-----------|---------|---------------|
| P2-CLAIM-010 `qokain` EARLY Stars | n=7, 0.248, p=0.007 | TRANSCRIPTION_MISMATCH; family test CENTRAL (n=106, p=0.365) | TRANSCRIPTION_MISMATCH | `CONFIRMED` → `PROVISIONAL` |
| P2-CLAIM-011 `laiin` LATE Stars | n=5, 0.875, p=0.007 | 0 in Stars pkts | TRANSCRIPTION_MISMATCH / INSUFFICIENT_N | `CONFIRMED` → `CONFIRMED, CROSS-TRANSCRIPTION PENDING` |
| P2-CLAIM-012 `ai!n` LATE corpus-wide | n=23, 0.686, p=0.005 | ! not in ZL | TRANSCRIPTION_MISMATCH | `CONFIRMED` → `CONFIRMED, CROSS-TRANSCRIPTION PENDING` |

---

## 7. Next Steps

1. **For P2-CLAIM-010**: Obtain a third transliteration (e.g., GC v101 or RF Extended Eva) that encodes the `!`/no-`!` distinction separately. Test if the same n=7 EARLY result holds. If no third transliteration encodes this distinction, the claim must remain PROVISIONAL.

2. **For P2-CLAIM-011**: ZL splits `laiin` → `l` + `aiin` in some contexts. Test `l` immediately followed by R2 in Stars packets as a proxy, or use a transliteration that treats `laiin` as a single token.

3. **For P2-CLAIM-012**: Requires an Eva-T compatible transliteration. The RF (Reference) or IT (Takahashi original) extended format may be usable.

4. **Immediate action**: Update CLAIM_REGISTRY.md to reflect the downgrade of P2-CLAIM-010 and the CROSS-TRANSCRIPTION_PENDING status for P2-CLAIM-011 and P2-CLAIM-012.

---

## 8. Methodological Lessons

- **Eva-T vs Eva-**: Takahashi H encodes glyph-level distinctions (via `!`) absent from ZL Eva-. Claims built on Eva-T-specific tokens cannot be replicated on Eva- transcriptions.
- **Token granularity matters**: The EARLY bias in `qokain` (no !) disappears at the family level (`qok-ain`, n=106, CENTRAL). Low-n findings in specific variant tokens are vulnerable to transcription normalization.
- **ZL is a valid but limited cross-check**: The ZL corpus covers similar folios and has comparable section distributions, making it an excellent cross-check for section-level structural claims. But it cannot replicate claims built on Takahashi H's extra glyph distinctions.
