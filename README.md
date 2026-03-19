# SPBCEH — Voynich Manuscript Positional Role Analysis

**Semantic Pose-Based Cognitive Encoding Hypothesis (SPBCEH)**
Structural and functional analysis of the Voynich Manuscript (Beinecke MS 408) using transition-based positional role classification of EVA glyph clusters.

**Author**: Roble Mumin
**Status**: Active research, March 2026
**Papers**: [Paper 1](#paper-1) · [Paper 2](#paper-2)
**Zenodo archive**: *DOI pending deposit*

---

## Latest Results (2026-03-19)

### ROSETTA3 — Stem-consonant alignment (completed 2026-03-19)

Four findings from `-ain` family consonant alignment against Arabic astronomical (35 terms, al-Sufi tradition), Arabic/Hebrew balneological (25 terms), and Latin balneological (22 terms) lexicons:

1. **`sal` → Latin *sal* / *salus*: exact 2-consonant match** (sl = sl). Confirms the strongest entity-label candidate. Combined with terminal packet pattern (4/17 B-section packets end with `sal` before R2), this is the most tightly constrained alignment in the corpus.

2. **`qokain` alignment: NULL (significant negative)**. No Arabic or Hebrew term carries the `qk` consonant pair as a root. This is expected: `qok-` is the INIT grammatical particle (structural morpheme), not lexical content. The null result confirms `qok-` encodes grammatical role, not entity identity. Entity information in `qokain` resides in the `-ain` suffix alone.

3. **`lkaiin` → Latin *lacus* (lake/pool): exact 2-consonant match** (lk = lk). New candidate, low confidence — requires expanded testing. `lkaiin` is a Stars-section token; Latin *lacus* is balneological. Cross-domain exact match is either meaningful (celestial water bodies) or coincidental.

4. **Baseline limitation identified**: 90.5% of random stems match at score ≥ 0.5 — single-consonant alignments are not discriminating. Only 2-consonant exact matches are reportable. ROSETTA3b planned with full al-Sufi catalog (283 entries) and 2-consonant minimum threshold.

### ROSETTA2 / PILOT4 / PILOT5 batch (2026-03-19)

Three positional findings:

- **`qokain` has section-specific positional semantics** — EARLY-biased in Stars section packets (mean position 0.248, *p* = 0.007) but central in Balneological (mean 0.558, *p* = 0.40). First confirmed case of a single token occupying different structural slots by section.
- **`ai!n` is LATE-biased corpus-wide** (mean position 0.686, *p* = 0.005) — candidate terminal-entity marker across all sections.
- **`sal` shows a terminal-entity pattern** — immediately before R2 CLOSE in 24% of Balneological packet occurrences (4/17), elevated 1.44× inside packet payloads.

Two clean refutations:
- **Nested B-section packets**: REFUTED — 0/67 B-packets with INIT-first-payload contain a sub-CLOSE token. Grammar remains finite-state.
- **Folio-uniqueness as entity-label evidence**: RETRACTED — non-`-ain` rare tokens are equally folio-unique (74.8% vs 67.6%), confirming this is a baseline property of rare tokens.

Active next step: **ROSETTA3b** — full al-Sufi star catalog (283 entries), 2-consonant minimum threshold, per-stem-length baseline.

---

## Overview

The Voynich Manuscript has resisted decipherment for over a century. Rather than assuming it encodes natural language, this project classifies EVA-transcribed glyph clusters by their *positional behavior and functional role* within line and paragraph structures.

The central finding: EVA clusters exhibit **directional functional asymmetry** — their roles are not interchangeable without destroying structural coherence. The R2 (Closure-like) → R1 (Initiator-like) transition is the single strongest structural signal in the corpus (*z* = +9.71 vs. 1,000 shuffled baselines), anchoring a packet grammar that operates at the paragraph level. Paragraph-level FSA conformance reaches **61.3%**, exceeding the pre-registered 60% threshold.

These findings are **compatible with multiple interpretive hypotheses** (recording system, Hebrew/Semitic cipher, structured notation) and do not claim to translate the manuscript. The contribution is structural: establishing that a real, reproducible, falsification-tested grammar exists — a necessary foundation for any subsequent interpretive work.

---

## Six-Role Taxonomy (v2.0)

Derived from the original seven-role framework through empirical anti-projection testing. The R4/R5 merger (Action-like + Mode-like → Content) is data-driven, not arbitrary.

| Role | Label | Defining criterion | Key tokens |
|------|-------|-------------------|-----------|
| R1 | Initiator-like | Significantly elevated R2→R1 transition (*z*=+9.71); all 10 active types share exclusive `qok-` prefix | `qokeedy`, `qokeey`, `qokedy` |
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

## Paper 1

**Title**: Positional Role Asymmetry in Voynich Manuscript EVA Clusters: A Functional Classification Framework with Falsification Protocol

**Key results**:
- 7→6 role taxonomy via anti-projection testing
- R2→R1 *z* = +9.71; CLOSE→INIT packet grammar
- Section profiles significant across all roles (Kruskal-Wallis *p* < 0.0001)
- Falsification: original framework 3/3 coherent; inverted framework 0/3
- Cross-transliteration: Pearson *r* = 0.937 for positional % (Takahashi vs. Stolfi)

---

## Paper 2

**Title**: Transition Grammar and Cognitive Domain Profiles in the Voynich Manuscript: Evidence for a Functional Recording System from Six-Role Cluster Analysis

**Key results**:
- Paragraph-level FSA conformance: **61.3%** (pre-registered threshold: 60%)
- Entropy: H(structural) = 2.38 bits < H(variant) = 2.77 bits ✓
- Section classification accuracy: **64.7%** (majority-class baseline: 57.8%)
- `shedy`-cluster: 10× elevated in Balneological vs. Herbal (*p* < 0.0001)
- Three-way interpretive comparison: recording system (Model A), Hebrew cipher (Model B), structured notation (Model C)

---

## Reproducing the 61.3% FSA Conformance Result

```bash
# 1. Parse the corpus
cd scripts/
python parse_corpus.py \
  --input ../data/Lsi_ivtff_0d_v4j_fixed.txt \
  --output ../data/corpus_tokens.csv

# 2. Run cluster analysis (generates role assignments)
python p1_cluster_analysis.py \
  --corpus ../data/corpus_tokens.csv \
  --output ../results/p1_1_cluster_frequencies.csv

# 3. Run the Paper 2 FSA conformance analysis
python p2_analysis.py \
  --corpus ../data/corpus_tokens.csv \
  --roles ../results/p1_1_cluster_frequencies.csv \
  --output ../results/

# Expected output: paragraph_fsa_conformance = 0.613
```

**Requirements**: Python ≥ 3.9, pandas, numpy, scipy, scikit-learn

---

## Repository Structure

```
/
├── README.md
├── LICENSE
├── data/
│   ├── corpus_tokens.csv          # Parsed token-level corpus (37,045 tokens)
│   └── corpus_lines.csv           # Line-level corpus
├── scripts/
│   ├── parse_corpus.py            # IVTFF → CSV parser
│   ├── p1_cluster_analysis.py     # Role classification + positional stats
│   ├── p1_3_falsification.py      # Role inversion falsification test
│   ├── p1_4_classification.py     # Leave-one-folio-out section classifier
│   ├── p2_analysis.py             # FSA conformance + entropy decomposition
│   ├── p2_5_6role_rerun.py        # Anti-projection test (31 alternatives)
│   ├── DECODE1_sal_cluster.py     # sal co-occurrence analysis
│   ├── DECODE2_stars_ain.py       # Stars -ain folio-anchor analysis
│   ├── DECODE3_qol_cluster.py     # qol/ol correlation analysis
│   ├── MORPH1_ain_suffix_alignment.py
│   ├── ROSETTA1_balneological_alignment.py
│   ├── ROSETTA2_sal_packet_position.py  # sal packet enrichment + terminal position
│   ├── ROSETTA3_ain_stem_alignment.py   # -ain stem consonant alignment vs Arabic/Latin lexicons
│   ├── FRAME1_structural_token_alignment.py
│   ├── ILLUS1_content_token_illustration_alignment.py
│   ├── PILOT4_balneo_packet_structure.py # B-section packet grammar analysis
│   └── PILOT5_ain_subfolio_analysis.py  # -ain positional sub-differentiation
├── results/
│   ├── p1_1_cluster_frequencies.csv     # 47 classified clusters with role assignments
│   ├── p1_2_section_profiles.csv        # Normalized role frequencies by section
│   ├── p1_3_falsification_v1.1_results.json
│   ├── p1_4_classification_results.json # 64.7% accuracy result
│   ├── p1_6_transition_matrix.json      # 6×6 Markov transition matrix
│   ├── DECODE1_sal_results.json
│   ├── DECODE2_stars_ain_results.json
│   ├── DECODE3_qol_results.json
│   ├── ROSETTA2_sal_packet_results.json
│   ├── ROSETTA3_ain_alignment_results.json  # stem-consonant alignment; 90.5% baseline noted
│   ├── PILOT4_balneo_packet_results.json
│   └── PILOT5_ain_subfolio_results.json
└── pilots/
    ├── folio_pilot_5folios.md          # Three-layer analysis: f75r, f88r, f103r, f111v, f114v
    ├── stars_ain_alignment.md          # Stars -ain folio-anchor test (PILOT2)
    ├── qol_ol_doublet.md               # qol/ol inner-packet doublet analysis (PILOT3)
    ├── ROSETTA2_sal_packet_log.md      # sal packet-internal position analysis (ROSETTA2)
    ├── ROSETTA3_ain_alignment_log.md   # -ain stem alignment; baseline problem; qokain null result
    ├── PILOT4_balneo_packet_log.md     # Balneological packet structure analysis (PILOT4)
    ├── PILOT5_ain_subfolio_log.md      # -ain positional sub-differentiation (PILOT5)
    └── NEW_FINDINGS_2026-03-19.md      # Consolidated findings + falsifications (2026-03-19)
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

Archived at: *[Zenodo DOI pending]*

---

## License

Code: [MIT License](LICENSE)
Data outputs (results/): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
