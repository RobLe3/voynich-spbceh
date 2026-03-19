# Transcription Sensitivity — Methods Note
**Date**: 2026-03-19
**Status**: Active methods guidance
**Purpose**: Establishes how transcription choice affects token identity, packet-level testability, and claim comparability across the SPBCEH corpus. Required reading before evaluating any cross-transliteration replication result.

---

## 1. Background: The Transliteration Landscape

The Voynich Manuscript has been independently transliterated by multiple scholars. This project uses two:

| Code | File | Alphabet | Special markers |
|------|------|----------|----------------|
| H (Takahashi) | `Lsi_ivtff_0d_v4j_fixed.txt` | Eva-T | `!` glyph-variant marker |
| ZL (Zandbergen-Landini) | `data/ZL3b-n.txt` | Eva- (basic) | none |

**Critical difference**: Eva-T (Takahashi H) encodes a glyph-level distinction using `!`. Eva- (ZL) does not encode this distinction. This is not a transcription error — it reflects a deliberate difference in alphabet choice and glyph-level granularity.

All primary corpus analysis in this project uses Takahashi H. The ZL file was used only for cross-transliteration replication (ROSETTA3d).

---

## 2. The Three Sensitivity Cases

### Case 1: `qokain` vs `qokai!n` — The `!`-Marker Splitting Problem

In Takahashi H Eva-T:
- `qokain` = 69 total corpus occurrences (12 in Stars)
- `qokai!n` = 92 total corpus occurrences (most in Stars)

These are **two separate tokens** in Takahashi H. The `!` distinguishes a specific glyph variant from the standard form.

In ZL Eva-:
- `qokain` = 278 total corpus occurrences (100 in Stars)

The count 278 vs 69+92 = 161 shows that ZL `qokain` absorbs both Takahashi variants into one token. Confirmed by direct folio-level comparison:

> f111v: Takahashi H `qokai!n` = 24; ZL `qokain` = 24. **Exact match.**

**Consequence for positional inference**: The EARLY bias (P2-CLAIM-010) was found for Takahashi H `qokain` (no `!`, n=7 Stars packets). The corresponding ZL token is `qokain` (= Takahashi `qokai!n`), which is CENTRAL (n=22, p=0.234). Additionally, the combined Takahashi family (`qokain` + `qokai!n` + `qokaiin`, n=106) is also CENTRAL (p=0.365).

**Label**: `TOKEN-LEVEL, TRANSCRIPTION-BOUND`
The claim applies only to Takahashi H `qokain` (the no-`!` variant). It is not testable in any Eva- based transliteration.

---

### Case 2: `laiin` — The Token-Splitting Problem

In Takahashi H Eva-T:
- `laiin` = 11 total occurrences (9 in Stars)
- Treated as a single token: `l` + `a` + `i` + `i` + `n`

In ZL Eva-:
- `laiin` = 13 total occurrences (7 in Stars)
- BUT: ZL sometimes splits this into `l` (separate) + `aiin`, depending on word-internal spacing conventions
- f111v: ZL shows `l` = 11 as a separate token; Takahashi H shows this as part of compound tokens including `laiin`-family

**Consequence for packet-level analysis**: ZL has 7 `laiin` in Stars, but **0 appear in Stars packet payloads**. The token is present in the corpus but falls outside reconstructed packet boundaries in ZL due to different paragraph boundary and word-split conventions.

**Consequence for inference**: The LATE bias found for `laiin` in Takahashi H (n=5 Stars packets, p=0.007) cannot be tested in ZL because the token is structurally inaccessible in the ZL packet context, not because the phenomenon is absent.

**Label**: `TOKEN-LEVEL, NOT_TESTABLE_ACROSS_ZL`
This is a packet-structure accessibility problem, not a straightforward null replication. Absence in ZL packet payloads does not falsify the claim.

---

### Case 3: `ai!n` — The Marker Representation Problem

In Takahashi H Eva-T:
- `ai!n` = 56 total occurrences (40 in Stars, corpus-wide in all sections)
- The `!` encodes a specific glyph variant of the standard `aiin` form

In ZL Eva-:
- `ai!n` = 0 occurrences — **the token does not exist**
- The underlying glyph is represented as `aiin` or absorbed into similar tokens

**Consequence for positional inference**: The corpus-wide LATE bias (P2-CLAIM-012, n=23, p=0.005) found for `ai!n` in Takahashi H cannot be tested in ZL because the token is structurally unrepresentable in ZL's alphabet.

**Critical note**: `ai!n` ≠ `aiin` in Takahashi H. The `!` marker encodes a glyph distinction. Using ZL `aiin` as a proxy would conflate two different tokens and is methodologically invalid.

**Label**: `TOKEN-LEVEL, NOT_TESTABLE_ACROSS_ZL`
The claim is valid within the Takahashi H corpus. Its scope is bounded to the Eva-T transliteration system.

---

## 3. Taxonomy of Cross-Transcription Comparability

