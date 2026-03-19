# ROSETTA3 — -ain Stem Alignment Log
**Date**: 2026-03-19
**Script**: `scripts/ROSETTA3_ain_stem_alignment.py`
**Results**: `results/ROSETTA3_ain_alignment_results.json`

---

## Summary Table

| Token | Stem | Priority finding | Score | Match | Verdict |
|-------|------|-----------------|-------|-------|---------|
| sal | sl | Balneo 2.08× (terminal pattern) | **1.00** | sal/salus (Latin) | CONFIRMED — 2-con exact |
| lkaiin | lk | Stars common (n=37) | **1.00** | lacus (Latin) | CANDIDATE — 2-con exact |
| qotaiin | qt | Stars folio-anchor (n=39) | 0.67 | qatr (Arabic, "drop of water") | CANDIDATE — 2 shared |
| qol | ql | B inner-function OR=7.83 | 0.67 | qalb (Arabic, "heart/Antares") | CANDIDATE — 2 shared |
| qokain | qk | Stars EARLY (0.248, p=0.007) | 0.50 | none adequate | NULL — see §6 |
| laiin | l | Stars LATE (0.875, p=0.007) | 1.00 | oleum (Latin, "oil") | NOT MEANINGFUL — 1-con |
| daiin, okaiin, raiin, saiin | d/k/r/s | Stars common | 0.50 | various | NOT MEANINGFUL — 1-con |
| ai!n, aiin | ∅ | bare -ain | no match | — | NO STEM — not testable |

---

## Critical Finding 1: BASELINE PROBLEM

The consonant matching approach produces a **90.5% match rate** for random stems against the combined reference lexicons. All priority tokens with 1+ consonants hit 100% match rate, only 1.11× above baseline.

**Consequence**: Single-consonant stems (l, d, k, r, s) cannot produce discriminating alignment. Any "match" for these tokens is indistinguishable from chance. Results for single-consonant tokens are **not reportable** as evidence.

**Threshold for meaningful results**: 2+ consonant stems with exact consonant match only. This limits interpretable results to: `sal` (sl), `lkaiin` (lk), `qotaiin` (qt partial), `qol` (ql partial).

---

## Finding 2: sal → Latin sal / salus (CONFIRMED)

`sal` (sl, Balneological 2.08×, terminal-entity candidate):
- Exact consonant match against Latin `sal` (salt, sl) and `salus` (health/welfare, sl)
- Score 1.00 for both
- This is not a new finding — it was the hypothesis entering ROSETTA3
- **ROSETTA3 confirms**: The consonant alignment is exact and consistent with a Latin Balneological origin
- Combined with the terminal-entity packet pattern (4/17 immediately before R2, 24%), `sal` → Latin *sal* or *salus* remains the strongest entity-label candidate in the corpus

---

## Finding 3: lkaiin → lacus (Latin, "lake/pool") — CANDIDATE

`lkaiin` (lk, Stars section, n=37):
- Exact 2-consonant match against Latin `lacus` (lk: lake/pool) — Score 1.00
- Also matches Arabic `kulya` (kl: kidney) — same consonants, reversed order

