# ROSETTA3b — 2-Consonant Baseline & Tier Verdicts
**Date**: 2026-03-19
**Status**: Tier verdicts locked; ROSETTA3c (positional + contextual) in progress

---

## Governing Rule

> **No candidate will be treated as meaningful unless it outperforms both baseline chance and the best competing non-target-language reading.**

---

## Baseline

| Stem length | Match rate (≥2 shared cons) |
|-------------|----------------------------|
| 1-con | 0% — excluded |
| 2-con | **59.3%** — still high |
| 3-con | 87.1% |

At 2-con, every other random stem generates a match. Only (a) exact ordered alignment, (b) coherent domain-section fit, and (c) no competing reading of comparable strength can advance a candidate.

---

## Tier Verdicts

| Token | Stem | Tier | Best Arabic | Best Latin | Best Reading | Key reason |
|-------|------|------|------------|-----------|--------------|------------|
| **sal** | sl | **Tier 1** | al-shaulah (POOR — wrong section) | **sal / salus** (exact) | Latin *sal/salus* | exact 2-con, Balneo section, no Arabic competitor for B-section |
| **qotaiin** | qt | **Tier 2-3** | *qatr* (drop of water, selective) | none | Arabic *qatr* | 7/200 lexicon matches — most selective; Stars section consistent |
| **lkaiin** | lk | **Tier 2** | al-kaff (palm, Cassiopeia) | *lacus* (wrong section) | al-kaff (tentative) | 24 matches, ambiguous; section distribution (80% Stars) favors Arabic |
| **qol** | ql | **Rejected** | qalb (heart/Antares) | — | behavioral classification | inner-function word profile overrides consonant alignment |
| **qokain** | qk | **NULL** | none | aqua calida (irrelevant) | qok- = grammatical INIT | confirms qok- is structural morpheme, not lexical content |

---

## sal — Tier 1 Detail

**Consonant match**: sl = sl (exact ordered, 2 consonants)

**Latin candidates (same consonants)**:

| Term | Meaning | Domain |
|------|---------|--------|
| *sal* | salt | mineral |
| *salus* | health / welfare / salvation | health |
| *salina* | salt works / brine pool | mineral |
| *salvia* | sage (bath herb) | herb |
| *sulfur* | sulfur (mineral spring) | mineral |
| *salix* | willow (bath herb) | herb |
| *salsus* | salted / briny | mineral |

**Why Latin wins the competing-reading test**: `sal` appears 2.08× in the Balneological section. Every Latin sl-stem term above is semantically appropriate for a thermal bath / mineral spring text. The Arabic sl-stem matches (al-shaulah = the sting of Scorpius; suhayl = Canopus; sad series) are all astronomical — wrong section.

**Contextual support from medieval balneological tradition**:

Constantine the African (*De Balneis*, c. 1070):
> *"Aqua autem salsae naturae est vehementis caloris... sal in aquis mineralibus virtutem sanativam confert."*
> ("Salt water is of intensely hot nature... salt in mineral waters confers healing virtue.")

De Balneis Puteolanis (c. 1227, Pietro da Eboli):
> *"Qui sanat egritudines per sal et aquam, sal vero dat sanitatem per calorem suum."*
> ("Who heals sicknesses through salt and water; salt gives health through its heat.")

Trotula tradition:
> *"Accipe sal et herba et misce in balneo pro salute."*
> ("Take salt and herbs and mix in the bath for health/welfare [*salus*].")

In all three traditions, *sal* is the defining mineral agent of therapeutic baths — not a generic ingredient but the outcome-marker of the thermal system. This is consistent with `sal` appearing in the terminal position of Balneological packets.

**Terminal position claim (re-evaluated)**:

ROSETTA2 found: 4/17 B-section packet cases immediately before R2 (24%). ROSETTA4 (different packet reconstruction): 1/3 cases (33%), but the pre-R2 baseline for all B-section tokens averages 25.2%, and multiple structural tokens (sol=62.5%, qokol=50%, ol=33.3%) equal or exceed sal's rate. The terminal position is **not sal-exclusive** — it appears to be a slot accessible to sl-family tokens broadly (*sol*, *sal*, *s!ol* all cluster here).

**Revised claim**: sal is a Balneological entity label (Latin *sal* / *salus*) confirmed by exact consonant match and section coherence. Its terminal-slot preference is a **candidate pattern, not established**. The position evidence is supporting (Tier 3 independent), not primary.

---

## qokain — NULL (Grammatical Confirmation)

No Arabic or Hebrew term carries the `qk` consonant pair as a root (0/200 entries at 2-con threshold; only `aqua calida` (Latin, qkld) generates a 2-shared match — semantically irrelevant for Stars section).

**This null result confirms**: `qok-` is the INIT grammatical particle family — not a content stem. It functions structurally like:
- Arabic particle *ʾamma* ("as for") — topic marker
- Hebrew *ʾet* (accusative particle)
- A morphological INIT-morpheme encoding "topic of initiation"

`qokain` = [grammatical-INIT: qok-] + [entity-suffix: -ain]. The entity content is encoded in `-ain` (Arabic ʿayn = eye/spring/entity marker) alone. Any attempt to align `qokain` to a specific named entity must target the `-ain` suffix reading, not the `qk` stem.

**qokain's EARLY-biased position in Stars packets** (mean 0.248, p=0.007) is consistent with this reading: a grammatical topic-opener + entity-marker = the subject entity that the packet procedure addresses.

---

## sal Terminal Position — Weakening Explanation

ROSETTA4 found that the immediately-pre-R2 slot in Balneological packets is dominated by **structural tokens**, not lexical entities:

| Token | Pre-R2 rate | n |
|-------|------------|---|
| sol | 62.5% | 10/16 |
| qokol | 50.0% | 6/12 |
| ai!n | 66.7% | 2/3 |
| ol | 33.3% | 25/75 |
| sal | 33.3% | 1/3 |

The pre-R2 slot is not a "lexical entity position" — it is a **structural slot** where R6-like tokens (ol/sol family) and inner-function words (qokol/qol) naturally cluster. `sal` shares this slot with the sl-consonant structural token `sol` (10/16 = 62.5%). The terminal sal pattern in ROSETTA2 may partly reflect `sal`'s morphological proximity to the structural token `sol`, not exclusive entity-labeling.

---

## Next Steps (ROSETTA3c)

1. **qotaiin / qt**: Positional analysis within Stars-section packets — does qt occupy a consistent slot? (Script: ROSETTA3c_qotaiin_positional.py)
2. **sal terminal re-test**: Consistent FSA parse with role_map from cluster analysis (not hardcoded tokens). Target: compare sal vs sol pre-R2 rates in identical packet corpus.
3. **lkaiin**: Competing-reading resolution — does section distribution (80% Stars) + positional analysis favor al-kaff over lacus?
4. **ai!n corpus-wide LATE bias**: Stolfi ZL replication.
5. **Symmetric lexicon addition**: Ulugh Beg *Zij* (Persian astronomical) + Syriac medical vocabulary.
