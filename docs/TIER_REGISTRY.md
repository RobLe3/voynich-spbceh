# Tier Registry — Lexical Candidate Tiers
**Last updated**: 2026-03-19
**Purpose**: Formal documentation of Tier 1 / Tier 2 / Tier 3 assignments for lexical alignment candidates. Tier assignments govern how strongly a consonant-stem alignment is presented in the papers and what further work is required before upgrading.

---

## Tier Criteria

| Tier | Criteria | Presentation in Papers | Upgrade Path |
|------|----------|----------------------|--------------|
| **Tier 1** | (1) Ordered 2-consonant match to external vocabulary; (2) Section coherence — token enriched in the expected manuscript section; (3) No competing plausible reading eliminates the candidate | Stated as primary lexical alignment candidate with full consonant-section-semantic triple | Confirmed by stronger scoring (e.g., 3-consonant match, phonological model) |
| **Tier 2** | (1) Ordered 2-consonant match; (2) Partial section coherence OR competing reading not fully eliminated; (3) Positional evidence does not resolve ambiguity | Presented as probable candidate with explicit ambiguity note | Requires: competing-reading elimination test, or additional section coherence evidence |
| **Tier 3** | (1) Ordered 2-consonant match only; (2) No section coherence or positional evidence; (3) Multiple competing candidates remain | Mentioned only in future-work context | Requires: section enrichment test, positional evidence, or competing-reading elimination |

---

## Current Tier Assignments

### Tier 1 — Primary Lexical Candidates

| Token | Stem | Best Reading | Source Lexicon | Match Type | Section Coherence | Competing Readings | Claim ID | Status |
|-------|------|-------------|---------------|-----------|-------------------|-------------------|---------|--------|
| `sal` | sl | Latin *sal* (salt) / *salus* (health/welfare) | Latin balneological | 2-con ordered exact | B-section enrichment 2.08× (P2-CLAIM-013) | Arabic sl-stems (al-shaulah, suhayl, etc.) are astronomical — wrong section ✓ | P2-CLAIM-014 | `CONFIRMED` |

**Basis for Tier 1**: consonant-section-semantic triple confirmed. Competing Arabic sl-stem candidates are Stars-section terms; `sal` is Balneological-enriched — the section mismatch eliminates Arabic astronomical readings as primary candidates. The terminal-position claim was retracted (RETRACTED-001/P2-CLAIM-015) but does not affect the Tier 1 consonant-section alignment.

---

### Tier 2 — Probable Candidates

| Token | Stem | Competing Readings | Section | Positional | Ambiguity | Status |
|-------|------|-------------------|---------|-----------|-----------|--------|
| `lkaiin` | lk | (a) Arabic *al-kaff* (the palm/star); (b) Latin *lacus* (lake/pool) | 80.4% Stars-section → consistent with al-kaff (astro); inconsistent with *lacus* (B-specific) | CENTRAL p=0.943 (P2-CLAIM-021) — positional null, does not resolve | Section evidence favors al-kaff direction but does not eliminate competing readings at 2-con threshold | `PROVISIONAL` |

**Basis for Tier 2**: The Stars-section association points toward an astronomical candidate (al-kaff is a star-name; al-iklil, al-simak, and others also share lk). The Latin *lacus* reading is section-mismatched (B-specific term in Stars context). However, the Arabic candidates are numerous (24 matches in the expanded lexicon) and no single Arabic term is clearly preferred. Positional evidence is null. **Verdict**: section evidence narrows the direction to astronomical but competing Arabic readings prevent a single Tier 1 designation.

**Upgrade requirement**: A 3-consonant match or a frequency-ordered disambiguation within the Stars-section Arabic astronomical vocabulary.

---

### Tier 3 — Candidates Pending Evidence

| Token | Stem | Best Match | Source | Evidence Status | Claim ID |
|-------|------|-----------|--------|----------------|---------|
| `qotaiin` | qt | Multiple: Arabic *al-qaus* (the bow/Sagittarius), *al-qitr* (diameter), Latin *quattuor* (four) | Arabic astro / Latin | Consonant match only; positional null CENTRAL p=0.388 (P2-CLAIM-020); no section enrichment test run | P2-CLAIM-020 |

**Basis for Tier 3**: `qotaiin` shows consonant selectivity (qt stem in Stars context) but:
- Multiple plausible candidates at 2-con threshold, no dominant reading
- ROSETTA3c shows CENTRAL positional distribution — no early/late slot
- No section enrichment analysis run (Stars-section rate vs. corpus rate not computed)
- Section noted as Stars-primary (from folio distribution) but not formally tested

**Upgrade requirement**: (1) Section enrichment test (Stars-rate vs. corpus-wide rate); (2) Competing-candidate scoring across full Arabic astronomical lexicon; (3) If section-enriched AND one candidate is clearly preferred → Tier 2. If consonant match is exact at 3-con level → possible Tier 1.

---

## Tier Assignment Process

A lexical candidate moves through tiers via formal tests, not intuition. Each upgrade requires a registered claim and a computed result.

```
Token identified (from role_map or frequency list)
  ↓
2-con match found → register as Tier 3 candidate
  ↓
Section enrichment test run:
  - Enriched in predicted section? → progress toward Tier 2
  - Not enriched or wrong section? → demote or explain
  ↓
Competing reading test run:
  - Competitors eliminated by section mismatch? → progress toward Tier 1
  - Multiple competitors remain? → stay at Tier 2 with explicit ambiguity note
  ↓
Positional test (optional upgrade evidence):
  - Expected positional slot (EARLY/LATE)? → strengthens Tier 1
  - CENTRAL? → neutral; does not block or require tier change
  ↓
Assign Tier 1 if: 2-con match + section coherent + competitors eliminated
```

---

## Notes

1. **Tier is about alignment confidence, not structural importance**: `qok-` is R1 (INIT) and is structurally critical, but carries no lexical tier assignment (its null lexical alignment is confirmed — P2-CLAIM-016).

2. **Tier does not equal claim status**: A Tier 1 candidate may have an underlying claim that is still `CONFIRMED`. A Tier 3 candidate may have `PROVISIONAL` or no formal claim yet.

3. **All 44 Rosetta candidates (P2-CLAIM-019) have not been individually tiered**: Tier assignments require the competing-reading test; the 44-candidate list is a distributional enrichment result, not a lexical alignment result.

4. **R6 Hebrew preposition alignment (P2-CLAIM-018)** is a family-level finding, not a token-level tier. The R6 tokens (`ol`, `al`, `or`, `ar`) as a group align at 52.6% with Hebrew prepositions; individual tokens have not been individually tiered.
