# Annex B.5 — Replication and Cross-Transcription Outcomes
**Table**: Summary of all cross-transliteration tests and their outcomes under the ROSETTA3d boundary-test framework.
**Source**: `pilots/ROSETTA3d_20260319/STOLFI_ZL_POSITIONAL_REPLICATION.md`; `docs/TRANSCRIPTION_SENSITIVITY_METHOD.md`
**Primary paper**: Mumin (2026b) — Paper 2 §4.4 (cross-transliteration evaluation)

---

## B.5a — Corpus-level cross-transliteration comparison

| Feature | Takahashi H (Eva-T) | ZL (Eva- basic) | Difference | TC Status | Verdict |
|---------|---------------------|-----------------|------------|-----------|---------|
| Total corpus tokens | 37,045 | 37,649 | +1.6% | DIRECT | Consistent; minor tokenization differences |
| Assigned cluster tokens | ~19,317 (52.1%) | — | — | DIRECT | — |
| Total packet count (FSA reconstruction) | 896 | 886 | −1.1% | `CROSS-TRANSCRIPTION_COMPARABLE` | Packet grammar stable across transliterations |
| B-section packet fraction | 374/897 = 41.7% | Consistent | — | `DIRECT` | B-section structural intensity confirmed in ZL |
| R1/R2 positional percentages (Pearson r) | — | r = 0.937 | — | `CROSS-TRANSCRIPTION_COMPARABLE` | Structural role profiles stable; P1-CLAIM-004 |
| Raw cluster counts (Pearson r) | — | r = 0.999 | — | `CROSS-TRANSCRIPTION_COMPARABLE` | Near-perfect count stability |

---

## B.5b — Token-level cross-transliteration comparison (ROSETTA3d)

**Method**: ZL packet reconstruction using same ROSETTA3c-consistent FSA (payload stops at R2 only; role_map from `results/p1_1_cluster_frequencies.csv` via Takahashi H corpus). Stars-section packets only.

**Critical finding**: ZL Eva- does not encode the `!` glyph-variant marker. This creates three distinct failure modes (see column "TC Status" and "Why ZL cannot replicate").

| Token (Takahashi H) | Takahashi H Stars n | Takahashi H mean | Takahashi H p | Takahashi H direction | ZL token | ZL Stars n | ZL mean | ZL p | ZL direction | TC Status | Why ZL cannot replicate | Claim ID |
|---------------------|---------------------|-----------------|--------------|----------------------|----------|------------|---------|------|--------------|-----------|------------------------|----------|
| `qokain` (no `!`) | 7 | 0.248 | 0.007 | EARLY | `qokain` (= Takahashi `qokai!n`) | 22 | 0.605 | 0.234 | CENTRAL | `TRANSCRIPTION-BOUND` | ZL `qokain` is NOT Takahashi `qokain`. ZL collapses `qokain`+`qokai!n` into one token. Confirmed by f111v count: Takahashi `qokai!n`=24, ZL `qokain`=24 — exact match. The EARLY signal is a property of the no-`!` variant; ZL tests the `!`-marked variant. Different objects. | P2-CLAIM-010 |
| `qokai!n` (`!`-marked) | 39 | 0.517 | 0.841 | CENTRAL | same as ZL `qokain` | (merged) | — | — | — | `TRANSCRIPTION-BOUND` | ZL cannot separate `qokain` from `qokai!n` — they are collapsed into one token | (see P2-CLAIM-010) |
| `qokaiin` (double-i) | 60 | ~0.50 | ~0.36 | CENTRAL | `qokaiin` | comparable | CENTRAL | — | CENTRAL | `DIRECT` | Testable; no `!` involved | — |
| qok-ain family (all three) | 106 | ~0.496 | 0.365 | CENTRAL | comparable | comparable | — | — | CENTRAL | `NORMALIZATION_REQUIRED` | ZL total qokain (=qokai!n equivalent) comparable for family-level | — |
| `laiin` | 5 in payloads | 0.875 | 0.007 | LATE | `laiin` | 0 in payloads | N/A | N/A | NOT TESTABLE | `NOT_TESTABLE_ACROSS_ZL` | ZL has 7 `laiin` in Stars section but 0 in Stars packet payloads. ZL word-boundary conventions split `laiin` → `l` (separate) + `aiin` in packet reconstruction context. Packet-structure accessibility mismatch — not absence of phenomenon. | P2-CLAIM-011 |
| `ai!n` | 23 corpus-wide in payloads | 0.686 | 0.005 | LATE | — | 0 occurrences | — | — | NOT REPRESENTABLE | `NOT_TESTABLE_ACROSS_ZL` | `!` marker is Eva-T-specific. ZL contains 0 `ai!n` occurrences. Underlying glyph is absorbed into `aiin` or similar tokens. No ZL proxy can substitute without changing the object of study. | P2-CLAIM-012 |

---

## B.5c — Replication language standards

Per `docs/TRANSCRIPTION_SENSITIVITY_METHOD.md`, the following language conventions apply across all documents:

| Outcome | Preferred label | Avoid |
|---------|----------------|-------|
| ZL collapses two Takahashi tokens | "transcription normalization collapses..." | "failed replication" |
| ZL cannot represent the token | "not testable across ZL Eva-" | "null result in ZL" |
| ZL packet structure differs | "packet-level accessibility mismatch" | "`laiin` not found in ZL" |
| Full family tested as proxy | "family-level ZL test" | "`qokain` replicated" |
| Token-specific claim in Takahashi only | "result is transcription-bound" | "confirmed" without scope note |

---

## B.5d — Replication standard (3-condition requirement)

A valid cross-transliteration replication requires all three conditions:
1. The target token must be identifiable in the replication corpus with **the same boundary conventions**
2. The packet/structural context must be reconstructable from **the same or equivalent role assignments**
3. The n must be sufficient for **the same statistical framework**

All three ROSETTA3d token tests failed at least one condition:
- `qokain` (no `!`): fails condition 1 (different token in ZL)
- `laiin`: fails condition 2 (packet accessibility mismatch)
- `ai!n`: fails conditions 1 and 2 (token not representable; packet context inapplicable)

---

## Notes

1. **f111v confirmation**: The ZL `qokain` = Takahashi `qokai!n` identity was established by direct folio-level count comparison. On f111v: Takahashi H `qokai!n` = 24 occurrences; ZL `qokain` = 24 occurrences. Exact match. This confirms ZL normalizes the `!` distinction.

2. **Script reference**: The ROSETTA3d script (`scripts/ROSETTA3d_stolfi_zl_replication.py`) implements the ZL IVTFF parser, section assignment, role_map loading, and packet reconstruction. The script is the authoritative source for the ZL positional results. Output: `results/ROSETTA3d_stolfi_zl_results.json`.

3. **Structural vs. token-level replication**: Structural R1/R2 claims replicate directly across transliterations (B.5a). Token-level positional claims are more sensitive to transliteration conventions (B.5b). This difference is explained by the token-identity/packet-reconstruction/section-level three-dimensional sensitivity framework in `docs/TRANSCRIPTION_SENSITIVITY_METHOD.md`.
