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
| `results/p1_1_cluster_frequencies.csv` | 47 classified clusters; INIT 11 types (10 with qok- prefix + fachys), CLOSE 10 types |
| `results/p1_2_section_profiles.csv` | Role frequencies by section (H, P, B, Z, ...) |
| `results/p1_6_transition_matrix.json` | `zscores["CLOSE"]["INIT"]["z"]` = +9.753 (rounds to +9.75); 7-role model |

---

## p1_3_falsification.py → `results/`

| File | Key metric |
|------|-----------|
| `results/p1_3_falsification_v1.1_results.json` | Original wins ≥2/3 metrics vs both alternatives |

---

## p1_4_classification.py → `results/`

| File | Key metric |
|------|-----------|
| `results/p1_4_classification_results.json` | Section classification accuracy = 69.8% KNN-5 (7-role); baseline 57.8% |

---

## p2_analysis.py → `results/`

**Single consolidated output file** (not separate per-task files):

| File | JSON key path | Confirmed value |
|------|--------------|----------------|
| `results/p2_all_results.json` | `p2_1.para_level.pct_conformant_trans` | 61.3% paragraph FSA conformance |
| `results/p2_all_results.json` | `p2_2.pct_sealed` | 9.0% sealed paragraphs |
| `results/p2_all_results.json` | `p2_2.pct_open` | 91.0% open paragraphs |
| `results/p2_all_results.json` | `p2_3.daiin.count` | 748 |
| `results/p2_all_results.json` | `p2_3.daiin.CV` | 1.502 (clustered, not periodic) |
| `results/p2_all_results.json` | `p2_4.H_structural` | 2.5953 bits (7-role model) |
| `results/p2_all_results.json` | `p2_4.H_variant` | 2.4949 bits (7-role model) |
| `results/p2_all_results.json` | `p2_5.original_ranks` | TS=12/31, Classification=6/31, Markov=5/31 (7-role) |

**Note**: The 7-role model (p2_analysis.py) does NOT satisfy the entropy prediction (H_structural > H_variant). The 6-role model (p2_5_6role_rerun.py) does satisfy it. Paper 2 reports 6-role values.

---

## p2_5_6role_rerun.py → `results/`

**Single output file** implementing the true 6-role model (ACT+MODE merged into CONTENT):

| File | JSON key path | Confirmed value |
|------|--------------|----------------|
| `results/p2_5_v2_6role_results.json` | `p14_cls_accuracy` | 0.6473 = **64.7%** (6-role classification accuracy) |
| `results/p2_5_v2_6role_results.json` | `p16_close_init_z` | **9.713** (rounds to +9.71; 6-role model) |
| `results/p2_5_v2_6role_results.json` | `p24_entropy.H_structural` | **2.3787 bits** (6-role) |
| `results/p2_5_v2_6role_results.json` | `p24_entropy.H_variant` | **2.7668 bits** (6-role) |
| `results/p2_5_v2_6role_results.json` | `p24_entropy.prediction_holds` | `true` (H_structural < H_variant ✅) |
| `results/p2_5_v2_6role_results.json` | `p25_v2.original_scores.cls` | 0.6473 |
| `results/p2_5_v2_6role_results.json` | `p25_v2.original_ranks.cls` | **3/31** (Classification rank) |
| `results/p2_5_v2_6role_results.json` | `p25_v2.original_ranks.markov` | **5/31** (Markov rank) |
| `results/p2_5_v2_6role_results.json` | `p25_v2.original_ranks.ts` | 19/31 (TS metric biased toward simpler models) |

---

## Lexical + pilot scripts

| Script | Output file | Key metric |
|--------|------------|-----------|
| `DECODE3_qol_cluster.py` | `results/DECODE3_qol_results.json` | qol OR = 7.83 at first-payload position; Pearson r = 0.940 with ol; follows structural tokens in 53/105 = 50.5% of occurrences |
| `ROSETTA2_sal_packet_position.py` | `results/ROSETTA2_sal_packet_results.json` | sal 2.08× enriched in Balneological section |
| `PILOT4_balneo_packet_structure.py` | `results/PILOT4_balneo_packet_results.json` | **897 total packets** (Takahashi H primary corpus); 374/897 (41.7%) in B-section; 0/67 sub-CLOSE (nested packets FALSIFIED) |
| `ROSETTA3c_qotaiin_positional.py` | `results/ROSETTA3c_qotaiin_positional_results.json` | 896 packets (section-restricted scope; 1 fewer than PILOT4 due to scope difference); laiin LATE (Stars packets, p=0.007); qotaiin CENTRAL (p=0.388) |
| `ROSETTA3d_stolfi_zl_replication.py` | `results/ROSETTA3d_stolfi_zl_results.json` | ZL packet count: 886 vs Takahashi H 897 (PILOT4) — 99% match |
| `R6_hebrew_alignment.py` | `results/R6_hebrew_alignment_results.json` | al → Hebrew על/אל full-glyph match; 52.6% claimed rate not reproducible with 3-type pool |

---

## Notes

- All numbers above are from confirmed script runs committed to `results/`.
- **z-score disambiguation**: Paper 1 uses z=+9.75 (7-role, `p1_cluster_analysis.py`). Paper 2 uses z=+9.71 (6-role, `p2_5_6role_rerun.py`). These are not in conflict — they measure the same signal under different role-count models.
- **Packet count**: PILOT4 = 897 (canonical, full corpus). ROSETTA3c = 896 (section-restricted). Cross-transliteration (ZL) = 886. All reflect the same grammar; differences are scope/transliteration artifacts.
- **H(structural) vs H(variant)**: The entropy prediction (H_str < H_var) holds only under the 6-role model. Under 7-role it is reversed. Paper 2 reports 6-role values only.
- If your run produces different numbers, check that `data/Lsi_ivtff_0d_v4j_fixed.txt` is the correct IVTFF file (Takahashi H transcription, Landini-Stolfi Interlinear format).
- Cross-transliteration test (`p1_5_cross_transliteration.py`) requires `data/takahashi.txt` — a plain-text standalone Takahashi file. If absent, the script will fail at file read.
