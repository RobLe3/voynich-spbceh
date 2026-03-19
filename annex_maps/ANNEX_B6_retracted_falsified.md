# Annex B.6 — Retracted and Falsified Claims
**Table**: Complete record of all retracted and falsified claims in the SPBCEH research program.
**Source**: `docs/RETRACTED_AND_FALSIFIED_CLAIMS.md` (authoritative record with full wording)
**Policy**: Claims are retained, not deleted. The record is scientifically useful and reviewer-accessible.

---

## B.6a — Full retraction and falsification table

| ID | Claim ID | Type | Level | Original Claim (brief) | Falsifying Test | Root Cause | Replacement Interpretation | Paper Correction Applied |
|----|----------|------|-------|----------------------|----------------|-----------|---------------------------|--------------------------|
| RETRACTED-001 | P2-CLAIM-015 | `RETRACTED` | TOKEN-LEVEL | `sal` appears pre-R2 in 24% of B-section packets (n=4/17) — terminal-entity positional pattern | ROSETTA3c (n=374 B packets): sal pre-R2 rate = 0.200 (2/10); baseline mean = 0.169, p90 = 0.286. Rate is 1.19× mean — below p90, not exceptional. Pre-R2 slot dominated by structural tokens (sol: 62.5%, qokol: 50%). | ROSETTA2 used a manually hardcoded R1/R2 token set (incomplete); no pre-R2 baseline computed; 4/17 figure compared to intuition only. | `sal` Tier 1 status (P2-CLAIM-014) stands based on consonant-section-semantic triple (`sl`=`sl`, Latin *sal/salus*, Balneological section). No positional slot. | Applied in Paper 2 v0.94 (§7.3, §9, §10) |
| RETRACTED-002 | (informal; PILOT2) | `RETRACTED` | FAMILY-LEVEL | Stars `-ain` tokens show strong entity-labeling behavior: recto/verso consistent type suggests stable folio-level referents | PILOT2: Only 2/7 folios show recto/verso consistency in dominant `-ain` type — below the expectation for a stable entity-label hypothesis | Motivated by intuitive entity-label framing; not tested against a baseline consistency rate | Descriptive folio-anchor pattern confirmed (dominant `-ain` type varies per folio). Strong entity-labeling hypothesis retracted. Positional differentiation (P2-CLAIM-010, 011) and consonant alignment remain valid. | Not a formal paper claim; pilot-level retraction |
| RETRACTED-003 | (informal; Paper 2 §9 IA.5) | `FALSIFIED` | METHOD-LEVEL | Semantic sub-labels (ACT:PULSE, MODE:CELESTIAL, CLOSE:TERMINAL) are empirically supported by folio-level illustration-type distributions | 3/4 sub-label folio-type predictions fail: `shol` (MODE:CELESTIAL) shows zero rate in astronomical folios; `daiin` (ACT:PULSE) is 3.4× more frequent in botanical than balneological (Mann-Whitney p < 0.0001); `ykchdy` (CLOSE:TERMINAL) too rare to test. Only `shedy` correctly predicts elevated balneological. | Sub-labels were applied before systematic folio-type validation. Structural role assignments were confused with semantic sub-assignments. | Structural role assignments (R1–R6) are validated. Semantic sub-labels removed from Paper 2 taxonomy. `shedy` correctly predicts B-section (P2-CLAIM-004). | Applied in Paper 2 v0.93–v0.94 |
| RETRACTED-004 | (informal; ROSETTA3 preliminary) | `RETRACTED` | TOKEN-LEVEL | `lkaiin` → Latin *lacus* (lake/pool) as primary reading (ROSETTA3 log; exact 2-con match `lk`=`lk`) | Section mismatch: `lkaiin` is 80.4% Stars-section; *lacus* is a Balneological/water-basin term. Additionally: 24 Arabic astronomical terms also match `lk` at 2-con level (al-kaff, al-iklil, al-dalik, al-simak compounds). No single candidate preferred. | Preliminary alignment did not apply the section-coherence test. `lk` has many competing readings in astronomy-relevant Arabic lexicon. | `lkaiin` remains Tier 2: `lk` is ambiguous between Arabic astronomical `al-kaff` (Stars-consistent) and Latin *lacus* (wrong section). Positional evidence null (CENTRAL, p=0.943, P2-CLAIM-021). Unresolved. | Not a formal paper claim; ROSETTA3 log retraction |
| FALSIFIED-001 | P2-CLAIM-008 | `FALSIFIED` | METHOD-LEVEL | B-section packets with INIT-classified first-payload tokens may be nested sub-packets (recursive packet structure) | PILOT4 direct test: 0/67 B-section packets whose first-payload token is INIT-classified contain an internal CLOSE token before the outer R2. Sub-CLOSE = 0/67. | Elevated INIT-bleed rate in B (17.9%) suggested nesting; no direct test had been run. | Grammar is finite-state. INIT-bleed is explained by dual-function `qok-` tokens in procedurally dense text — they can appear in CONTENT positions within B-section payloads without initiating sub-packets. | Applied in Paper 2 v0.94 (§4.3) |
| FALSIFIED-002 | P2-CLAIM-017 | `FALSIFIED` | METHOD-LEVEL | `-ain` folio-uniqueness (67.6%) is entity-label evidence: unique per-folio appearance suggests stable folio referents | PILOT5 control: non-`-ain` rare tokens of matching frequency range show 74.8% folio-uniqueness — **higher** than `-ain` baseline (67.6%). Folio-uniqueness is a property of rare tokens in general. | No control comparison against matching-frequency non-`-ain` tokens had been performed. 67.6% was compared against 50% intuitively, not against the empirical baseline. | Folio-uniqueness retracted as entity-label evidence. Remaining `-ain` evidence is: (a) positional differentiation (P2-CLAIM-010, 011) and (b) consonant alignment to Arabic ʿayn suffix. Image-level folio mapping remains the required test. | Applied in Paper 2 v0.94 (§4.3) |

