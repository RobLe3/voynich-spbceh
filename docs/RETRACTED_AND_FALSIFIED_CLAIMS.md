# Retracted and Falsified Claims — SPBCEH Research Program
**Last updated**: 2026-03-19
**Policy**: Retracted and falsified claims are NOT deleted. They are preserved with their original wording, the evidence that initially made them plausible, the test that failed them, and the replacement interpretation (if any). This record is scientifically useful and reviewer-accessible.

---

## RETRACTED-001

**Claim ID**: P2-CLAIM-015
**Original wording** (Paper 2, versions ≤ v0.93, §7.3):
> "`sal` is elevated 1.44× inside complete packet payloads and appears immediately before the R2 CLOSE token in 24% of its Balneological packet occurrences (n = 4/17) — a pattern consistent with `sal` occupying a terminal-entity slot (the final recorded entity before packet closure), possibly encoding the outcome or product of the procedure."

**Why it was initially plausible**:
- ROSETTA2 reconstruction found 17 sal-containing packets in section B; 4 of these (24%) had sal immediately before the R2 CLOSE token.
- This was above the intuitive expectation for a random content token.
- Matched the literary/balneological hypothesis: in Constantine the African's regimens, the health outcome (*salus*) often appears at the end of a procedure description.

**What test falsified it**:
- ROSETTA3c (consistent FSA packet reconstruction, role_map from `p1_1_cluster_frequencies.csv`, n=374 B-section packets):
  - sal appears in 10 B-packet payloads (not 17 — ROSETTA2 counting included non-strict contexts)
  - 2/10 sal occurrences are immediately pre-R2 (rate = 0.200)
  - Full B-section baseline: mean pre-R2 rate = 0.169; 90th percentile = 0.286
  - sal's rate (0.200) = 1.19× baseline mean; **below p90** — not statistically exceptional
  - Tokens exceeding sal's pre-R2 rate: sol (62.5%), qokol (50%), ai!n (66.7%), kai!n (37.5%), plus 16 others
  - The pre-R2 slot is dominated by **structural tokens** (sol, ol, qokol) and inner-function words, not lexical entities

**Root cause of error**:
- ROSETTA2 used a manually defined R1/R2 token set (hardcoded list) that was incomplete, producing a different packet reconstruction than the role_map method.
- The 4/17 figure conflated strict-payload pre-R2 positions with all sal-proximate-R2 positions.
- No pre-R2 baseline was computed in ROSETTA2 — the 24% rate was compared only to intuition, not to the empirical distribution of all tokens.

**Replacement interpretation**:
- sal's Tier 1 status (P2-CLAIM-014) stands based on the consonant-section-semantic triple: sl = sl (exact, Latin *sal/salus*), Balneological section coherence, semantic fit (mineral spring / health context). This is independent of positional claims.
- sal shows no special positional privilege. It is a lexical entity candidate with a strong consonant alignment but no demonstrated structural slot.

**Reproduction path for the failed test**:
```bash
cd scripts/
python3 ROSETTA3c_qotaiin_positional.py
# Section 4 output: "sal: 0.200 (2/10) — top 25%, vs baseline mean 0.169, vs p90 0.286"
```

**Paper correction**: Applied in Paper 2 v0.94 (§7.3, §9, §10 Conclusion).

---

## FALSIFIED-001

**Claim ID**: P2-CLAIM-008 (Nested B-packet hypothesis)
**Original wording** (informal hypothesis, PILOT4 setup):
> "B-section packets with INIT-classified first-payload tokens may be nested packets — a new packet initiated within the payload of an outer packet."

**Why it was initially plausible**:
- B-section has an elevated INIT-bleed rate: 17.9% of B-packet first-payload slots are INIT-classified tokens (vs. 7.9% in Stars, 6.4% in Herbal).
- If `qok-` tokens can initiate new packets, the elevated rate might indicate recursive nesting.

**What test falsified it**:
- PILOT4 addendum: Direct inspection of 67 B-section packets whose first-payload token is INIT-classified.
- 0/67 contain an internal CLOSE token before the outer R2. Sub-CLOSE = 0/67.
- Grammar is finite-state; nesting is not supported.

**Replacement interpretation**:
- The elevated INIT-bleed in B reflects role ambiguity: `qok-` tokens operate as INIT markers at the structural level but can appear in CONTENT positions within B-section payloads (dual function of the qok- morpheme in procedurally dense text). This is now called "INIT-bleed" rather than nesting.

