# Annex B.3 — Lexical Candidate Claims
**Table**: Proof table for lexical alignment, distributional enrichment, and semantic candidate claims.
**Source**: `docs/CLAIM_REGISTRY.md`; `pilots/ROSETTA3b_20260319/`
**Primary paper**: Mumin (2026b) — Paper 2 §7.3 (sal), §6.1 (R6), §5 (Rosetta candidates)

---

## B.3a — `sal` distributional and lexical claims

| Claim ID | Level | Paper § | Token | Scope | Transcription | n | Test | Null / Control | Observed Result | Status | TC | Interpretation Bound | Repo Artifact |
|----------|-------|---------|-------|-------|---------------|---|------|----------------|----------------|--------|-----|---------------------|---------------|
| P2-CLAIM-013 | TOKEN-LEVEL | P2 §7.3 | `sal` | B-section enrichment | Takahashi H | n=44 total corpus occurrences | Rate ratio vs. corpus mean | Corpus mean token rate per section | 2.08× enrichment in B-section; 0 co-occurrences with `oly` (R6 structural marker, zero-overlap confirmed) | `CONFIRMED` | `DIRECT` | Distributional enrichment is a structural finding. Does not establish lexical meaning independently. Supports the Balneological semantic context but does not confirm it. | `scripts/ROSETTA2_sal_packet_position.py` → `results/ROSETTA2_sal_packet_results.json` |
| P2-CLAIM-014 | TOKEN-LEVEL | P2 §7.3 | `sal` (consonant stem `sl`) | Lexical alignment — B-section semantic | Takahashi H | — | 2-consonant exact ordered alignment | 200-entry lexicon (Latin, Arabic, Syriac); random 2-con baseline = 59.3%; competing-reading test (section coherence) | `sl` = `sl` exact ordered match: Latin *sal* (salt) and *salus* (health/welfare). 0 Arabic astronomical `sl`-stem terms in B-section context (Arabic `sl` astronomical candidates are Stars-section terms). | `CONFIRMED` (consonant-section-semantic triple) | `NOT_APPLICABLE` | Consonant-level match alone ≠ confirmed decipherment. Competing readings exist (any language with `sl` root). The "triple" (correct consonants + correct section + correct semantic domain) raises the alignment above chance but is not conclusive. Independent confirmation requires additional structural or codicological evidence. | `scripts/ROSETTA3b_expanded_alignment.py` → `results/ROSETTA3b_expanded_results.json` |

---

## B.3b — R6 Reference-like cluster Hebrew alignment

| Claim ID | Level | Paper § | Token Pool | Scope | Transcription | n (types) | Test | Null / Control | Observed Result | Status | TC | Interpretation Bound | Repo Artifact |
|----------|-------|---------|-----------|-------|---------------|-----------|------|----------------|----------------|--------|-----|---------------------|---------------|
| P2-CLAIM-018 | FAMILY-LEVEL | P2 §6.1 | R6 cluster family (`ol`, `al`, `or`, `ar` and variants) | Corpus-wide | Takahashi H | ~19 R6 token types (exact count pending full documentation) | Consonant alignment to Hebrew preposition inventory | Random 2-con match baseline; Hebrew preposition set (grammatical words: ל, ב, מ, על, אל, עם, כ, ו) | 52.6% of R6 token types match Hebrew prepositional consonant forms | `PROVISIONAL` | `NORMALIZATION_REQUIRED` | Scoring method not yet fully documented (hence PROVISIONAL). Match rate must be compared against random baseline for R6-length tokens. Hebrew preposition inventory must be pre-specified, not selected post-hoc. See `docs/R6_HEBREW_ALIGNMENT_METHOD.md` for method documentation target. | `scripts/ROSETTA3_ain_stem_alignment.py` (partial); full scoring not yet in repo |

---

## B.3c — 44 Rosetta candidates

| Claim ID | Level | Paper § | Feature | Scope | Transcription | n (tokens) | Test | Null / Control | Observed Result | Status | TC | Interpretation Bound | Repo Artifact |
|----------|-------|---------|---------|-------|---------------|-----------|------|----------------|----------------|--------|-----|---------------------|---------------|
| P2-CLAIM-019 | TOKEN-LEVEL | P2 §5 | 44 content tokens over-represented in specific illustration types | Folios with known illustration subtypes (20 folios, IA-series) | Takahashi H | n=44 tokens | Fisher exact | Per-illustration-type rate baseline (all assigned tokens in same illustration type) | p < 0.05 and enrichment > 3× for each of 44 tokens | `PROVISIONAL` | `NORMALIZATION_REQUIRED` | Illustration-type assignments (ground truth) are from scholarly consensus, not independently validated for this study. A token appearing 3× above mean in an illustration type is a candidate — not a confirmed alignment. Lexical alignment of the 44 candidates against external vocabulary is the required next step. | `scripts/ILLUS1_content_token_illustration_alignment.py` |

---

## B.3d — `qok-` null alignment (grammatical INIT morpheme confirmation)

Included here because it is a lexical null result that bears on interpretation of lexical candidates.

| Claim ID | Level | Paper § | Token Pool | Scope | Test | Null | Observed | Status | TC | Bound | Repo |
|----------|-------|---------|-----------|-------|------|------|----------|--------|-----|-------|------|
| P2-CLAIM-016 | TOKEN-LEVEL | P2 §7.3 | `qok-` prefix family (R1 tokens) | Lexical alignment | 2-consonant alignment vs. 200-entry Arabic/Hebrew/Latin lexicon | Random 2-con baseline = 59.3% | 0 `qk`-root terms in Arabic/Hebrew at 2-con threshold; only `aqua calida` (Latin `qkld`) at 2-con with irrelevant section context | `CONFIRMED` (null = expected) | `NOT_APPLICABLE` | Null result is the hypothesis-consistent result: if `qok-` is a grammatical INIT morpheme, it should have no lexical root. Confirmed. | `scripts/ROSETTA3b_expanded_alignment.py` |

---

## Notes

1. **Tier assignments**: `sal` is Tier 1 (exact consonant + section + semantic triple, no better competing reading). `qotaiin` is Tier 3 (consonant selectivity only, no positional slot, no section-semantic match). `lkaiin` is Tier 2 (ambiguous between Arabic `al-kaff` and Latin *lacus*). Tier definitions are maintained in pilot notes, not yet in a formal tier registry.

2. **RETRACTED-001**: `sal`'s earlier claimed terminal-entity positional pattern (24% pre-R2, n=4/17) was retracted after ROSETTA3c showed the rate (0.200) is below the 90th-percentile baseline (0.286). P2-CLAIM-014 stands on consonant alignment only — not on positional evidence. See Annex B.6.

3. **Normalization standard for lexical claims**: All lexical claims use the 2-consonant ordered-exact match at minimum. Higher-n consonant matches are better evidence. Section coherence test (does the candidate's semantic domain match the manuscript section?) is a required secondary test. All results are candidates until independent confirmation.