| Status | Meaning | Example |
|--------|---------|---------|
| `DIRECT` | Token exists with same identity in both systems; packet context preserved | `daiin`, `aiin`, structural R1/R2 tokens |
| `NORMALIZATION_REQUIRED` | Token exists but count differs; normalization step needed before comparison | `qokaiin` in Takahashi vs ZL |
| `TRANSCRIPTION-BOUND` | Claim depends on Eva-T-specific marker distinction; not representable in Eva- | `qokain` EARLY (no-`!` variant) |
| `NOT_TESTABLE_ACROSS_ZL` | Token exists in ZL but packet/structural context differs; result not transferable | `laiin` LATE (packet splitting), `ai!n` LATE (! absent) |
| `CROSS-TRANSCRIPTION_COMPARABLE` | Result has been tested in ZL and direction holds | (none yet for positional claims) |
| `NOT_APPLICABLE` | Claim does not depend on transliteration (e.g., image-level, physical) | Folio-level illustration type assignments |

---

## 4. Implications for Positional Inference

When a token appears at a specific position within reconstructed packets, that result is:

1. **Token-identity dependent**: the claim is only as stable as the token boundary. If ZL splits or merges tokens differently, the same underlying phenomenon may not be captured by the same token string.

2. **Packet-reconstruction dependent**: packet boundaries are reconstructed from R1/R2 role assignments derived from the Takahashi H corpus. Applying the same role_map to ZL is a methodological approximation — valid for structural R1/R2 tokens (which are consistently represented), but may not correctly position rare payload tokens that differ by transcription system.

3. **Section-level vs token-level**: section-level structural claims (e.g., "B-section has higher packet density") are more robust across transcriptions because they depend on aggregate token counts rather than specific glyph-level distinctions. Token-level claims are more vulnerable.

---

## 5. Worked Examples

### Example A: `qokain` EARLY in Stars (P2-CLAIM-010)

| | Takahashi H (Eva-T) | ZL (Eva-) |
|--|---------------------|-----------|
| Token | `qokain` (no !) | `qokain` (= Takahashi `qokai!n`) |
| n in Stars packets | 7 | 22 |
| Mean position | 0.248 | 0.605 |
| p-value | 0.007 | 0.234 |
| Direction | EARLY | CENTRAL |
| Same object? | No — different token in each system | |
| Conclusion | Token-level result, transcription-bound | Cannot replicate in ZL |

The EARLY bias is a property of the specific no-`!` `qokain` variant in Takahashi H. The ZL test is testing a different token (the `!`-marked form). These are not the same object.

### Example B: `laiin` LATE in Stars (P2-CLAIM-011)

| | Takahashi H (Eva-T) | ZL (Eva-) |
|--|---------------------|-----------|
| Token | `laiin` | `laiin` |
| Total in Stars | 9 | 7 |
| In Stars packet payloads | 5 | 0 |
| Conclusion | LATE (p=0.007) | Not testable — outside packet structure |

ZL has `laiin` in the Stars section but it falls outside packet boundaries. This is a structural accessibility problem, not a null result on the phenomenon itself.

### Example C: `ai!n` LATE corpus-wide (P2-CLAIM-012)

| | Takahashi H (Eva-T) | ZL (Eva-) |
|--|---------------------|-----------|
| Token | `ai!n` (! variant) | does not exist |
| Count | 56 | 0 |
| Conclusion | LATE (p=0.005, n=23) | Not representable |

The ! marker is Eva-T-specific. No ZL proxy can substitute for this token without changing the object of study.

---

## 6. Language Conventions for Papers and Registry

When reporting cross-transliteration results, the following language should be used:

| Outcome | Preferred label | Avoid |
|---------|----------------|-------|
| ZL collapses two Takahashi tokens | "transcription normalization collapses..." | "failed replication" |
| ZL cannot represent the token | "not testable across ZL Eva-" | "null result in ZL" |
| ZL packet structure differs | "packet-level accessibility mismatch" | "laiin not found in ZL" |
| Full family tested as proxy | "family-level ZL test" | "qokain replicated" |
| Token-specific claim in Takahashi only | "result is transcription-bound" | "confirmed" without scope note |

---

## 7. Implications for Replication Claims

A replication claim requires that the object being tested in the replication corpus is the same object as in the original corpus. When transcription normalization, token-splitting, or marker absence prevents this, the replication is **blocked at the object-identity level**, not failed at the statistical level.

**Standard for acceptable replication**:
1. The target token must be identifiable in the replication corpus with the same boundary conventions
2. The packet/structural context must be reconstructable from the same or equivalent role assignments
3. The n must be sufficient for the same statistical framework

If any of these conditions fail, the appropriate label is `NOT_TESTABLE_ACROSS_ZL` or `TRANSCRIPTION-BOUND`, not `FAILED_REPLICATION`.

---

## 8. Next Steps for Cross-Transcription Coverage

| Token | Path to replication |
|-------|---------------------|
| `qokain` (no !) | Requires a third transliteration that encodes the ! distinction separately (e.g., RF Extended Eva or IT Eva-T) |
| `laiin` | Requires a transliteration where `laiin` is consistently tokenized as a single unit with stable paragraph boundary conventions |
| `ai!n` | Same as `qokain` — requires Eva-T compatible source |
| Structural R1/R2 tokens | Directly testable in ZL; packet counts comparable (896 vs 886) |
| Section-level profiles | Directly testable in ZL; section assignment by folio range is transcription-independent |