**Reproduction path**:
```bash
cd scripts/
python3 PILOT4_balneo_packet_structure.py
# Look for: "nested packet hypothesis" section
```

---

## FALSIFIED-002

**Claim ID**: P2-CLAIM-017 (Folio-uniqueness as entity-label evidence)
**Original wording** (pilot phase, pre-PILOT5):
> "67.6% of -ain hapax types are folio-unique — i.e., appear on only one folio — which suggests they function as entity labels for specific illustration elements on that folio."

**Why it was initially plausible**:
- If -ain types label specific nymphs or stars depicted on individual folios, folio-unique tokens would be expected.
- 298/441 -ain types are folio-unique (67.6%) — above 50%.

**What test falsified it**:
- PILOT5 falsification check: Non-`-ain` tokens of matching frequency range are **74.8%** folio-unique.
- The baseline rate for rare tokens is 74.8% — higher than the -ain rate of 67.6%.
- Folio-uniqueness is a property of rare tokens in general, not specific to -ain types.

**Replacement interpretation**:
- Folio-uniqueness cannot serve as evidence for entity labeling. The strongest remaining evidence for -ain entity labeling is: (a) positional differentiation (qokain EARLY, laiin LATE) and (b) consonant alignment to the -ain suffix = Arabic ʿayn. Image-level mapping remains the required test.

**Reproduction path**:
```bash
cd scripts/
python3 PILOT5_ain_subfolio_analysis.py
# Look for: folio-unique section and control comparison
```

---

## RETRACTED-002

**Claim ID**: Informal (PILOT2 entity-labeling)
**Original claim**: Stars section -ain tokens show strong entity-labeling behavior: consistent recto/verso token identity suggests stable folio-level referents.

**Why it was initially plausible**: If -ain tokens label specific stars, the same star would appear on both recto and verso of the same folio spread.

**What test falsified it**: PILOT2 found only 2/7 folios showing recto/verso consistency in dominant -ain type — below random expectation for a stable entity-label hypothesis.

**Status**: `RETRACTED` (strong entity-labeling hypothesis retracted; descriptive folio-anchor pattern confirmed without causal entity-label interpretation)

---

## RETRACTED-003

**Claim ID**: Paper 2 §9 (IA.5 semantic sub-labels)
**Original claim**: Semantic sub-labels for roles (e.g., ACT:PULSE, MODE:CELESTIAL, CLOSE:TERMINAL) are empirically supported by folio-level illustration-type distributions.

**What test falsified it**: 3/4 sub-label predictions fail:
- `shol` (predicted MODE:CELESTIAL): zero rate in astronomical folios; elevated in botanical
- `daiin` (predicted domain-neutral ACT:PULSE): significantly more frequent in botanical than balneological (p < 0.0001)
- `ykchdy` (predicted CLOSE:TERMINAL): too rare to test
- Only `shedy` (R2, CLOSE) correctly predicts elevated balneological association

**Replacement**: Structural role assignments are validated; semantic interpretation of sub-labels within roles is not confirmed. Sub-labels removed from Paper 2 taxonomy.

**Status**: `FALSIFIED` (3/4 predictions failed; sub-label framework dropped)

**Alias**: Also identified as `FALSIFIED-003` in the Paper 1 appendix retraction count. Paper 1 counts all retractions including informal pilot items and uses FALSIFIED-003 as the alias for this entry. Paper 2 counts only formal P2-CLAIM-NNN items (which excludes this entry since it has no P2-CLAIM-NNN ID). The `daiin` section-rate finding from this falsification was subsequently formalized as `P2-CLAIM-022`.

---

## RETRACTED-004

**Claim ID**: ROSETTA3 (preliminary) — `lkaiin` → Latin *lacus* as primary reading
**Original claim** (ROSETTA3 log): `lkaiin` (lk stem) → Latin *lacus* (lake/pool) exact 2-consonant match — new candidate.

**What invalidated it**: lkaiin is 80.4% Stars-section. Latin *lacus* is a Balneological/water-basin term. Section mismatch disqualifies it as the primary reading. Additionally, multiple Arabic astronomical terms also match lk (al-kaff, al-iklil, al-dalik, al-simak compounds — 24 total matches in expanded lexicon). No single candidate is preferred over another.

**Replacement**: lkaiin remains Tier 2 — lk ambiguous between al-kaff (Arabic astro, Stars-consistent) and lacus (Latin water, wrong section). Positional evidence null (CENTRAL, p=0.943). Requires further study.

**Status**: `RETRACTED` (lacus not primary reading; lkaiin Tier 2 with unresolved ambiguity)
