# Annex B.8 — Claim Verification Index
**Table**: Master index of all 30 active claims in Papers 1 and 2.
**Purpose**: Allows a reviewer to locate any claim's annex table, current status, claim level, transcription comparability, and primary repo artifact in a single lookup.
**Source**: `docs/CLAIM_REGISTRY.md` (current post-ZL, post-registry state, 2026-03-19; updated 2026-03-19 to add P2-CLAIM-022)

---

## How to use this index

1. Find the claim by ID (P1-CLAIM-NNN or P2-CLAIM-NNN)
2. Read the Status and TC columns to understand current confidence level and cross-transliteration scope
3. Follow the Annex link to the proof table with full method details
4. Follow the Repo Artifact link to the script or output file for reproduction

**Status codes**: `CONFIRMED` | `PROVISIONAL` | `RETRACTED` | `FALSIFIED` | `CONFIRMED + CROSS-TRANSCRIPTION_PENDING`
**TC codes**: `DIRECT` | `NORMALIZATION_REQUIRED` | `TRANSCRIPTION-BOUND` | `NOT_TESTABLE_ACROSS_ZL` | `CROSS-TRANSCRIPTION_COMPARABLE` | `NOT_APPLICABLE`
**Level codes**: `TOKEN-LEVEL` | `FAMILY-LEVEL` | `SECTION-LEVEL` | `METHOD-LEVEL`

---

## Paper 1 Claims

| Claim ID | Statement (brief) | Level | Status | TC | Annex | Repo Artifact |
|----------|-------------------|-------|--------|-----|-------|---------------|
| P1-CLAIM-001 | Six-role taxonomy best-supported among 31 alternatives by anti-projection test | `METHOD-LEVEL` | `CONFIRMED` | `DIRECT` | B.1 | `scripts/p2_5_6role_rerun.py` |
| P1-CLAIM-002 | R2→R1 transition z=+9.71 is the single strongest signal in the corpus | `SECTION-LEVEL` | `CONFIRMED` | `DIRECT` | B.1 | `scripts/p1_cluster_analysis.py` → `results/p1_6_transition_matrix.json` |
| P1-CLAIM-003 | Inversion falsification: original 3/3 coherent; inverted 0/3 coherent | `METHOD-LEVEL` | `CONFIRMED` | `NOT_APPLICABLE` | B.1 | `scripts/p1_3_falsification.py` → `results/p1_3_falsification_v1.1_results.json` |
| P1-CLAIM-004 | Cross-transliteration r=0.937 for R1/R2 positional percentages | `SECTION-LEVEL` | `CONFIRMED` | `CROSS-TRANSCRIPTION_COMPARABLE` | B.1, B.5 | `scripts/p1_cluster_analysis.py` |
| P1-CLAIM-005 | Section role profiles significant across all 6 roles (KW p < 0.0001) | `SECTION-LEVEL` | `CONFIRMED` | `DIRECT` | B.1 | `scripts/p1_cluster_analysis.py` → `results/p1_2_section_profiles.csv` |
| P1-CLAIM-006 | `qok-` prefix exclusive to all 10 R1 (INIT) token types | `TOKEN-LEVEL` | `CONFIRMED` | `DIRECT` | B.1 | `scripts/p1_cluster_analysis.py` → `results/p1_1_cluster_frequencies.csv` |
| P1-CLAIM-007 | R2 types reduce to 3 consonant stems × 4 suffix variants | `FAMILY-LEVEL` | `CONFIRMED` | `DIRECT` | B.1 | `scripts/p1_cluster_analysis.py` → `results/p1_1_cluster_frequencies.csv` |
| P1-CLAIM-008 | `ch`/`sh` R2 alternation tracks domain (B vs S sections) | `FAMILY-LEVEL` | `CONFIRMED` | `DIRECT` | B.1 | `scripts/p2_analysis.py` |

---

## Paper 2 Claims

