# ROSETTA3c — qotaiin Positional + Consistent FSA Baseline Results
**Date**: 2026-03-19
**Script**: `scripts/ROSETTA3c_qotaiin_positional.py`
**Results**: `results/ROSETTA3c_qotaiin_positional_results.json`

---

## Packet Count Validation

ROSETTA3c reconstructed **896 packets total** using the ROSETTA2-consistent role_map method (vs ROSETTA2's reported 897 — rounding/edge difference of 1). B-section: **374 packets** — matches ROSETTA2 exactly.

This confirms the consistent FSA method. All prior ROSETTA4 results (281 or 439 packets) were wrong due to incomplete hardcoded R1/R2 token sets. Only ROSETTA2-consistent results are used below.

---

## Finding 1: qotaiin — CENTRAL (NULL positional result)

| Metric | Value |
|--------|-------|
| n in Stars payload | 16 |
| Mean position | 0.543 |
| t-test vs 0.5 | t=0.890, p=0.388 |
| Bias | **CENTRAL — not significant** |

qotaiin does not occupy a consistent structural slot in Stars-section packet payloads. It appears at positions ranging from 0.20 to 0.91, with no statistically detectable bias toward EARLY or LATE.

**Cross-section** (within packets): S=CENTRAL (0.543, p=0.39); B=LATE tendency (0.584, p=0.50, n=7, not sig); C=EARLY tendency (0.360, p=0.13, n=4, too few).

**Implication for qotaiin / qatr hypothesis**:
- Positional evidence: NULL (no structural slot)
- Consonant evidence: Tier 2-3 (7/200 selective, qt→qatr ordered)
- The null positional result means there is no structural anchor for the semantic claim
- **Updated status**: Tier 3 — consonant selectivity is the only supporting signal; positional structure absent

**Disconfirmation check**: if qotaiin had been EARLY-biased (like qokain), that would strengthen the "topic entity" reading. CENTRAL result means qotaiin behaves like a generic content token with no slot preference — consistent with it being a high-frequency folio-anchor type that appears throughout payload structures.

---

## Finding 2: lkaiin — CENTRAL (NULL positional result)

| Metric | Value |
|--------|-------|
| n in Stars payload | 15 |
| Mean position | 0.506 |
| t-test vs 0.5 | t=0.073, p=0.943 |
| Bias | **CENTRAL — not significant** |

lkaiin is positionally neutral in Stars-section packets. No early-entity or late-entity slot detected.

**Implication for lkaiin / lk ambiguity**:
- Neither al-kaff (Arabic astro) nor lacus (Latin water) is supported by positional structure
- lkaiin's 80% Stars concentration + neutral position means it is likely a general Stars-section content token without a specific structural role
- **Status remains Tier 2** — consonant ambiguity unresolved; positional evidence adds no discriminating signal

---

## Finding 3: sal terminal-entity claim — FALSIFIED by consistent methodology ★

| Metric | Consistent ROSETTA3c | ROSETTA2 (prior) |
|--------|---------------------|-----------------|
| B-section packets | 374 | 374 |
| sal in any B payload | **10** occurrences | 17 |
| sal immediately pre-R2 | **2** | 4 |
| sal pre-R2 rate | **0.200 (20%)** | 0.235 (24%) |
| Baseline mean pre-R2 | **0.169** | — |
| sal vs baseline mean | **1.19×** | — |
| Above baseline p90 | **NO** | — |

The 24% figure from ROSETTA2 was based on 17 sal payload occurrences. The consistent ROSETTA3c method finds only 10 sal payload occurrences (2 of which are pre-R2). The discrepancy arises because ROSETTA2 counted sal occurrences across ALL packet contexts (including R2-proximate positions outside the strict payload definition), while ROSETTA3c counts only tokens inside the strict R1→payload→R2 boundary.

**sal's pre-R2 rate (0.200) is only 1.19× above the baseline mean (0.169) and is BELOW the baseline p90 (0.286).** This is not statistically distinguishable from random content token behavior in B-section payloads.

For comparison, the top pre-R2 tokens in B-section packets are:

| Token | Pre-R2 rate | Type |
|-------|------------|------|
| olchey | 43% | content |
| oty | 40% | content |
| kai!n | 38% | content/-ain |
| qokol | 33% | INIT-family |
| qokain | 31% | INIT-family |
| shckhy | 31% | content |
| sheol | 29% | content |
| … | … | … |
| sal | **20%** | content |

Multiple ordinary content tokens exceed sal's pre-R2 rate. The terminal slot is not an entity-label slot — it is simply the last content token that happens to precede R2, with no entity-specific meaning.

**Verdict: The sal terminal-entity positional claim is FALSIFIED.** This is a clean negative result from consistent methodology. The claim should be removed from Paper 2 §7.3.

**What survives**: The Tier 1 Latin consonant alignment (sl → sal/salus) stands independently. sal is still the strongest entity-label candidate in the corpus — but the evidence is the consonant-section-semantic triple, not positional privilege.

---

## Finding 4: Calibration — Stars packet positional hierarchy (updated)

| Token | n | Mean pos | p | Status |
|-------|---|---------|---|--------|
| qokain | 7 | **0.248** | 0.007* | EARLY — confirmed |
| laiin | 5 | **0.875** | 0.007* | LATE — confirmed |
| aiin | 76 | 0.560 | 0.103 | CENTRAL |
| daiin | 47 | 0.459 | 0.379 | CENTRAL |
| okaiin | 47 | 0.497 | 0.941 | CENTRAL |
| lkaiin | 15 | 0.506 | 0.943 | CENTRAL |
| qotaiin | 16 | 0.543 | 0.388 | CENTRAL |

Only qokain (EARLY) and laiin (LATE) have statistically significant positional bias in Stars packets. All others are central. The -ain family has a two-tier structure:
- **Positionally differentiated**: qokain (EARLY), laiin (LATE) — structurally anchored
- **Positionally neutral**: all others — general content tokens

---

## Finding 5: Top-10 Balneological payload tokens — all CENTRAL

No significant positional bias was found in any of the top 20 Balneological payload tokens. The B-section packet structure does not appear to positionally segregate tokens in the way the Stars section segregates qokain and laiin.

This is consistent with the B section's higher packet density and procedural complexity — payloads are longer and more variable, making positional slots less rigid.

---

## Updated Status of Prior Claims

| Claim | Prior status | ROSETTA3c verdict |
|-------|-------------|------------------|
| sal terminal-entity position (24%) | CANDIDATE | **FALSIFIED** — 1.19× baseline, below p90 |
| qotaiin has EARLY bias in Stars | Not tested | **NULL** — CENTRAL (p=0.388) |
| lkaiin EARLY in Stars | Not tested | **NULL** — CENTRAL (p=0.943) |
| qokain EARLY in Stars | CONFIRMED | **RE-CONFIRMED** (p=0.007) |
| laiin LATE in Stars | CONFIRMED | **RE-CONFIRMED** (p=0.007) |
| B-section top tokens positionally neutral | Assumed | **CONFIRMED** — no significant bias |

---

## Next Steps (ROSETTA3d)

1. **Paper 2 correction**: Remove the sal terminal-entity positional claim from §7.3. Replace with: "sal appears in B-section packet payloads at 1.44× enrichment; its pre-R2 rate (0.200) is not distinguishable from baseline (mean 0.169, p90 = 0.286)."
2. **qotaiin Tier demotion**: qotaiin → Tier 3 explicitly. The consonant selectivity argument (7/200) remains the only supporting signal. Document that selectivity alone at 2-con threshold is insufficient for Tier 2.
3. **Symmetric expansion**: Add Ulugh Beg Zij + Syriac medical vocabulary to lexicon for ROSETTA3d.
4. **ai!n Stolfi replication**: Cross-transcription confirmation of the LATE bias — the only remaining unresolved positional finding.