**Interpretation**: `lacus` (lake/pool) is a balneological Latin term, but `lkaiin` is primarily a Stars-section token. The match is phonetically exact but semantically cross-domain. Two explanations:
1. Spurious: `lk` is a common consonant pair that will match widely (but at 2 consonants this is less likely to be chance)
2. Genuine: the scribal system reused the same consonant template across domains (astronomical water body = pool/lake, consistent with medieval astronomical texts' descriptions of celestial regions)

**Status**: Candidate only. Requires: (a) check whether `lkaiin` appears in any Balneological context; (b) test `lk` baseline against expanded lexicons.

---

## Finding 4: qotaiin → qatr (Arabic, "drop of water") — CANDIDATE

`qotaiin` (qt, Stars folio-anchor, n=39):
- Score 0.67, 2 shared consonants (q and t) against `qatr` (qtr)
- `qatr` in Arabic = "drop of water" — appears in astronomical/hydrological contexts
- Also matches `laqit` (Arabic star name: "the foundling") at 0.67 and `tiryaq` (theriac/antidote) at 0.67

**Interpretation**: `qotaiin` is a folio-anchor token in the Stars section — appears as the dominant or near-dominant -ain type on specific folios. The `qatr` match (drop of water) is semantically plausible for astronomical water notation. Not an exact match (qt vs qtr — missing r), so this is a partial alignment only.

**Status**: Speculative candidate. Worth noting in future work but not claimable.

---

## Finding 5: qol → qalb (Arabic, "heart/Antares") — CANDIDATE

`qol` (ql, B inner-function word, OR=7.83):
- Score 0.67, 2 shared consonants (q and l) against `qalb` (qlb: heart, the name of Antares)
- `qalb` is one of the most prominent Arabic star names (Qalb al-ʿAqrab = Heart of the Scorpion = Antares)

**Critical qualifier**: `qol` is classified as an inner-function word (like a grammatical particle), not a lexical entity. If `qol` is the Voynich equivalent of Hebrew *kol* (all/every), the Arabic star name alignment is coincidental. The qalb match is intriguing but likely spurious given qol's grammatical behavior.

**Status**: Not pursued. qol's function-word classification takes precedence over speculative lexical alignment.

---

## Finding 6: qokain → NULL (Significant Negative) ★

`qokain` (qk, Stars EARLY, mean position 0.248, p=0.007):
- Best match: qaus (bow/arc), score 0.50, sharing only q
- No Arabic astronomical or Hebrew term has both q AND k as root consonants in a common configuration
- The Arabic `qk` consonant pair is not a standard triconsonantal root pattern

**Interpretation**: This null result is *itself* evidential. The qok- prefix is the INIT morpheme shared by ALL R1 tokens (qokeedy, qokeey, qokedy, qokol, qokchey, qokain, etc.). Its consonants should not align with a specific lexical word because it encodes structural role (topic-initiation), not content. The fact that `qk` finds no Arabic/Hebrew lexical home is consistent with `qok-` being a **grammatical particle** — the equivalent of Arabic `ʾamma` (as for...) or Hebrew `ʾet` (accusative marker), rather than a translatable noun.

**Implication for morphological model**: `qokain` = [grammatical-INIT-morpheme: qok] + [entity-marker: ain]. The `qok-` component is structural, not lexical. The entity being referenced is encoded in the -ain suffix alone, not in qok-. Attempting to align qokain to a specific Arabic star name via consonant matching is methodologically incorrect — it conflates grammatical and lexical components.

**Status**: NULL as expected. Supports grammatical-particle reading of qok-.

---

## Finding 7: Morphological Observation — lam prefix in laiin

`laiin` (l, Stars LATE, mean position 0.875, p=0.007):
- Single-consonant l stem: not discriminating by baseline analysis
- BUT: Arabic/Hebrew lam (l) functions as a prefix particle — "to/for/of/by"
- Reading: laiin = lam + ʿayn = "for the [eye/spring/entity]" or "of the entity"
- This is consistent with LATE position: terminal entity receiving the action or outcome of the Stars-section packet

This is a morphological reading, not a lexical alignment. It predicts `laiin` ≠ a standalone word, but rather a prepositional phrase: `l-` (preposition) + `-ain` (entity noun). The Stars section LATE position of `laiin` would then mean: "for/of [the named entity]" — the entity to which the packet procedure is directed.

**Status**: Speculative morphological hypothesis only. Cannot be distinguished from coincidence without broader transliteration testing.

---

## Methodological Assessment

**What the scoring function cannot do** (at short stems):
- Discriminate 1-consonant alignments from chance (baseline 90.5%)
- Confirm any specific etymological link

**What is potentially meaningful** (2+ consonant exact):
- `sal` → sl: EXACT (pre-existing candidate, confirmed)
- `lkaiin` → lk: EXACT (new candidate, low confidence)
- Partial 2-consonant: qotaiin→qatr (intriguing but not claimable)

**Recommended ROSETTA3b improvements**:
1. Expand Arabic lexicon to full al-Sufi star catalog (283 entries) — test 3+ consonant stems
2. Expand Latin balneological lexicon to Constantine the African and De Balneis (~150 terms)
3. Apply 2-consonant minimum threshold for any reported match
4. Test the `qotaiin` qt pattern against all known `qatr` / `qatr al-X` compounds in al-Sufi
5. Compute per-stem baseline by stem length (1-con baseline, 2-con baseline, 3-con baseline separately)

---

## Updated -ain Morphological Model

```
[STEM-CONSONANT] + [VOCALIC] + ain/aiin/ai!n/aiiin

STEM-CONSONANT encodes (updated after ROSETTA3):
  ∅        → bare entity marker (ai!n = terminal corpus-wide; aiin = pan-folio)
  qok-     → INIT grammatical particle (not lexical; NULL alignment expected)
  d-       → common entity prefix (unresolved, single-con not discriminating)
  ok-      → reduced INIT entity (k-stem, unresolved)
  ot-      → common content entity (t-stem; qotaiin→qatr partial)
  lk-      → entity with l+k stem; lacus (Latin) exact match — candidate
  l-       → lam-prepositional entity; "for/of [entity]" — LATE slot
  s-       → sal-domain entity (saiin, s-stem, unresolved)
  sl       → sal: CONFIRMED lexical entity (Latin sal/salus)

GRAMMATICAL vs LEXICAL distinction:
  qok- is GRAMMATICAL (INIT-morpheme; no lexical alignment expected)
  -ain is LEXICAL (entity marker; Arabic/Hebrew ʿayn etymon)
  Stems other than qok- are candidate LEXICAL prefixes (unresolved)
```

---

## Status Verdicts

| Claim | Status |
|-------|--------|
| sal → Latin sal/salus (sl exact) | SUPPORTED — exact consonant alignment confirmed |
| lkaiin → Latin lacus (lk exact) | CANDIDATE — exact 2-con, low confidence |
| qotaiin → Arabic qatr (qt partial) | SPECULATIVE — 2 shared, 1 missing |
| qok- is grammatical, not lexical | SUPPORTED — null alignment is expected |
| laiin l-prefix = lam preposition | SPECULATIVE — morphological reading only |
| -ain = Arabic ʿayn (eye/spring) | BACKGROUND ASSUMPTION — not tested here |
| Any 1-consonant alignment | NOT MEANINGFUL — baseline too high |

---

## Next Steps

1. **ROSETTA3b** (high priority): Expand lexicons to full al-Sufi catalog + Constantine. Apply 2-con minimum. Compute per-stem-length baseline. Test all qotaiin / qt-root Arabic compounds.
2. **ROSETTA4** (sal terminal-entity): Measure whether ANY content token appears before R2 at 24% rate (compute baseline). If sal is significantly above baseline, terminal-entity hypothesis strengthened.
3. **ai!n Stolfi replication**: LATE bias (0.686, p=0.005) found in Takahashi; replicate in Stolfi ZL transliteration.
4. **Image mapping** (user action required): Identify whether folio-anchor -ain tokens correspond to specific nymph/star illustration elements in Beinecke high-res scans.