| Claim ID | Statement (brief) | Level | Status | TC | Annex | Repo Artifact |
|----------|-------------------|-------|--------|-----|-------|---------------|
| P2-CLAIM-001 | FSA paragraph-level conformance 61.3% ≥ 60% pre-registered threshold | `METHOD-LEVEL` | `CONFIRMED` | `DIRECT` | B.4 | `scripts/p2_analysis.py` |
| P2-CLAIM-002 | H(structural)=2.38 bits < H(variant)=2.77 bits (entropy decomposition) | `METHOD-LEVEL` | `CONFIRMED` | `DIRECT` | B.4 | `scripts/p2_analysis.py` |
| P2-CLAIM-003 | Section classification accuracy 64.7% vs 57.8% majority-class baseline | `SECTION-LEVEL` | `CONFIRMED` | `DIRECT` | B.7 | `scripts/p1_4_classification.py` → `results/p1_4_classification_results.json` |
| P2-CLAIM-004 | `shedy` cluster 10× elevated in B vs H (Mann-Whitney p < 0.0001) | `TOKEN-LEVEL` | `CONFIRMED` | `DIRECT` | B.7 | `scripts/p2_analysis.py` |
| P2-CLAIM-005 | Three-layer structural model (frame / inner-function / lexical entities) | `METHOD-LEVEL` | `CONFIRMED` (layers 1–2); `PROVISIONAL` (layer 3) | `DIRECT` | B.7 | `scripts/DECODE3_qol_cluster.py` + `scripts/ILLUS1_content_token_illustration_alignment.py` |
| P2-CLAIM-006 | `qol` first-payload slot OR=7.83 in B-section packets (p < 0.01) | `TOKEN-LEVEL` | `CONFIRMED` | `DIRECT` | B.2 | `scripts/DECODE3_qol_cluster.py` → `results/DECODE3_qol_results.json` |
| P2-CLAIM-007 | B-section accounts for 374/897 packets (41.7%; density 2.26×) | `SECTION-LEVEL` | `CONFIRMED` | `DIRECT` | B.4, B.7 | `scripts/PILOT4_balneo_packet_structure.py` + `scripts/ROSETTA3c_qotaiin_positional.py` |
| P2-CLAIM-008 | Nested B-section sub-packets: 0/67 — nested grammar FALSIFIED | `METHOD-LEVEL` | `FALSIFIED` | `NOT_APPLICABLE` | B.4, B.6 | `scripts/PILOT4_balneo_packet_structure.py` |
| P2-CLAIM-009 | INIT-bleed rates: B 17.9%, S 7.9%, H 6.4% | `SECTION-LEVEL` | `CONFIRMED` | `DIRECT` | B.4, B.7 | `scripts/PILOT4_balneo_packet_structure.py` |
| P2-CLAIM-010 | `qokain` (no `!`) EARLY in Stars packets (mean 0.248, p=0.007) | `TOKEN-LEVEL` | `PROVISIONAL` | `TRANSCRIPTION-BOUND` | B.2, B.5 | `scripts/ROSETTA3c_qotaiin_positional.py` + `scripts/ROSETTA3d_stolfi_zl_replication.py` |
| P2-CLAIM-011 | `laiin` LATE in Stars packets (mean 0.875, p=0.007) | `TOKEN-LEVEL` | `CONFIRMED` + `CROSS-TRANSCRIPTION_PENDING` | `NOT_TESTABLE_ACROSS_ZL` | B.2, B.5 | `scripts/ROSETTA3c_qotaiin_positional.py` |
| P2-CLAIM-012 | `ai!n` LATE corpus-wide (mean 0.686, n=23, p=0.005) | `TOKEN-LEVEL` | `CONFIRMED` + `CROSS-TRANSCRIPTION_PENDING` | `NOT_TESTABLE_ACROSS_ZL` | B.2, B.5 | `scripts/PILOT5_ain_subfolio_analysis.py` |
| P2-CLAIM-013 | `sal` enriched 2.08× in B-section | `TOKEN-LEVEL` | `CONFIRMED` | `DIRECT` | B.3 | `scripts/ROSETTA2_sal_packet_position.py` → `results/ROSETTA2_sal_packet_results.json` |
| P2-CLAIM-014 | `sal` Tier 1: `sl`=`sl` (Latin *sal/salus*), Balneological coherence | `TOKEN-LEVEL` | `CONFIRMED` (lexical triple) | `NOT_APPLICABLE` | B.3 | `scripts/ROSETTA3b_expanded_alignment.py` → `results/ROSETTA3b_expanded_results.json` |
| P2-CLAIM-015 | `sal` terminal pre-R2 positional pattern (4/17, 24%) ← **RETRACTED** | `TOKEN-LEVEL` | `RETRACTED` | `NOT_APPLICABLE` | B.6 | `scripts/ROSETTA3c_qotaiin_positional.py` (falsification run) |
| P2-CLAIM-016 | `qok-` null alignment: 0 lexical root matches → confirmed INIT morpheme | `TOKEN-LEVEL` | `CONFIRMED` (null) | `NOT_APPLICABLE` | B.3, B.4 | `scripts/ROSETTA3b_expanded_alignment.py` |
| P2-CLAIM-017 | `-ain` folio-uniqueness (67.6%) is entity-label evidence ← **FALSIFIED** | `METHOD-LEVEL` | `FALSIFIED` | `DIRECT` | B.6 | `scripts/PILOT5_ain_subfolio_analysis.py` |
| P2-CLAIM-018 | R6 tokens align with Hebrew prepositions at 52.6% (PROVISIONAL) | `FAMILY-LEVEL` | `PROVISIONAL` | `NORMALIZATION_REQUIRED` | B.3 | `scripts/ROSETTA3_ain_stem_alignment.py` (partial) |
| P2-CLAIM-019 | 44 Rosetta candidates: p<0.05 and enrichment >3× per illustration type | `TOKEN-LEVEL` | `PROVISIONAL` | `NORMALIZATION_REQUIRED` | B.3 | `scripts/ILLUS1_content_token_illustration_alignment.py` |
| P2-CLAIM-020 | `qotaiin` CENTRAL in Stars packets (p=0.388) — Tier 3 | `TOKEN-LEVEL` | `CONFIRMED` (null) | `DIRECT` | B.2 | `scripts/ROSETTA3c_qotaiin_positional.py` → `results/ROSETTA3c_qotaiin_positional_results.json` |
| P2-CLAIM-021 | `lkaiin` CENTRAL in Stars packets (p=0.943) — Tier 2 unresolved | `TOKEN-LEVEL` | `CONFIRMED` (null) | `DIRECT` | B.2 | `scripts/ROSETTA3c_qotaiin_positional.py` |
| P2-CLAIM-022 | `daiin` non-periodic (CV=1.502) and section-clustered (H: 35.6/1k, B: 10.8/1k) — R4 domain-modulated | `SECTION-LEVEL` | `CONFIRMED` | `DIRECT` | B.7c | `scripts/p2_analysis.py` |

