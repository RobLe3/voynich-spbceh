# Paper-to-Repo Traceability Map
**Last updated**: 2026-03-19
**Purpose**: For each paper section, this file specifies which repo folder supports it, which pilot produced the result, which script computes it, and which output file contains the final numbers.

---

## PAPER 1 — v0.92 — Positional Role Asymmetry in Voynich Manuscript EVA Clusters

### §1 Introduction
- Claim group: Corpus description (37,045 tokens, Takahashi H transliteration)
- Script: `scripts/parse_corpus.py`
- Input: `data/Lsi_ivtff_0d_v4j_fixed.txt`
- Output: `data/corpus_tokens.csv`
- Status: **stable**

### §2 Data and Methods
- Script: `scripts/parse_corpus.py`
- Input: `data/Lsi_ivtff_0d_v4j_fixed.txt` (not in repo — external)
- Output: `data/corpus_tokens.csv`, `data/corpus_lines.csv`
- Note: Raw IVTFF source not included due to provenance — download from voynich.nu/transcr.html
- Status: **stable**

### §3.1 Role Taxonomy
- Claim group: Six-role taxonomy; R1 qok-prefix; R2 ch/sh/lch stems
- Script: `scripts/p1_cluster_analysis.py`
- Input: `data/corpus_tokens.csv`
- Output: `results/p1_1_cluster_frequencies.csv`
- Annex: Annex A, Table A.1
- Status: **confirmed**

### §3.2 R2→R1 Transition Signal (z = +9.71)
- Script: `scripts/p1_cluster_analysis.py`
- Output: `results/p1_6_transition_matrix.json`
- Annex: Annex A, Table A.2
- Status: **confirmed**

### §4.3 Section Profiles (Kruskal-Wallis p < 0.0001)
- Script: `scripts/p1_cluster_analysis.py`
- Output: `results/p1_2_section_profiles.csv`
- Annex: Annex A, Table A.2
- Status: **confirmed**

### §5.2 ch/sh Alternation
- Script: `scripts/p1_cluster_analysis.py`, `scripts/p2_analysis.py`
- Annex: Annex A, Table A.5
- Status: **confirmed**

### §6 Falsification Protocol (3/3 vs. 0/3)
- Script: `scripts/p1_3_falsification.py`
- Output: `results/p1_3_falsification_v1.1_results.json`
- Annex: Annex A, Table A.3
- Status: **confirmed**

### §7 Cross-Transliteration (r = 0.937)
- Script: `scripts/p1_cluster_analysis.py` (cross-transliteration section)
- Annex: Annex A, Table A.4
- Status: **confirmed**

### §8 Section Classification (64.7%)
- Script: `scripts/p1_4_classification.py`
- Output: `results/p1_4_classification_results.json`
- Annex: Annex A, Table A.5
- Status: **confirmed**

---

## PAPER 2 — v0.94 — Transition Grammar and Cognitive Domain Profiles

### §3 FSA Conformance (61.3%)
- Script: `scripts/p2_analysis.py`
- Input: `data/corpus_tokens.csv`, `results/p1_1_cluster_frequencies.csv`
- Annex: Annex B, Table B.1
- Verification: `python scripts/p2_analysis.py`
- Status: **confirmed**

### §3.2 Entropy Decomposition (H=2.38 < H=2.77)
- Script: `scripts/p2_analysis.py`
- Annex: Annex B, Table B.2
- Status: **confirmed**

### §4.1 Section Classification (64.7%)
- Script: `scripts/p1_4_classification.py`
- Output: `results/p1_4_classification_results.json`
- Annex: Annex B, Table B.3
- Status: **confirmed**

### §4.3 Domain Coherence — shedy 10× elevation
- Script: `scripts/p2_analysis.py`
- Annex: Annex B, Table B.4
- Status: **confirmed**

### §4.3 B-section packet density (374/897, 2.26×)
- Script: `scripts/PILOT4_balneo_packet_structure.py`, `scripts/ROSETTA3c_qotaiin_positional.py`
- Output: `results/PILOT4_balneo_packet_results.json`, `results/ROSETTA3c_qotaiin_positional_results.json`
- Pilot: `pilots/PILOT4_balneo_packet_log.md`
- Annex: Annex B, Table B.6
- Status: **confirmed** (verified by ROSETTA3c consistent FSA)

### §4.3 Nested packet REFUTED (0/67)
- Script: `scripts/PILOT4_balneo_packet_structure.py`
- Pilot: `pilots/PILOT4_balneo_packet_log.md` (addendum)
- Status: **falsified** (hypothesis killed — see `docs/RETRACTED_AND_FALSIFIED_CLAIMS.md` FALSIFIED-001)

### §5.1 Three-layer model / qol inner-function (r=0.940, OR=7.83)
- Script: `scripts/DECODE3_qol_cluster.py`
- Output: `results/DECODE3_qol_results.json`
- Pilot: `pilots/qol_ol_doublet.md`
- Annex: Annex B, Table B.5
- Status: **confirmed**

