# Expected Outputs

**Purpose**: Reference for verifying that scripts produce the correct headline metrics. Compare against these values after running `scripts/reproduce.sh`.

---

## parse_corpus.py → `data/`

| File | Key metric |
|------|-----------|
| `data/corpus_tokens.csv` | 37,045 tokens (transcriber H) |
| `data/corpus_lines.csv` | Line-level records |

---

## p1_cluster_analysis.py → `results/`

| File | Key metric |
|------|-----------|
| `results/p1_1_cluster_frequencies.csv` | 47 classified clusters; INIT 10 types, CLOSE 10 types |
| `results/p1_2_section_profiles.csv` | Role frequencies by section (H, P, B, Z, ...) |
| `results/p1_6_transition_matrix.json` | R2→R1 z = +9.71 |

---

## p1_3_falsification.py → `results/`

| File | Key metric |
|------|-----------|
| `results/p1_3_falsification_v1.1_results.json` | Original 3/3 metrics pass; inverted 0/3; shuffled 0/3 |

---

## p1_4_classification.py → `results/`

| File | Key metric |
|------|-----------|
| `results/p1_4_classification_results.json` | Section classification accuracy = 64.7% (baseline 57.8%) |

---

## p2_analysis.py → `results/`

| File | Key metric |
|------|-----------|
| `results/p2_fsa_conformance.json` | `paragraph_fsa_conformance` = 0.613 (pre-registered threshold: 0.60) |
| `results/p2_entropy.json` | H(structural) = 2.38 bits < H(variant) = 2.77 bits |
| `results/p2_section_classification.json` | 64.7% (Kruskal-Wallis *p* < 0.0001) |
| `results/p2_domain_coherence.json` | shedy: 10× elevation B vs H (*p* < 0.0001) |
| `results/p2_daiin_analysis.json` | CV = 1.502 (non-periodic; above Poisson threshold 1.0) |

---

## Lexical + pilot scripts

| Script | Output file | Key metric |
|--------|------------|-----------|
| `DECODE3_qol_cluster.py` | `results/DECODE3_qol_results.json` | qol OR = 7.83 at first-payload position; Pearson r = 0.940 with ol |
| `ROSETTA2_sal_packet_position.py` | `results/ROSETTA2_sal_packet_results.json` | sal 2.08× enriched in Balneological section |
| `PILOT4_balneo_packet_structure.py` | `results/PILOT4_balneo_packet_results.json` | 374/897 packets in B-section (41.7%); 0/67 sub-CLOSE (nested packets FALSIFIED) |
| `ROSETTA3c_qotaiin_positional.py` | `results/ROSETTA3c_qotaiin_positional_results.json` | laiin LATE (Stars packets, p=0.007); qotaiin CENTRAL (p=0.388) |
| `ROSETTA3d_stolfi_zl_replication.py` | `results/ROSETTA3d_stolfi_zl_results.json` | ZL packet count: 886 vs Takahashi H 897 |
| `R6_hebrew_alignment.py` | `results/R6_hebrew_alignment_results.json` | al → Hebrew על/אל full-glyph match; 52.6% claimed rate not reproducible with 3-type pool |

---

## Notes

- All numbers above are from the confirmed run archived in `results/`.
- If your run produces different numbers, check that `data/Lsi_ivtff_0d_v4j_fixed.txt` is the correct IVTFF file (Takahashi H transcription, Landini-Stolfi Interlinear format).
- Cross-transliteration test (`p1_5_cross_transliteration.py`) requires `data/takahashi.txt` — a plain-text standalone Takahashi file. If absent, the script will fail at file read.
