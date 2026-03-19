# New Findings — 2026-03-19
**Session**: ROSETTA2 + PILOT4 + PILOT5 + cross-section position test

---

## Summary of New Results

| Finding | Script | Status |
|---------|--------|--------|
| sal payload enrichment: 1.44× | ROSETTA2 | CONFIRMED |
| sal positional bias: none | ROSETTA2 | CONFIRMED (null) |
| sal terminal-entity pattern (4× before R2) | ROSETTA2 | CANDIDATE |
| B-section most packet-dense (41.7%, 2.26×) | PILOT4 | CONFIRMED |
| shedy = B-specific R2 closure (59% in B) | PILOT4 | CONFIRMED |
| qol as B first-payload entity (OR=7.83, p<0.01) | PILOT4 | CONFIRMED |
| Nested B packet hypothesis | PILOT4 addendum | REFUTED (0/67) |
| B INIT-bleed rate 17.9% (2.3× above S) | PILOT4 addendum | CONFIRMED |
| -ain 67.6% folio-unique types | PILOT5 | RETRACTED — baseline rate for rare tokens |
| qokain EARLY-biased in Stars (mean 0.248, p=0.007) | PILOT5 | CONFIRMED |
| laiin LATE-biased in Stars (mean 0.875, p=0.007) | PILOT5 | CONFIRMED |
| ai!n LATE-biased corpus-wide (mean 0.686, p=0.005) | Cross-section | CONFIRMED |
| qokain position is section-specific (S=early, B=central) | Cross-section | CONFIRMED |

---

## Finding 1: sal as intra-packet terminal entity (ROSETTA2)

`sal` (n=44, 2.08× Balneological) is elevated inside packet payloads (1.44×), slightly above structural `ol` (1.35×) and less than inner-function `qol` (2.01×). It has no positional bias overall (mean 0.552, p=0.52), but in 4/17 B-section packet cases it appears immediately before the R2 CLOSE token — the terminal entity slot.

**Interpretive candidate**: `sal` = entity label that records the outcome or product of the Balneological packet procedure. If the packet encodes a procedure (initiate → enumerate entities → close), the final entity may be the result or the focal object. Consistent with Latin *sal* (salt/brine) as the product of a bath preparation, or *salus* (health/well-being) as the outcome.

**Not yet established**: Whether the terminal position vs. other positions encodes a semantic distinction (subject vs. object), or whether `sal` simply appears throughout without a consistent slot.

---

## Finding 2: Balneological section has distinct packet grammar properties (PILOT4)

Three grammar-level properties separate section B from all other sections:

**a. Packet density**: B has 374/897 packets (41.7%) despite being only 18.5% of corpus tokens. Packet density 2.26× the corpus average. B is the most procedurally-intense section.

**b. Domain-specific R2 closure**: `shedy` closes 31.6% of B packets; 59% of all `shedy`-closed packets are in B. This quantifies at the packet level the ch/sh alternation found in Paper 2. The `sh-` stem is not just Balneological-associated — it is the **Balneological R2 closure marker**.

**c. Elevated INIT-bleed (17.9%)**: In 17.9% of B packets, the first-payload token is itself an INIT-classified token. This is 2.3× higher than Stars (7.9%) and 2.8× higher than Herbal (6.4%). Nested packet hypothesis REFUTED (0/67 have sub-CLOSE). The `qok-` morpheme appears to serve a dual function in section B: structural packet initiation AND content-layer entity reference.

**d. qol leads B payloads** (OR=7.83, p<0.01): `qol` preferentially occupies the FIRST payload slot in B packets — consistent with `qol` being an inner-packet function word that frames/introduces the B-section payload content.

---

## Finding 3: -ain positional sub-differentiation — first statistically confirmed (PILOT5)

For the first time, tokens within the -ain family show statistically significant positional bias within packet payloads:

| Token | Section | n | Mean pos | p | Interpretation |
|-------|---------|---|---------|---|----------------|
| `qokain` | S (Stars) | 7 | **0.248** | 0.007 | EARLY — entity-subject/topic-opener |
| `laiin` | S (Stars) | 5 | **0.875** | 0.007 | LATE — entity-object/terminal |
| `ai!n` | ALL | 23 | **0.686** | 0.005 | LATE — corpus-wide terminal marker |