### §5.2 qokain EARLY (0.248, p=0.007) / laiin LATE (0.875, p=0.007) / ai!n LATE (0.686, p=0.005)
- Script: `scripts/PILOT5_ain_subfolio_analysis.py`, `scripts/ROSETTA3c_qotaiin_positional.py`, `scripts/ROSETTA3d_stolfi_zl_replication.py`
- Output: `results/PILOT5_ain_subfolio_results.json`, `results/ROSETTA3c_qotaiin_positional_results.json`, `results/ROSETTA3d_stolfi_zl_results.json`
- Pilot: `pilots/PILOT5_ain_subfolio_log.md`, `pilots/ROSETTA3d_20260319/TOKEN_IDENTITY_FREEZE.md`, `pilots/ROSETTA3d_20260319/STOLFI_ZL_POSITIONAL_REPLICATION.md`
- Annex: Annex B, Table B.7
- Status:
  - `qokain` EARLY: **PROVISIONAL** (downgraded — signal confined to n=7 no-! variant; qokai!n n=39 CENTRAL; family n=106 CENTRAL p=0.365; ZL normalization collapses qokain/qokai!n)
  - `laiin` LATE: **confirmed** (ROSETTA3c re-confirmed); ZL: TRANSCRIPTION_MISMATCH (laiin absent from ZL Stars packet payloads)
  - `ai!n` LATE: **confirmed** (Takahashi H); ZL: TRANSCRIPTION_MISMATCH (! marker Eva-T specific)

### §7.3 sal Balneological enrichment (2.08×) + Tier 1 alignment (sl→sal/salus)
- Scripts: `scripts/ROSETTA2_sal_packet_position.py`, `scripts/ROSETTA3b_expanded_alignment.py`, `scripts/ROSETTA3c_qotaiin_positional.py`
- Outputs: `results/ROSETTA2_sal_packet_results.json`, `results/ROSETTA3b_expanded_results.json`, `results/ROSETTA3c_qotaiin_positional_results.json`
- Pilots: `pilots/ROSETTA2_sal_packet_log.md`, `pilots/ROSETTA3b_20260319/ROSETTA3b_verdicts.md`, `pilots/ROSETTA3b_20260319/ROSETTA3c_results.md`
- Annex: Annex B, Table B.8
- Status: **confirmed** (enrichment + alignment); terminal-position claim **RETRACTED** (see RETRACTED-001)

### §7.3 qok- = INIT grammatical particle (NULL lexical alignment)
- Script: `scripts/ROSETTA3b_expanded_alignment.py`, `scripts/ROSETTA3_ain_stem_alignment.py`
- Output: `results/ROSETTA3b_expanded_results.json`
- Pilot: `pilots/ROSETTA3_ain_alignment_log.md`, `pilots/ROSETTA3b_20260319/ROSETTA3b_verdicts.md`
- Annex: Annex B, Table B.8
- Status: **confirmed** (null result)

### §9 Future Work — qotaiin/qt (Tier 3 after ROSETTA3c)
- Script: `scripts/ROSETTA3c_qotaiin_positional.py`, `scripts/ROSETTA3b_expanded_alignment.py`
- Output: `results/ROSETTA3c_qotaiin_positional_results.json`
- Status: **PROVISIONAL** — Tier 3; consonant selectivity only; no positional slot

### §9 Future Work — lkaiin/lk (Tier 2 ambiguous)
- Script: `scripts/ROSETTA3c_qotaiin_positional.py`, `scripts/ROSETTA3b_expanded_alignment.py`
- Status: **PROVISIONAL** — Tier 2; section ambiguity unresolved

---

## Pending Replication Items

Transcription comparability status codes follow `docs/TRANSCRIPTION_SENSITIVITY_METHOD.md`.

| Claim | TC Status | Replication path | Notes |
|-------|-----------|------------------|-------|
| qokain EARLY (0.248, p=0.007) | `TRANSCRIPTION-BOUND` | Requires 3rd transliteration encoding !-marker separately (e.g., RF Extended Eva) | ZL collapses qokain+qokai!n; tests different token; family CENTRAL (n=106, p=0.365) |
| laiin LATE (0.875, p=0.007) | `NOT_TESTABLE_ACROSS_ZL` | Requires transliteration that tokenizes laiin as single unit with stable paragraph conventions | ZL splits laiin in packet context; 0 in Stars packet payloads |
| ai!n LATE (0.686, p=0.005) | `NOT_TESTABLE_ACROSS_ZL` | Requires Eva-T compatible source | ! marker absent from ZL Eva-; not representable |
| R6 Hebrew preposition match (52.6%) | `NORMALIZATION_REQUIRED` | Full scoring method needs documentation | See docs/R6_HEBREW_ALIGNMENT_METHOD.md (pending) |
| 44 Rosetta candidates | `NORMALIZATION_REQUIRED` | Illustration-type data quality clarification | Enrichment confirmed; ground truth validation pending |