---

## Summary by status and level

| Status | TOKEN-LEVEL | FAMILY-LEVEL | SECTION-LEVEL | METHOD-LEVEL | Total |
|--------|------------|--------------|--------------|-------------|-------|
| `CONFIRMED` | 11 | 2 | 6 | 3 | 22 |
| `CONFIRMED` + `CROSS-TRANSCRIPTION_PENDING` | 2 | 0 | 0 | 0 | 2 |
| `PROVISIONAL` | 1 | 1 | 0 | 0 | 2 |
| `PROVISIONAL` (layer 3 component) | 0 | 0 | 0 | 1 | 1 |
| `RETRACTED` | 1 | 0 | 0 | 0 | 1 |
| `FALSIFIED` | 0 | 0 | 0 | 2 | 2 |
| **Total** | **15** | **3** | **6** | **6** | **30** |

---

## Quick-access: claims by transcription comparability

| TC Status | Claim IDs |
|-----------|-----------|
| `CROSS-TRANSCRIPTION_COMPARABLE` | P1-CLAIM-004 |
| `DIRECT` | P1-CLAIM-001, 002, 003, 005, 006, 007, 008; P2-CLAIM-001, 002, 003, 004, 005, 006, 007, 009, 013, 017, 020, 021, 022 |
| `NORMALIZATION_REQUIRED` | P2-CLAIM-018, 019 |
| `TRANSCRIPTION-BOUND` | P2-CLAIM-010 |
| `NOT_TESTABLE_ACROSS_ZL` | P2-CLAIM-011, 012 |
| `NOT_APPLICABLE` | P1-CLAIM-003; P2-CLAIM-008, 014, 015, 016 |

---

## Reproduction verification commands

```bash
# Paper 1 primary results
cd scripts/
python3 p1_cluster_analysis.py     # P1-CLAIM-002, 004, 005, 006, 007, 008
python3 p1_3_falsification.py      # P1-CLAIM-003
python3 p1_4_classification.py     # P1-CLAIM-001 (anti-projection); P2-CLAIM-003

# Paper 2 primary results
python3 p2_analysis.py             # P2-CLAIM-001, 002, 004, 022
python3 PILOT4_balneo_packet_structure.py  # P2-CLAIM-007, 008, 009
python3 ROSETTA3c_qotaiin_positional.py    # P2-CLAIM-006, 010, 011, 020, 021
python3 PILOT5_ain_subfolio_analysis.py    # P2-CLAIM-012, 017
python3 ROSETTA3b_expanded_alignment.py   # P2-CLAIM-014, 016
python3 ROSETTA3d_stolfi_zl_replication.py  # B.5 cross-transcription boundary test
python3 ROSETTA2_sal_packet_position.py   # P2-CLAIM-013
python3 DECODE3_qol_cluster.py            # P2-CLAIM-006
```

Expected key outputs:
- `paragraph_fsa_conformance = 0.613` (P2-CLAIM-001)
- `R2->R1 z-score = 9.71` (P1-CLAIM-002)
- `B-section packets = 374/897` (P2-CLAIM-007)
- `qokain Stars mean = 0.248, p = 0.007` (P2-CLAIM-010)
