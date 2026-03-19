# Annex B.4 — Grammatical Structure and Null-Root Claims
**Table**: Proof table for claims establishing the packet grammar's formal properties and null-root lexical findings.
**Source**: `docs/CLAIM_REGISTRY.md`; `pilots/PILOT4_balneo_packet_log.md`
**Primary paper**: Mumin (2026b) — Paper 2 §3 (FSA/grammar), §7.3 (qok- null)

These claims jointly establish: (a) the packet grammar is non-random and formally expressible as an FSA, (b) the structural layer is more predictable than the surface layer, and (c) the R1 morpheme `qok-` is a grammatical initiator with no lexical root — the null alignment is the expected and hypothesis-consistent result.

---

## B.4a — Packet grammar and FSA conformance

| Claim ID | Level | Paper § | Feature | Scope | Transcription | n | Metric / Test | Null / Control | Observed Result | Pre-registered threshold | Status | TC | Interpretation Bound | Repo Artifact |
|----------|-------|---------|---------|-------|---------------|---|--------------|----------------|----------------|--------------------------|--------|-----|---------------------|---------------|
| P2-CLAIM-001 | METHOD-LEVEL | P2 §3 | FSA paragraph-level conformance | 413 paragraphs with assigned roles | Takahashi H | 413 paragraphs; 3,542 lines | % role-to-role transitions conformant to FSA; paragraph-level | Random role-sequence baseline | 61.3% paragraph-level conformant transitions | 60% (pre-registered) | `CONFIRMED` | `DIRECT` | Exceeds pre-registered threshold. Does not prove the text is a grammar — it confirms the grammar model is non-random. 91% of paragraphs are open (FSA-incomplete); consistent with packets spanning paragraph boundaries. | `scripts/p2_analysis.py` |
| P2-CLAIM-002 | METHOD-LEVEL | P2 §3.2 | Entropy decomposition (structural vs. variant) | Corpus-wide | Takahashi H | Corpus | Shannon entropy comparison | Random sequence baseline | H(structural role) = 2.38 bits < H(surface variant) = 2.77 bits | — | `CONFIRMED` | `DIRECT` | Structural role layer is more predictable than surface glyph-cluster choices. Consistent with dual-channel encoding hypothesis (grammar + lexical). Does not determine encoding mechanism. | `scripts/p2_analysis.py` |

---

## B.4b — Grammatical INIT morpheme null-root confirmation

| Claim ID | Level | Paper § | Token Pool | Scope | Test | Null / Control | Observed | Status | TC | Interpretation Bound | Repo Artifact |
|----------|-------|---------|-----------|-------|------|----------------|----------|--------|-----|---------------------|---------------|
| P2-CLAIM-016 | TOKEN-LEVEL | P2 §7.3 | `qok-` prefix family (10 R1 types) | Lexical alignment — corpus-wide | 2-consonant ordered-exact alignment vs. 200-entry Arabic/Hebrew/Latin lexicon | 59.3% random 2-con baseline; same scoring applied to all 200-entry candidate tokens | 0 Arabic/Hebrew `qk`-root matches at 2-con threshold. Only `aqua calida` (Latin; consonants `q-k-l-d`) at 2-con level — irrelevant section (not Balneological or Stars). | `CONFIRMED` (null = expected) | `NOT_APPLICABLE` | The null result is the hypothesis-consistent outcome: `qok-` as a grammatical INIT morpheme should have no lexical root (content words have roots; grammatical function words may not). The null result confirms that `qok-` behaves as a grammatical morpheme, not a content token. | `scripts/ROSETTA3b_expanded_alignment.py` → `results/ROSETTA3b_expanded_results.json` |

---

## B.4c — Cross-FSA structural validation (full-corpus packet reconstruction)

These results (from PILOT4 and ROSETTA3c) validate the FSA reconstruction method and confirm its application to section-specific packet density claims.

| Claim ID | Level | Paper § | Feature | n | Observed | Status | TC | Repo Artifact |
|----------|-------|---------|---------|---|----------|--------|-----|---------------|
| P2-CLAIM-007 | SECTION-LEVEL | P2 §4.3 | B-section packet density | 897 total packets | 374/897 = 41.7% in B; density 2.26× corpus average; B = 18.5% of tokens | `CONFIRMED` | `DIRECT` | `scripts/PILOT4_balneo_packet_structure.py` + `scripts/ROSETTA3c_qotaiin_positional.py` |
| P2-CLAIM-008 | METHOD-LEVEL | P2 §4.3 | Nested packet hypothesis | 67 B-packets with INIT-first-payload token | 0/67 contain sub-CLOSE before outer R2; grammar is finite-state | `FALSIFIED` | `NOT_APPLICABLE` | `scripts/PILOT4_balneo_packet_structure.py` |
| P2-CLAIM-009 | SECTION-LEVEL | P2 §4.3 | INIT-bleed rates by section | Per-section packets | B: 17.9%; S: 7.9%; H: 6.4% (INIT-classified first-payload token) | `CONFIRMED` | `DIRECT` | `scripts/PILOT4_balneo_packet_structure.py` |

---

## Notes

1. **Relationship between B.4a and B.4b**: FSA conformance (P2-CLAIM-001) establishes that the packet grammar is non-random. The null-root result (P2-CLAIM-016) establishes that R1 (`qok-`) tokens behave grammatically (no lexical root), which is consistent with the FSA grammar. Together they support a dual-layer structure: a grammatical layer (R1/R2 packet boundaries) and a lexical layer (R4 content tokens with roots).

2. **FSA and open paragraphs**: 91% of paragraphs are FSA-incomplete (open). Two interpretations: (a) packets are paragraph-spanning units; (b) the FSA model fails to capture the grammar. Both are consistent with the 61.3% conformance figure at the transition level.

3. **FALSIFIED-001** (P2-CLAIM-008): The nested packet hypothesis was a natural extension of the elevated INIT-bleed rate in B. Its falsification (0/67 sub-closes) is recorded here and in Annex B.6. The INIT-bleed is now interpreted as dual-function `qok-` tokens in procedurally dense text.
