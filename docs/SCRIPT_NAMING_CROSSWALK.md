# Script Naming Crosswalk
**Purpose**: Map working-directory script names (`research/`) to formal repo script names (`scripts/`) and paper citations.
**Last updated**: 2026-03-20

---

## Formal scripts/ ↔ Research/ working scripts

| Formal script (`scripts/`) | Research working name | Paper citation | CLAIM_REGISTRY |
|----------------------------|-----------------------|---------------|----------------|
| `scripts/p1_cluster_analysis.py` | `research/P1_structural/` corpus analysis | Paper 1 §3, §4, §5 | P1-CLAIM-002 through P1-CLAIM-008 |
| `scripts/p1_3_falsification.py` | `research/P1_structural/` falsification task | Paper 1 §6 | P1-CLAIM-003 |
| `scripts/p1_4_classification.py` | `research/P1_structural/` classification task | Paper 1 §7 | P2-CLAIM-003 |
| `scripts/p2_analysis.py` | Multiple: `research/P2_cognitive/` tasks | Paper 2 §3, §4.1, §5.1 | P2-CLAIM-001, P2-CLAIM-002, P2-CLAIM-022 |
| `scripts/p2_5_6role_rerun.py` | `research/P2_cognitive/W2.1–W2.3` | Paper 2 §3.1 | P1-CLAIM-001 |
| `scripts/DECODE3_qol_cluster.py` | `research/DECODE3` internal | Paper 2 §5.1 | P2-CLAIM-006 |
| `scripts/ILLUS1_content_token_illustration_alignment.py` | `research/ILLUS1` | Paper 2 §5 | P2-CLAIM-019 |
| `scripts/PILOT4_balneo_packet_structure.py` | `research/PILOT4` → later formalized | Paper 2 §4.3 | P2-CLAIM-007, P2-CLAIM-008, P2-CLAIM-009 |
| `scripts/PILOT5_ain_subfolio_analysis.py` | `research/PILOT5` | Paper 2 §5.2 | P2-CLAIM-010, P2-CLAIM-011, P2-CLAIM-012, P2-CLAIM-017 |
| `scripts/ROSETTA2_sal_packet_position.py` | `research/rosetta/ROSETTA2` | Paper 2 §7.3 | P2-CLAIM-013 |
| `scripts/ROSETTA3b_expanded_alignment.py` | `research/rosetta/ROSETTA3b` | Paper 2 §7.3 | P2-CLAIM-014, P2-CLAIM-016 |
| `scripts/ROSETTA3c_qotaiin_positional.py` | `research/rosetta/ROSETTA3c` | Paper 2 §5.2, footnote | P2-CLAIM-010, P2-CLAIM-011, P2-CLAIM-020, P2-CLAIM-021 |
| `scripts/ROSETTA3d_stolfi_zl_replication.py` | `research/rosetta/ROSETTA3d` | Paper 2 §4.4 | P2-CLAIM-010 (downgrade), cross-transcription |
| `scripts/R6_hebrew_alignment.py` | `research/LC2` (partial) | Paper 2 §6.1 | P2-CLAIM-018 |
| `scripts/DECODE2_token_section_positions.py` | Related to `research/DECODE2`, `MORPH1` | Paper 2 (supplementary) | Not formally registered |

---

## Research-only scripts (no formal `scripts/` equivalent)

| Research script | Content | Paper relevance | CLAIM_REGISTRY |
|-----------------|---------|-----------------|----------------|
| `research/CON1_context_dependent_tokens.py` | Section-specific token distributions (70% of top-50) | Informs Paper 2 §4 domain profiles | SUPP-CON1 |
| `research/CON2_morphological_decomposition.py` | Morphological compression (1.76×); `-dy` bias | Informs Paper 2 §5 three-layer model | SUPP-CON2 |
| `research/CON3_packet_semantic_clustering.py` | k=8 KMeans on packets; Cluster 1 = shedy-dominated | **Source of P2-CLAIM-004** (misattributed to p2_analysis.py) | P2-CLAIM-004 |
| `research/CON4_cross_section_identity.py` | Universal tokens VARIABLE (cosine 0.045 vs null 0.102) | Paper 2 §4.3 (added 2026-03-20) | P2-CLAIM-026 |
| `research/CON5_illustration_packet_correlation.py` | Per-folio Cluster-1 rate; B=15.2%, H=1.5%, U=1943.5 | **Source of P2-CLAIM-004** numerical values | P2-CLAIM-004 |
| `research/CT1_content_token_analysis.py` | Position-exclusive types (70-84%); suffix analysis | Informs three-layer model | SUPP-CT1 |
| `research/LC1_hebrew_cipher_test.py` | Hebrew cipher structural test (weak support, 2:3) | Informs Paper 2 §6.1 limitations | SUPP-LC1 |
| `research/LC2_structural_cipher_test.py` | R6 Hebrew function word alignment 52.6% | **Source of P2-CLAIM-018** 52.6% figure | P2-CLAIM-018 |
| `research/loop3b/loop3b_analysis.py` | Multi-task loop: Currier A/B, Zodiac, fractal, multi-scale | Paper 2 §3.3, §4.2, §4.3 (added 2026-03-20) | P2-CLAIM-023, P2-CLAIM-024, P2-CLAIM-025 |
| `research/IA4_language_comparison_log.md` | Zipf, hapax, Hebrew z-score comparison | Paper 2 §6 (informs limitations) | SUPP-IA4 |
| `research/IA5_semantic_validation_log.md` | 1/4 semantic sub-labels confirmed | Drove 7→6 role merger | SUPP-IA5 |

---

## Known naming mismatches

| Paper citation | Actual source | Resolution |
|---------------|---------------|------------|
| "PILOT2" in Paper 3 §3 | `research/rosetta/ROSETTA2` or local PILOT2 | Paper 3 cites "PILOT2" for zodiac recto/verso consistency test; check Paper 3 draft |
| `scripts/p2_analysis.py` (P2-CLAIM-004 original) | `research/CON3→CON5` chain | RESOLVED 2026-03-20; CLAIM_REGISTRY updated |
| "MORPH1" in pilot logs | Related to `scripts/DECODE2` + `scripts/PILOT5` | No formal scripts/ equivalent; MORPH1 is a working label only |
| "PILOT1" in research log | Maps to early token clustering (pre-formalization) | Not the same as any scripts/PILOT*.py; naming collision |
| "PILOT3" in Paper 3 | May refer to a local PILOT3 or to research/PILOT3 | Check Paper 3 §3 citation when preparing final draft |

---

## How to add new entries

When creating a new formal script in `scripts/`:
1. Add a row to the first table above.
2. If it formalizes a `research/` analysis, update the second table to mark it as "formalized as `scripts/X.py`".
3. Update the CLAIM_REGISTRY `repo path` field to point to the formal `scripts/` path.
