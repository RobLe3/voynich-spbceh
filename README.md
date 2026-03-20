# SPBCEH — Voynich Manuscript Positional Role Analysis

**Semantic Pose-Based Cognitive Encoding Hypothesis (SPBCEH)**
Structural and functional analysis of the Voynich Manuscript (Beinecke MS 408) using transition-based positional role classification of EVA glyph clusters.

**Author**: Roble Mumin
**Status**: Active research, March 2026
**Papers**: [Paper 1](#paper-1) · [Paper 2](#paper-2) · [Paper 3](#paper-3)
**Published at**: https://roblemumin.com/library.html

---

## Current Claim State (2026-03-19)

All 30 claims are tracked in [`docs/CLAIM_REGISTRY.md`](docs/CLAIM_REGISTRY.md). Full proof tables are in [`annex_maps/ANNEX_B1–B8`](annex_maps/). Claim-to-artifact map: see [Reproducing Results](#reproducing-the-primary-results-613-fsa-conformance-and-647-classification-accuracy) and `annex_maps/ANNEX_B8_verification_index.md`.

### Claim status summary

| Status | Count | Notes |
|--------|-------|-------|
| `CONFIRMED` | 22 | All structural, grammar, and section-level claims; sal enrichment and Tier 1 lexical |
| `CONFIRMED + CROSS-TRANSCRIPTION_PENDING` | 2 | `laiin` LATE Stars (P2-CLAIM-011); `ai!n` LATE corpus-wide (P2-CLAIM-012) |
| `PROVISIONAL` | 3 | `qokain` EARLY Stars (P2-CLAIM-010) — downgraded; R6 Hebrew prepositions (P2-CLAIM-018); 44 Rosetta candidates illustration-type enrichment (P2-CLAIM-019) |
| `RETRACTED` | 1 | `sal` terminal-entity positional pattern (P2-CLAIM-015) |
| `FALSIFIED` | 2 | Nested B-section packets (P2-CLAIM-008); folio-uniqueness as entity evidence (P2-CLAIM-017) |

These five status categories are mutually exclusive. They sum to 30 (= 22 + 2 + 3 + 1 + 2).

### ROSETTA3d — ZL cross-transliteration boundary test (2026-03-19)

Cross-transliteration evaluation (Zandbergen-Landini ZL corpus, Eva- basic) reveals that the ZL tests constitute **boundary tests on token comparability**, not straightforward null replications. The ZL alphabet lacks the `!` glyph-variant marker used in Takahashi H (Eva-T).

| Claim | Takahashi H result | ZL result | TC Status | Verdict |
|-------|--------------------|-----------|-----------|---------|
| `qokain` (no `!`) EARLY Stars | n=7, p=0.007 | ZL `qokain` = Takahashi `qokai!n`; n=22, p=0.234, CENTRAL | `TRANSCRIPTION-BOUND` | **PROVISIONAL** — different token tested in ZL; `qokai!n` (n=39) CENTRAL; full family (n=106) CENTRAL (p=0.365) |
| `laiin` LATE Stars | n=5, p=0.007 | 0 in Stars packet payloads | `NOT_TESTABLE_ACROSS_ZL` | **CONFIRMED + CROSS-TRANSCRIPTION_PENDING** — ZL splits `laiin` in packet context; absence ≠ falsification |
| `ai!n` LATE corpus-wide | n=23, p=0.005 | 0 occurrences | `NOT_TESTABLE_ACROSS_ZL` | **CONFIRMED + CROSS-TRANSCRIPTION_PENDING** — `!` marker absent from ZL Eva- |
| Structural packet count | 897 packets (PILOT4) | 886 packets | `DIRECT` | Full replication — structural claims are transliteration-stable |

Full method: [`docs/TRANSCRIPTION_SENSITIVITY_METHOD.md`](docs/TRANSCRIPTION_SENSITIVITY_METHOD.md)

### Tier verdicts — ROSETTA3b/3c (2026-03-19)

| Token | Tier | Best reading | Key evidence |
|-------|------|-------------|--------------|
| `sal` | **Tier 1** | Latin *sal* / *salus* | sl = sl exact; Balneological section; no competing Arabic sl-stem for B context. Positional privilege **retracted** (ROSETTA3c: rate 1.19× baseline, below p90). |
| `qotaiin` | Tier 3 | — | No positional slot (CENTRAL, p=0.388); consonant selectivity only |
| `lkaiin` | Tier 2 | ambiguous: al-kaff (Arabic) vs *lacus* (Latin) | 80% Stars → Arabic favored; *lacus* primary reading **retracted** (section mismatch) |
| `qol` | Rejected (lexical) | — | Inner-function word profile (Layer 2); no lexical alignment |
| `qok-` prefix | **NULL confirmed** | grammatical INIT morpheme | Zero Arabic/Hebrew qk roots; NULL = expected for grammatical particle |

---

## Overview

The Voynich Manuscript has resisted decipherment for over a century. Rather than assuming it encodes natural language, this project classifies EVA-transcribed glyph clusters by their *positional behavior and functional role* within line and paragraph structures.

The central finding: EVA clusters exhibit **directional functional asymmetry** — their roles are not interchangeable without destroying structural coherence. The R2 (Closure-like) → R1 (Initiator-like) transition is the single strongest structural signal in the corpus (*z* = +9.75 vs. 1,000 shuffled baselines), anchoring a packet grammar that operates at the paragraph level. Paragraph-level FSA conformance reaches **61.3%**, exceeding the pre-registered 60% threshold.

These findings are **compatible with multiple interpretive hypotheses** (recording system, Hebrew/Semitic cipher, structured notation) and do not claim to translate the manuscript. The contribution is structural: establishing that a real, falsification-tested grammar exists — quantified by author-runnable scripts with claim-to-artifact traceability — a necessary foundation for any subsequent interpretive work.

---

## Six-Role Taxonomy (v2.0)

Derived from the original seven-role framework through empirical anti-projection testing. The R4/R5 merger (Action-like + Mode-like → Content) is data-driven, not arbitrary.

| Role | Label | Defining criterion | Key tokens |
|------|-------|-------------------|-----------|
| R1 | Initiator-like | Significantly elevated R2→R1 transition (*z*=+9.71, 6-role; *z*=+9.75, 7-role); 10 of 11 INIT types share exclusive `qok-` prefix (fachys excluded, n=1) | `qokeedy`, `qokeey`, `qokedy` |
| R2 | Closure-like | Elevated R2→R1 preceding; 3 consonant stems (`ch-`, `sh-`, `lch-`) × 4 suffix variants | `chedy`, `shedy`, `lchedy` |
| R3 | Link-like | >85% medial position in all 7 tokens (cross-validated: >83%) | `okaiin`, `aiin` |
| R4 | Content | Section-modulated; clustered not periodic (CV=1.502); domain anchor | `daiin`, `ol`, `al` |
| R5 | Temporal-like | Positional flexibility; appears in pairs/triplets | `aiin` (medial contexts) |
| R6 | Reference-like | High frequency, even distribution; maps to Hebrew prepositions at 52.6% | `ol`, `al`, `or`, `ar` |

**`ch`/`sh` R2 alternation**: `sh`-stem tokens associate with Biological/Balneological section; `ch`-stem tokens associate with Stars section. Structurally real and folio-validated.

---

## Three-Layer Structural Model

Post-classification content analysis reveals three sublayers within the structural/content binary:

```
LAYER 1 — FRAME (positionally privileged, structurally decoded)
  R1 tokens: qok- prefix → grammatical position morpheme
  R2 tokens: ch/sh/lch stems → closure + domain marker
  R6 tokens: ol, al, or, ar → Hebrew preposition matches (52.6%)

LAYER 2 — INNER-PACKET FUNCTION WORDS (content-classified, function-word behavior)
  qol  (n=145, 77% Balneological): Pearson r=0.940 with structural R6 token ol
  kal, kol: Hebrew kol (all/every) root candidates
  These tokens appear inside packet payloads but mirror structural-layer section profiles

LAYER 3 — LEXICAL ENTITIES (section- and folio-specific vocabulary)
  44 Rosetta candidates (Fisher exact p<0.05, enrichment >3× in specific illustration types)
  sal  → Latin sal (salt) or salus (health): exact consonant match, 3.54× Balneological
  ain  → Arabic/Hebrew ʿayn (eye/spring): score 1.00
  -ain suffix: folio-anchor pattern in Stars section (dominant token changes per folio)
```

**Decipherment implication**: A two-layer decode strategy (structural vs. content) will fail because it conflates Layer 2 inner-packet function words with Layer 3 lexical entities. The three-layer model is the minimum architecture for substantive decipherment progress.

---

## Paper 1 — v0.92

**Title**: Positional Role Asymmetry in Voynich Manuscript EVA Clusters: A Functional Classification Framework with Falsification Protocol
**Version**: v0.92 — Manuscript Draft, March 2026
**Compiled**: 10 pages; 0 LaTeX errors
**Claim IDs**: P1-CLAIM-001 through P1-CLAIM-008 (all `CONFIRMED`)

**Key results**:
- 7→6 role taxonomy via anti-projection testing
- R2→R1 *z* = +9.75 (7-role); CLOSE→INIT packet grammar
- Section profiles significant across all roles (Kruskal-Wallis *p* < 0.0001)
- Falsification: original framework 3/3 coherent; inverted framework 0/3
- Cross-transliteration: Pearson *r* = 0.937 for positional % (Takahashi vs. Stolfi)

---

## Paper 2 — v0.94

**Title**: Transition Grammar and Cognitive Domain Profiles in the Voynich Manuscript: Evidence for a Functional Recording System from Six-Role Cluster Analysis
**Version**: v0.94 — Manuscript Draft, March 2026
**Compiled**: 17 pages; 0 LaTeX errors
**Claim IDs**: P2-CLAIM-001 through P2-CLAIM-022 (22 confirmed, 2 provisional, 3 retracted/falsified)

**Key results**:
- Paragraph-level FSA conformance: **61.3%** (pre-registered threshold: 60%)
- Entropy: H(structural) = 2.38 bits < H(variant) = 2.77 bits ✓
- Section classification accuracy: **64.7%** (6-role model, 1-NN; pre-registered primary result from `p2_5_6role_rerun.py`). 7-role KNN-5 reaches 69.8% but is superseded by the 6-role model selection. RF3b note: the 7-role raw-token baseline (73.3% KNN-5) remains in the result file (`rf3b_triggered: true` in `p1_4_classification_results.json`) as a documented instrument limitation under the superseded 7-role model.
- `shedy`-cluster: 10× elevated in Balneological vs. Herbal (*p* < 0.0001)
- Three-way interpretive comparison: recording system (Model A), Hebrew cipher (Model B), structured notation (Model C)

---

## Paper 3 — v0.30

**Title**: The Stranded Recorder Hypothesis: The Voynich Manuscript as a Domain-Specific Notation System
**Version**: v0.30 — Manuscript Draft, March 2026
**Compiled**: 10 pages; 0 LaTeX errors

**Key argument**: The Voynich text is the earliest surviving example of a highly structured, multi-layer domain-specific notation system. The paper demonstrates four defining properties of domain-specific notation and compares the VM architecture to contemporaneous notation traditions (liturgical music, astronomical tables, pharmaceutical recipe notation). The ET/non-human authorship hypothesis is confined to a speculative epilogue, clearly labeled as such. Gate condition for this paper: P1.3 + P1.4 + P2.1 + P2.5 + D3 — all passed.

---

## Reproducing the Primary Results (61.3% FSA Conformance and 64.7% Classification Accuracy)

```bash
# Place Lsi_ivtff_0d_v4j_fixed.txt in data/ (download from voynich.nu/transcr.html)

cd scripts/

# 1. Parse corpus → data/corpus_tokens.csv, data/corpus_lines.csv
python parse_corpus.py

# 2. Cluster analysis → results/p1_1_cluster_frequencies.csv, results/p1_6_transition_matrix.json
python p1_cluster_analysis.py

# 3. FSA conformance + entropy → results/p2_all_results.json
python p2_analysis.py
# Key output: p2_1.para_level.pct_conformant_trans = 61.3

# 4. 6-role anti-projection test → results/p2_5_v2_6role_results.json
python p2_5_6role_rerun.py
# Key output: p14_cls_accuracy = 0.647
```

Scripts read inputs from `data/` and write outputs to `results/` relative to the repo root.

**Requirements**: Python ≥ 3.9; install dependencies with `pip install -r requirements.txt`

Full pipeline: `bash scripts/reproduce.sh` (runs steps 1–6 in order).
Verify existing outputs: `python scripts/smoke_test.py`
Expected metric values: `docs/EXPECTED_OUTPUTS.md`

---

## Repository Structure

```
/
├── README.md
├── LICENSE
├── requirements.txt               # pandas, numpy, scipy, scikit-learn (for peripheral scripts; core pipeline is stdlib-only)
├── data/
│   ├── corpus_tokens.csv          # Parsed token-level corpus (37,045 tokens)
│   ├── corpus_lines.csv           # Line-level corpus
│   └── ZL3b-n.txt                 # Zandbergen-Landini ZL transliteration (Eva- basic; cross-transliteration)
├── scripts/
│   ├── reproduce.sh               # Full pipeline runner (steps 1–6 in order)
│   ├── smoke_test.py              # Verify output artifacts + headline metrics
│   ├── parse_corpus.py            # IVTFF → CSV parser
│   ├── p1_cluster_analysis.py     # Role classification + positional stats (P1 primary)
│   ├── p1_3_falsification.py      # Role inversion falsification test
│   ├── p1_4_classification.py     # Leave-one-folio-out section classifier
│   ├── p1_5_cross_transliteration.py  # Cross-transliteration r=0.937 test
│   ├── p2_analysis.py             # FSA conformance + entropy decomposition (P2 primary)
│   ├── p2_5_6role_rerun.py        # Anti-projection test (31 alternatives)
│   ├── DECODE1_sal_cluster.py     # sal co-occurrence analysis
│   ├── DECODE2_stars_ain.py       # Stars -ain folio-anchor analysis
│   ├── DECODE3_qol_cluster.py     # qol/ol inner-function correlation (P2-CLAIM-006)
│   ├── MORPH1_ain_suffix_alignment.py
│   ├── ROSETTA1_balneological_alignment.py
│   ├── ROSETTA2_sal_packet_position.py      # sal enrichment; original terminal-position (RETRACTED)
│   ├── ROSETTA3_ain_stem_alignment.py       # -ain stem alignment; partial R6 alignment
│   ├── ROSETTA3b_expanded_alignment.py      # 200-entry lexicon alignment; sal Tier 1; qok- null
│   ├── ROSETTA3c_qotaiin_positional.py      # Packet-internal position; qokain/laiin/ai!n/qotaiin/lkaiin
│   ├── ROSETTA3d_stolfi_zl_replication.py   # ZL cross-transliteration boundary test (ROSETTA3d)
│   ├── ROSETTA4_sal_terminal_baseline.py    # sal pre-R2 baseline; confirms RETRACTED-001
│   ├── FRAME1_structural_token_alignment.py
│   ├── ILLUS1_content_token_illustration_alignment.py  # 44 Rosetta candidates
│   ├── PILOT4_balneo_packet_structure.py    # B-section packet grammar; FALSIFIED-001
│   └── PILOT5_ain_subfolio_analysis.py      # -ain positional sub-differentiation; FALSIFIED-002
├── results/
│   ├── p1_1_cluster_frequencies.csv         # 47 classified clusters with role assignments (role_map)
│   ├── p1_2_section_profiles.csv            # Normalized role frequencies by section
│   ├── p1_3_falsification_v1.1_results.json # Inversion falsification 3/3 vs 0/3
│   ├── p1_4_classification_results.json     # 69.8% best section accuracy (KNN-5, 7-role); rf3b_triggered=true
│   ├── p1_6_transition_matrix.json          # 7×7 Markov transition matrix (R2→R1 z=+9.75)
│   ├── DECODE1_sal_results.json
│   ├── DECODE2_stars_ain_results.json
│   ├── DECODE3_qol_results.json             # qol first-payload OR=7.83 (P2-CLAIM-006)
│   ├── ROSETTA2_sal_packet_results.json     # sal enrichment 2.08× (P2-CLAIM-013)
│   ├── ROSETTA3_ain_alignment_results.json
│   ├── ROSETTA3b_expanded_results.json      # Tier verdicts; sal Tier 1; qok- null (P2-CLAIM-014, 016)
│   ├── ROSETTA3c_qotaiin_positional_results.json  # Positional claims 010, 011, 020, 021
│   ├── ROSETTA3d_stolfi_zl_results.json     # ZL boundary test; qokain/laiin/ai!n (ROSETTA3d)
│   ├── PILOT4_balneo_packet_results.json    # B-section 374/897 packets (P2-CLAIM-007, 008, 009)
│   └── PILOT5_ain_subfolio_results.json     # ai!n LATE corpus-wide (P2-CLAIM-012, 017)
├── annex_maps/
│   ├── PAPER_TO_REPO_MAP.md                 # Section-by-section paper→repo traceability
│   ├── ANNEX_B1_structural_paper1.md        # Proof table: Paper 1 structural claims
│   ├── ANNEX_B2_positional_paper2.md        # Proof table: positional claims (token-level)
│   ├── ANNEX_B3_lexical_candidates.md       # Proof table: lexical/semantic claims
│   ├── ANNEX_B4_grammatical_null.md         # Proof table: grammar/null-root claims
│   ├── ANNEX_B5_replication_crosstranscription.md  # Cross-transliteration outcomes
│   ├── ANNEX_B6_retracted_falsified.md      # All retracted and falsified claims
│   ├── ANNEX_B7_section_method.md           # Section-level and method-level claims
│   └── ANNEX_B8_verification_index.md       # Master index: all 30 claims, repo paths, status
├── docs/
│   ├── CLAIM_REGISTRY.md                    # Per-claim registry (ID, level, status, TC, repo path)
│   ├── RETRACTED_AND_FALSIFIED_CLAIMS.md    # Full record of retracted/falsified claims
│   ├── TRANSCRIPTION_SENSITIVITY_METHOD.md  # Eva-T vs Eva- taxonomy; ZL boundary-test framework
│   ├── R6_HEBREW_ALIGNMENT_METHOD.md        # R6 Hebrew preposition alignment method (P2-CLAIM-018)
│   ├── CONSISTENCY_AUDIT_POST_ANNEX.md      # Full audit; readiness assessment for ROSETTA3d restart
│   ├── TIER_REGISTRY.md                     # Tier 1/2/3 assignments for lexical candidates
│   ├── EXPECTED_OUTPUTS.md                  # Headline metrics for all scripts; use with smoke_test.py
│   └── TABLE_FIGURE_TRACEABILITY.md         # Every table/figure traced to its source script
└── pilots/
    ├── PILOT1_five_folio_results.md
    ├── PILOT2_stars_ain_log.md              # Stars -ain folio-anchor test; entity-label retraction
    ├── PILOT3_qol_ol_log.md                 # qol/ol inner-packet doublet analysis
    ├── PILOT4_balneo_packet_log.md          # B-section packets; nested-packet falsification
    ├── PILOT5_ain_subfolio_log.md           # -ain positional sub-differentiation
    ├── ROSETTA2_sal_packet_log.md           # sal enrichment; terminal-position (retracted)
    ├── ROSETTA3_ain_alignment_log.md
    ├── ROSETTA3b_expanded_alignment_log.md
    ├── ROSETTA3b_20260319/                  # Tier verdicts; ROSETTA3b/3c results
    ├── ROSETTA3d_20260319/                  # ZL boundary test; token identity freeze
    │   ├── TOKEN_IDENTITY_FREEZE.md         # ai!n ≠ aiin ≠ laiin; p-value scope resolution
    │   └── STOLFI_ZL_POSITIONAL_REPLICATION.md  # Full ROSETTA3d results
    └── NEW_FINDINGS_2026-03-19.md           # Consolidated batch findings
```

---

## Data Source

Primary corpus: Takahashi transliteration (transcriber code H) from the Landini-Stolfi Interlinear file (IVTFF format).
Available from: https://www.voynich.nu/transcr.html

The raw IVTFF source file is not included in this repository due to its provenance as community-maintained data. Download `Lsi_ivtff_0d_v4j_fixed.txt` from the above URL and place it in `data/`.

---

## Citation

Mumin, R. (2026a). *Positional Role Asymmetry in Voynich Manuscript EVA Clusters: A Functional Classification Framework with Falsification Protocol*. Manuscript draft.

Mumin, R. (2026b). *Transition Grammar and Cognitive Domain Profiles in the Voynich Manuscript: Evidence for a Functional Recording System from Six-Role Cluster Analysis*. Manuscript draft.

Mumin, R. (2026c). *The Stranded Recorder Hypothesis: The Voynich Manuscript as a Domain-Specific Notation System*. Manuscript draft.

All three papers are available at: https://roblemumin.com/library.html

---

## License

Code: [MIT License](LICENSE)
Data outputs (results/): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
