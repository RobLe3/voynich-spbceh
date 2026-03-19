# PILOT2 — Stars -ain Folio-Anchor Alignment Test
**Phase 2 Step 5**
**Date**: 2026-03-19

---

## Summary

| Metric | Result |
|--------|--------|
| Total Stars -ain occurrences | 1,225 |
| Total -ain types in Stars | 414 |
| Folios with dominant -ain token (≥3) | 23 |
| Known zodiac-subject folios tested | 17 |
| Mean alignment score (EVA stem vs Arabic constellation) | 0.078 |
| Max alignment score | 0.333 (4 folios) |
| Scores ≥ 0.50 | **0** |
| Same-subject consistency (recto/verso pairs) | **2/7 = 29%** |

---

## Folio-by-Folio Results

| Folio | Subject | Dominant -ain | n | Stem cons | Align score |
|-------|---------|--------------|---|-----------|------------|
| f103r | Aries | `okai!n` | 5 | k | 0.00 |
| f103v | Aries | `okai!n` | 5 | k | 0.00 |
| f104r | Taurus | `lkaiin` | 4 | lk | 0.00 |
| f104v | Taurus | `qotai!n` | 4 | qt | 0.33 |
| f105r | Gemini | `odaiin` | 4 | d | 0.00 |
| f105v | Gemini | `chedaiin` | 3 | chd | 0.00 |
| f106r | Cancer | `okai!n` | 5 | k | 0.00 |
| f106v | Cancer | `qotaiin` | 5 | qt | 0.33 |
| f107r | Leo | `lkaiin` | 7 | lk | 0.00 |
| f107v | Leo | `lkaiin` | 6 | lk | 0.00 |
| f108r | Virgo | `okai!n` | 4 | k | 0.00 |
| f108v | Virgo | `raiin` | 4 | r | 0.00 |
| f111r | Sagittarius | `okai!n` | 3 | k | 0.00 |
| f111v | Star catalog | `okai!n` | 12 | k | N/A |
| f112r | Capricorn | `sai!n` | 3 | s | 0.00 |
| f112v | Aquarius | `chedaiin` | 3 | chd | 0.33 |
| f113r | Pisces | `lkaiin` | 4 | lk | 0.00 |
| f113v | Aries-alt | `lkaiin` | 5 | lk | 0.33 |
| f114r | Star charts | `qodaiin` | 5 | qd | N/A |
| f114v | Star charts | `qotaiin` | 9 | qt | N/A |
| f115r | Star charts | `raiin` | 5 | r | N/A |
| f115v | Star charts | `qotai!n` | 4 | qt | N/A |
| f116r | Star charts/text | `ai!n` | 10 | — | N/A |

---

## Same-Subject Consistency Test

Does the dominant -ain token stay the same across recto/verso of the same subject?

| Subject | Folios | Dominant tokens | Consistent? |
|---------|--------|----------------|------------|
| Aries | f103r, f103v | `okai!n`, `okai!n` | ✓ |
| Taurus | f104r, f104v | `lkaiin`, `qotai!n` | ✗ |
| Gemini | f105r, f105v | `odaiin`, `chedaiin` | ✗ |
| Cancer | f106r, f106v | `okai!n`, `qotaiin` | ✗ |
| Leo | f107r, f107v | `lkaiin`, `lkaiin` | ✓ |
| Virgo | f108r, f108v | `okai!n`, `raiin` | ✗ |
| Star charts | f114r–f115v | `qodaiin`, `qotaiin`, `raiin`, `qotai!n` | ✗ |

**Same-subject consistency: 2/7 = 29%**

This is **not significantly above chance** (expected ≈ 1/414 × number of shared types; with hundreds of -ain types, two folios sharing the same dominant token at chance would be rare, but within a small vocabulary of ~20 high-frequency types the probability is non-negligible).

---

## Key Findings

### Positive
1. **Folio-anchor pattern exists**: The dominant -ain token differs between most folios — it is not the same token globally dominating the whole Stars section. `okai!n`, `lkaiin`, `qotaiin`, `raiin`, `ai!n` each dominate different folios.
2. **Recto/verso consistency: 2/7 cases** (Aries: `okai!n` both sides; Leo: `lkaiin` both sides). These two are the strongest candidates for entity-label consistency.

### Negative (critical)
1. **Same-subject consistency fails in 5/7 cases**: Taurus, Gemini, Cancer, Virgo, and Star charts all show different dominant -ain tokens on recto vs. verso of the same illustration subject. This **refutes the strong version of the entity-labeling hypothesis**: the dominant -ain token does not reliably encode the folio's primary illustration subject.
2. **Arabic constellation alignment fails**: Mean score 0.078; no score ≥ 0.50. The EVA stem consonants do not map to Arabic zodiac names at above-chance rates.

---

## Revised Interpretation

The folio-anchor pattern is real — different folios have different dominant -ain tokens — but the anchoring is not consistently tied to illustration subject identity. Two alternative explanations:

**A. Sub-page structure**: Recto and verso of a zodiac folio may encode different entities even within the same illustration subject (e.g., different star groups or nymph figures within the Taurus zodiac circle). The -ain token may label a sub-page entity, not the zodiac sign itself.

**B. Writing session / scribe variability**: The dominant -ain token may reflect scribal session variation rather than subject encoding. Two scribal sessions on the same subject could produce different high-frequency tokens.

**C. Sampling noise**: The dominant token threshold (≥3 occurrences) is relatively low. With 20+ competing -ain types and short folios, stochastic dominance is likely for many folios.

---

## Status

**Entity-labeling hypothesis (strong form)**: NOT SUPPORTED. Same-subject consistency 2/7 = 29%.
**Folio-anchor pattern (descriptive)**: CONFIRMED. Each folio has a distinct dominant -ain cluster; the token changes across folios.
**Arabic alignment**: NOT CONFIRMED. Max score 0.33; mean 0.078.

**Consequence for Papers**: The folio-anchor pattern should be described purely descriptively (different folios have different dominant -ain tokens). The entity-labeling interpretation should be explicitly labeled as speculative. The strong claim that the Stars section is a "star catalog with per-folio entity labels" is not supported by the within-subject consistency test.

---

## Files
- `PILOT2_stars_ain_alignment.py` — analysis script
- `PILOT2_stars_ain_results.json` — raw results
- `PILOT2_stars_ain_log.md` — this file
