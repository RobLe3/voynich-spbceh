# Table and Figure Traceability
**Last updated**: 2026-03-19
**Policy**: Every table or figure in a paper must have a source script, input data path, and output artifact. If assembled manually, this must be stated.

---

## Paper 1 Tables

### Table 1 — Six-Role Taxonomy
- **Paper**: Paper 1, §3
- **Caption**: Six-role taxonomy with defining criterion, z-scores, and key tokens
- **Script**: `scripts/p1_cluster_analysis.py`
- **Input**: `data/corpus_tokens.csv`
- **Output**: `results/p1_1_cluster_frequencies.csv`
- **Manual edits**: Role labels (INIT, CLOSE, LINK, CONTENT, TEMPORAL, REF) are interpretive labels applied post-hoc to computationally derived clusters. The cluster assignments are script-derived; the role names are manually assigned based on positional criteria.
- **Status**: confirmed

### Table 2 — Section Profiles (Normalized Role Frequencies)
- **Paper**: Paper 1, §4
- **Caption**: Role frequency by section (S, B, H, C, T, Z)
- **Script**: `scripts/p1_cluster_analysis.py`
- **Input**: `data/corpus_tokens.csv`, `results/p1_1_cluster_frequencies.csv`
- **Output**: `results/p1_2_section_profiles.csv`
- **Manual edits**: None
- **Status**: confirmed

### Table 3 — Transition Matrix (6×6 Markov)
- **Paper**: Paper 1, §3.2
- **Caption**: Normalized transition probabilities between consecutive role pairs
- **Script**: `scripts/p1_cluster_analysis.py`
- **Output**: `results/p1_6_transition_matrix.json`
- **Manual edits**: None
- **Status**: confirmed

### Table 4 — Falsification Results
- **Paper**: Paper 1, §6
- **Caption**: Three coherence criteria for original vs. inverted taxonomy
- **Script**: `scripts/p1_3_falsification.py`
- **Output**: `results/p1_3_falsification_v1.1_results.json`
- **Manual edits**: None
- **Status**: confirmed

### Table 5 — Anti-Projection Test (31 alternatives)
- **Paper**: Paper 1, §5
- **Caption**: 31 alternative role groupings ranked by three metrics
- **Script**: `scripts/p2_5_6role_rerun.py`
- **Manual edits**: None
- **Status**: confirmed

---

## Paper 2 Tables

### Table 1 — FSA Conformance and Entropy
- **Paper**: Paper 2, §3
- **Caption**: FSA conformance rate, entropy decomposition
- **Script**: `scripts/p2_analysis.py`
- **Manual edits**: None
- **Status**: confirmed

### Table 2 — Section Classification Accuracy
- **Paper**: Paper 2, §4.1
- **Caption**: Leave-one-folio-out classification accuracy by section
- **Script**: `scripts/p1_4_classification.py`
- **Output**: `results/p1_4_classification_results.json`
- **Manual edits**: None
- **Status**: confirmed

### Table 3 — Three-Layer Model Summary
- **Paper**: Paper 2, §5
- **Caption**: Layer assignments with enrichment ratios and section profiles
- **Script**: Multiple: `DECODE3_qol_cluster.py`, `ILLUS1_content_token_illustration_alignment.py`, `DECODE1_sal_cluster.py`
- **Manual edits**: Layer-to-token assignments synthesized from multiple script outputs; the synthesis step is manual
- **Note**: This table's assembly is partially manual — the enrichment figures are script-derived but the three-layer classification is interpretive
- **Status**: PROVISIONAL (manual synthesis step)

### Table 4 — Positional Sub-Differentiation (-ain family)
- **Paper**: Paper 2, §5.2
- **Caption**: qokain, laiin, ai!n positional positions and p-values
- **Script**: `scripts/PILOT5_ain_subfolio_analysis.py`, `scripts/ROSETTA3c_qotaiin_positional.py`
- **Output**: `results/PILOT5_ain_subfolio_results.json`, `results/ROSETTA3c_qotaiin_positional_results.json`
- **Manual edits**: None
- **Status**: confirmed (ROSETTA3c re-validation)

### Table 5 — ROSETTA3b Alignment Tier Table
- **Paper**: Paper 2, §7.3 (candidate alignment summary)
- **Caption**: Token | Stem | Arabic Candidate | Latin Candidate | Tier | Status
- **Script**: `scripts/ROSETTA3b_expanded_alignment.py`
- **Output**: `results/ROSETTA3b_expanded_results.json`
- **Manual edits**: Tier assignments (1/2-3/Reject/Null) are interpretive judgments applied post-scoring; competing-reading comparison is manual
- **Note**: The tier system is a judgment call — competing-reading test requires domain knowledge not encoded in the script
- **Status**: PROVISIONAL (tier assignments manual)

### Table 6 — Pilot/ROSETTA Result Summary (§9 Future Work)
- **Paper**: Paper 2, §9
- **Caption**: Summary of pilot results and their verification status
- **Script**: Multiple (all ROSETTA, PILOT scripts)
- **Manual edits**: This summary table is manually assembled from pilot logs
- **Status**: PROVISIONAL (manually assembled)

---

## Figures

### Figure 1 (Paper 1) — Role Position Distributions
- Not currently rendered as a figure in paper; embedded as inline statistics
- Source: `scripts/p1_cluster_analysis.py`

### Figure 2 (Paper 2) — Packet Grammar FSA Diagram
- **Type**: Manually drawn (TikZ in TeX source)
- **Source**: Conceptual; states (OPEN, PAYING, CLOSED) defined by role analysis
- **Manual edits**: Entire figure is manually constructed from structural findings
- **Note**: This figure is illustrative, not computationally generated

---

## Manual Assembly Notes

The following tables/content in the papers contain manually synthesized elements:
- Paper 2, Table 3 (Three-layer model): synthesis of multiple script outputs
- Paper 2, Table 5 (ROSETTA3b tier table): tier and competing-reading judgments
- Paper 2, Table 6 (pilot summary): assembled from pilot logs
- Paper 1, Table 1 (taxonomy labels): role names are interpretive post-hoc labels
- Paper 2, Figure 1 (FSA diagram): fully manual TikZ construction

All manual synthesis steps are noted here and should be flagged in annex descriptions.
