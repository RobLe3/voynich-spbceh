# Annex B.7 — Section-Level and Method-Dependent Claims
**Table**: Proof table for claims that operate at section-level or depend on the SPBCEH method as a whole.
**Source**: `docs/CLAIM_REGISTRY.md`
**Primary paper**: Mumin (2026b) — Paper 2 §4 (domain profiles), §5 (three-layer model)

These claims characterize aggregate structural patterns at section level or at the method level. They are more robust to transcription variation than token-level claims because they aggregate over many tokens. All are `DIRECT`-testable across transliterations.

---

## B.7a — Section-level domain profile claims

| Claim ID | Level | Paper § | Feature | Section Scope | Transcription | n | Test | Null / Control | Observed Result | p / stat | Status | TC | Interpretation Bound | Repo Artifact |
|----------|-------|---------|---------|--------------|---------------|---|------|----------------|----------------|----------|--------|-----|---------------------|---------------|
| P2-CLAIM-003 | SECTION-LEVEL | P2 §4.1 | Section classification accuracy | 8 manuscript sections | Takahashi H | Per-folio (20 folios with known labels) | 1-NN leave-one-folio-out classifier; 6D role-frequency vector | Majority-class baseline = 57.8% | 64.7% classification accuracy | +6.9 pp over baseline | `CONFIRMED` | `DIRECT` | 6.9 percentage-point gain is suggestive but not decisive. Classifier uses role-frequency vectors; does not resolve what roles mean semantically. | `scripts/p1_4_classification.py` → `results/p1_4_classification_results.json` |
| P2-CLAIM-004 | TOKEN-LEVEL | P2 §4.3 | `shedy` R2 cluster elevation in B vs H | B and H sections | Takahashi H | Per-folio; Mann-Whitney U | Mann-Whitney U; NMI vs illustration type (20 IA-series folios) | Other sections and other R2 cluster types | `shedy`: B 15.2% vs H 1.5% per-folio rate (10×); Mann-Whitney p < 0.0001; NMI = 0.107 | p < 0.0001 | `CONFIRMED` | `DIRECT` | `shedy` is the B-specific R2 closure marker at grammar level. The `ch`/`sh` alternation tracks domain type at the level of individual R2 token identity, not only aggregate role frequency. | `scripts/p2_analysis.py` |
| P2-CLAIM-007 | SECTION-LEVEL | P2 §4.3 | B-section packet density (2.26×) | B vs. all sections | Takahashi H | 897 complete packets (ROSETTA3c consistent FSA) | Rate ratio: B-section packet count vs. B-section token share | Corpus-wide expected rate if packets were uniformly distributed | 374/897 = 41.7% of packets in B; B = 18.5% of corpus tokens; density = 2.26× average | — | `CONFIRMED` | `DIRECT` | ROSETTA3c confirmed with consistent FSA. `shedy` accounts for 59% of all `shedy`-closed packets in B; 31.6% of B-section packets close with `shedy`. | `scripts/PILOT4_balneo_packet_structure.py` + `scripts/ROSETTA3c_qotaiin_positional.py` |
| P2-CLAIM-009 | SECTION-LEVEL | P2 §4.3 | INIT-bleed rates by section | B, S, H sections | Takahashi H | Per-section packet sets | Rate comparison: % of packets whose first-payload token is INIT-classified | Section-specific baselines | B: 17.9%; S: 7.9%; H: 6.4% | — | `CONFIRMED` | `DIRECT` | INIT-bleed explained as dual-function `qok-` tokens in procedurally dense (B) text. Not nesting — falsified by FALSIFIED-001. | `scripts/PILOT4_balneo_packet_structure.py` |

---

## B.7b — Three-layer model (method-level synthesis)

| Claim ID | Level | Paper § | Feature | Scope | Status | TC | Interpretation Bound | Repo Artifact |
|----------|-------|---------|---------|-------|--------|-----|---------------------|---------------|
| P2-CLAIM-005 | METHOD-LEVEL | P2 §5 | Three-layer structural model (frame / inner-function / lexical entities) | Corpus-wide | `CONFIRMED` (layers 1–2); `PROVISIONAL` (layer 3) | `DIRECT` | **Layer 1** (frame tokens: R1/R2/R6): structurally confirmed by transition statistics, morphological regularity, cross-transliteration stability. **Layer 2** (inner-packet function words: `qol`): confirmed by section-profile correlation r=0.940 with `ol`, first-payload OR=7.83 (P2-CLAIM-006). **Layer 3** (lexical entities: 44 Rosetta candidates): confirmed at distributional level (P2-CLAIM-019); illustration-type ground truth quality uncertain. Layer labels are structural, not semantic — they do not determine what the layers encode. | `scripts/DECODE3_qol_cluster.py` + `scripts/ILLUS1_content_token_illustration_alignment.py` |

---

## B.7c — daiin analysis (structural validation)

| Feature | Claim Level | Test | Observed | Interpretation | Status |
|---------|------------|------|----------|---------------|--------|
| `daiin` periodicity | METHOD-LEVEL | Inter-occurrence CV | CV = 1.502 (> 1.5 = clustered, not periodic) | `daiin` is domain-clustered, not a corpus-wide periodic signal | `CONFIRMED` |
| `daiin` section rates | SECTION-LEVEL | Rate comparison | H: 35.6/1k tokens; P: 34.6/1k; B: 10.8/1k; Z: 8.3/1k | `daiin` is a domain-modulated content marker; 3× higher in content-intensive sections | `CONFIRMED` |

Note: `daiin` analysis is now formalized as **P2-CLAIM-022** in `docs/CLAIM_REGISTRY.md` (assigned 2026-03-19). It supports the R4 (Content) role characterization as domain-modulated. See `docs/CONSISTENCY_AUDIT_POST_ANNEX.md` item C-005.

---

## Notes

1. **Section-level vs. token-level robustness**: Section-level claims (P2-CLAIM-003, 007, 009) aggregate across many tokens and are more robust to transcription variation than token-level claims (P2-CLAIM-004 for `shedy`, but `shedy` as an R2 token type is directly comparable across Eva-T and Eva-). All B.7 claims are `DIRECT`-testable.

2. **P2-CLAIM-004 is TOKEN-LEVEL despite appearing in a section-level table**: The `shedy` elevation claim is about a specific token identity (`shedy` as the B-specific R2 marker), not about aggregate section profiles. Placed here because it characterizes domain structure, but its level is TOKEN-LEVEL.

3. **B-section structural primacy**: Three independent metrics converge on B-section as the most structurally active: (a) highest R1+R2 density (Table B.7a P2-CLAIM-004), (b) highest packet density 2.26× (P2-CLAIM-007), and (c) highest INIT-bleed rate 17.9% (P2-CLAIM-009). This convergence is evidence for genuine B-section structural distinctiveness.