---

## B.6b — Retraction summary by paper and type

| Paper | Retracted | Falsified | Total |
|-------|-----------|-----------|-------|
| Paper 1 | 0 | 0 | 0 |
| Paper 2 (formal claim IDs) | 1 (P2-CLAIM-015) | 2 (P2-CLAIM-008, P2-CLAIM-017) | 3 |
| Pilot/informal (no formal claim ID) | 3 (RETRACTED-002, 003, 004) | 0 | 3 |
| **Total** | **4** | **2** | **6** |

Note: RETRACTED-003 is flagged as `FALSIFIED` in the retraction log (3/4 predictions failed under active test). The count above treats it as a retraction. For audit purposes, the effective falsification count (active test result) is 3 (FALSIFIED-001, 002, 003).

---

## Notes

1. **Completeness**: The full retraction record is in `docs/RETRACTED_AND_FALSIFIED_CLAIMS.md`. This table provides a structured cross-reference; the authoritative source has full original wording, why it was plausible, the exact falsifying evidence, and reproduction paths.

2. **Numbering consistency issue**: The retraction log uses `RETRACTED-NNN` and `FALSIFIED-NNN` prefixes. Paper 1's appendix refers to "four documented retractions (RETRACTED-001 through RETRACTED-004) and three falsifications (FALSIFIED-001 through FALSIFIED-003)." Paper 2's appendix lists only two retracted formal claims. The inconsistency arises because RETRACTED-002, 003, 004 are pilot-level retractions without formal Paper 2 claim IDs. The full count (4 retractions + 3 falsifications when RETRACTED-003 is counted as FALSIFIED) is consistent with Paper 1's statement. See `docs/CONSISTENCY_AUDIT_POST_ANNEX.md` item C-003.

3. **Replacement interpretation availability**: Every retracted/falsified claim has a replacement interpretation or explicit statement that no replacement exists. No retracted claim was simply deleted — all are preserved here and in the full retraction log.