The `qokain` finding is the most significant: the `qok-` INIT-morpheme + `-ain` suffix combination produces a token that preferentially occupies the LEADING entity position in Stars-section packet payloads. This is the first confirmed case of an entity-type token with a consistent structural slot.

**Critical qualifier**: `qokain`'s early bias is Stars-section-specific. In section B (n=29), mean position is 0.558 (p=0.40, central). The same token occupies different structural slots in different sections. This is direct evidence of **section-specific grammatical semantics** — the notation's token roles are context-dependent on the domain being recorded.

`ai!n`'s corpus-wide late bias (mean 0.686, p=0.005) suggests it is a **terminal entity marker across all sections** — possibly a generic entity-closing token.

---

## Finding 4: -ain family structure — two tiers

The -ain suffix family has at minimum two tiers:

**Tier 1 — Pan-folio function words** (appear in 15–23/23 folios, CENTRAL position):
- `aiin`, `daiin`, `qokaiin`, `okaiin`, `qokai!n`, `otaiin`
- These are NOT entity labels (too frequent and too pan-folio)
- Likely: aspectual markers, connectors, or particle-equivalents within the Stars notation

**Tier 2 — Rare entity labels** (298/441 types are hapax or near-hapax):
- Folio-uniqueness of this tier is NOT differentially evidential — non-ain tokens of similar frequency are 74.8% folio-unique (vs 67.6% for -ain). The folio-uniqueness rate is a baseline property of rare tokens, not specific to -ain.
- Whether these rare -ain types are entity labels remains an open question; the strongest test is image-level mapping (not yet done)

**Within the entity tier**: `qokain` (EARLY, Stars) and `laiin` (LATE, Stars) show positional differentiation — suggesting that even within entity-label tokens, there is a structural distinction between "leading entity" and "terminal entity."

---

## Morphological Framework (Draft)

Based on all pilots to date, a draft morphological model for the -ain family:

```
[STEM-CONSONANT] + [VOCALIC] + ain/aiin/ai!n/aiiin

STEM-CONSONANT encodes:
  ∅       → function-word ain (pan-folio, central)
  qok-    → INIT-family entity (leading position in S; bleed in B)
  d-      → common entity type (central, high-frequency)
  ok-     → reduced INIT entity (similar to qok-)
  ot-     → common content entity (central)
  l-      → LATE entity (terminal, low frequency)
  s-      → possible sal-type entity (bath/mineral domain)

VOCALIC variation (ain vs aiin vs aiiin vs ai!n vs ai!in):
  May encode: certainty/uncertainty of transcription (!) or
  morphological gradation (quantity/aspect in the original notation)
```

This framework predicts: the STEM consonants encode entity-class semantics; the VOCALIC suffix length encodes something like certainty or quantity (not yet tested).

---

## Next Research Steps (updated priority)

1. **ROSETTA3**: Stem consonant alignment for -ain types against:
   - Arabic astronomical names (al-Sufi tradition): `ʿayn`, `najm al-ʿayn`, etc.
   - Medieval Hebrew star vocabulary
   - Focus especially on: `qok-` + `-ain`, `l-` + `-ain`, `s-` + `-ain`

2. **ROSETTA4**: Medieval Latin balneological lexicon alignment for `sal` cluster:
   - *sal*, *salis*, *salina*, *salus*, *salubritas*, *salvia* (sage — common bath herb)
   - Constantine the African, De Balneis, Trotula tradition
   - Test: does the 4× "sal-before-R2" terminal pattern match a "product/result" slot in known recipes?

3. **Image analysis** (user action required): Map folio-unique -ain hapax types to specific nymph or star illustration elements on the Beinecke high-resolution scans

4. **`ai!n` corpus-wide late-bias replication**: This is a new corpus-wide finding — replicate on Stolfi transcription to check if it survives cross-transliteration

---

## Falsification Tests

The following would KILL the entity-label interpretation of -ain:

- If the 67.6% folio-unique rate is also found in NON-ain tokens of similar frequency — would indicate that rare tokens are always folio-unique regardless of function
- If `qokain`'s early bias does not replicate in Stolfi transliteration
- If image-level mapping of folio-unique hapax -ain types shows NO correspondence to individual illustration elements

The following would KILL the sal terminal-entity hypothesis:

- If other random content tokens also appear before R2 at 24% rate
- If the terminal sal pattern is not replicated in a different section's packet analysis
