# ROSETTA3b — Expanded -ain Stem Alignment Log
**Date**: 2026-03-19
**Scripts**: `scripts/ROSETTA3b_expanded_alignment.py`, `scripts/ROSETTA4_sal_terminal_baseline.py`
**Results**: `results/ROSETTA3b_expanded_results.json`, `results/ROSETTA4_sal_terminal_results.json`

---

## Governing Anti-Overfitting Rule

> **No candidate will be treated as meaningful unless it outperforms both baseline chance and the best competing non-target-language reading.**

This rule governs every claim below.

---

## Lexicon and Baseline

**Lexicons used:**
- al-Sufi Arabic star catalog: 91 entries (expanded from 35 in ROSETTA3)
- Latin balneological/medical: 64 entries (expanded from 22)
- Arabic/Hebrew linguistic: 45 entries
- **Total: 200 entries**

**Per-stem-length baseline (10,000 random samples):**

| Stem length | Match rate (≥ 2 shared consonants) |
|-------------|-------------------------------------|
| 1 consonant | **0.0%** — cannot meet 2-con threshold |
| 2 consonants | **59.3%** |
| 3 consonants | **87.1%** |

**Critical implication**: Even at the 2-consonant threshold, a random 2-con stem matches the combined lexicon 59% of the time. Any token with a 2-con stem will likely generate "matches." Matches alone are not evidence — **only** cases with (a) exact ordered alignment, (b) independently plausible semantics, and (c) no comparably strong competing reading across multiple source traditions are interpretable.

---

## Candidate Tier Ladder

| Tier | Criteria |
|------|---------|
| **Tier 1** | 2+ cons in order, strong semantic fit, good positional fit, no stronger competing reading |
| **Tier 2** | 2+ cons in order, partial semantic fit, competing readings cannot be excluded |
| **Tier 3** | Plausible but weak; exploratory only |
| **Reject** | Single consonant, forced semantics, or function-word behavioral override |

---

## Token-by-Token Assessment

### sal (stem: sl) — Section B, 2.08× enriched

| Column | Arabic best | Latin best | Other |
|--------|------------|-----------|-------|
| Term | al-shaulah (sting, Sco) | sal (salt) / salus (health) | Arabic: salama (safety) |
| Consonants | lshl (ordered ✓) | sl (exact ✓) | slm (ordered ✓) |
| Shared | 2 | **2 exact** | 2 |
| Semantic fit | POOR — astronomical, wrong section | **STRONG** — Balneological section, mineral/health | moderate |
| Positional fit | — | ROSETTA2: 24% terminal; ROSETTA4: 1/3 (33%), inconclusive | — |

**Section context**: `sal` appears 2.08× in Balneological. Arabic astronomical terms (al-shaulah, suhayl, etc.) match consonants but are semantically inconsistent with section B. Latin *sal* and *salus* match exactly and are semantically coherent with a thermal bath / health text.

**Positional evidence (ROSETTA4 findings)**: With paragraph-based packet reconstruction, only 3 sal-containing packets found (vs. 17 in ROSETTA2). Methodological discrepancy — the two scripts use different R1/R2 token sets. The ROSETTA4 baseline shows sal's pre-R2 rate is 33.3% (rank: top 17.9%), which is above median but below the p90 baseline. **The terminal-entity pattern is NOT confirmed as exceptional by ROSETTA4.** ROSETTA2's 24% figure must be re-evaluated with a consistent methodology.

**Disconfirmation pressure**:
- If sal appears frequently at EARLY or MIDDLE positions at the same rate as LATE → terminal pattern is chance
- If multiple tokens in B have equally high pre-R2 rates → terminal position is not entity-specific (ROSETTA4 suggests this: sol=62.5%, qokol=50%, ai!n=66.7% all exceed sal's rate)
- The pre-R2 "slot" in B packets may be structurally occupied by ol/sol/qol-type structural tokens, not lexical entities

**Verdict: Tier 1 for Latin alignment (sal/salus)**. The consonant-section-semantic triple match (sl exact, Balneological section, salt/health meaning) survives the competing-reading test: no Arabic astronomical term is semantically appropriate for Balneological context. The terminal-entity positional claim is **downgraded to Tier 3** pending consistent re-analysis.

---

### qotaiin (stem: qt) — Section S (Stars, 52.7%), folio-anchor n=39

| Column | Arabic best | Latin best | Other |
|--------|------------|-----------|-------|
| Term | qatr (drop of water) | (none with exact qt) | qata (to cut) |
| Consonants | qtr (qt ordered ✓) | — | qt (exact ✓) |
| Shared | 2 | — | 2 |
| Semantic fit | **PLAUSIBLE** — astronomical water notation, al-Sufi's nebula descriptions | — | POOR |
| Selectivity | **7 total matches** (lowest in priority set) | — | — |

**Selectivity note**: The qt pattern has only 7 matches in the expanded 200-entry lexicon. This is the most selective stem tested — far below the 59.3% 2-con baseline rate. This means the qt pattern is RARE in the reference lexicons, which makes each individual match relatively more meaningful.

**Arabic `qatr` (drop)**: In classical Arabic, *qatr* (drop of water; also: distillate, drip) appears in astronomical contexts in al-Sufi when describing nebular features. `qotaiin` is a Stars-section folio-anchor token — it changes by folio and may label specific celestial features. A "drop-feature" reading is plausible for certain al-Sufi star clusters described as "drops" or "scattered water."

**qotaiin section distribution**: S=52.7%, B=17.6%, H=13.5%. Primarily Stars. Arabic astronomical terms are semantically appropriate for Stars section.

**Competing readings**: `qata` (to cut, Arabic) = 2-con exact but semantically poor. `laqit` (foundling star, Arabic) = 2 shared, folio-anchor stars plausibly include obscure/unnamed objects ("foundlings"). Neither is as clean as `qatr`.

**Disconfirmation pressure**:
- If qt appears broadly in non-water, non-astronomical contexts → weakens qatr alignment
- If qotaiin position within Stars packets is not distinctively EARLY or LATE → no structural slot confirmation
- If qotaiin appears at equal rates in Herbal/Balneo → undermines Stars-specific reading (but it doesn't: 52.7% Stars)

**Verdict: Tier 2-3.** The selectivity (7 matches) is encouraging. Arabic `qatr` is semantically plausible for a Stars folio-anchor. But the 59.3% baseline still applies, and competing Arabic readings cannot be excluded. Requires positional analysis within Stars packets.

---

### lkaiin (stem: lk) — Section S (Stars, 80.4%)

| Column | Arabic astronomical | Latin water/bath | Hebrew |
|--------|---------------------|-----------------|--------|
| Term | al-kaff (the palm, Cas) | lacus (lake/pool) | melekh (king) |
| Consonants | lkf (lk ordered ✓) | lk (exact ✓) | mlk (ordered ✓) |
| Shared | 2 | 2 | 2 |
| Semantic fit | moderate (Stars section, palm/Cassiopeia area) | POOR (balneological, but lkaiin is 80% Stars) | POOR |
| Section match | yes (Stars 80%) | no (Balneo is wrong section) | no |

**Note on competing readings**: `lacus` (Latin, lake/pool) matches exactly (lk=lk) but is balneological while `lkaiin` is an 80% Stars-section token. `al-kaff` ("the palm" = a star in Cassiopeia area) is astronomically appropriate but the match is partial (lk matches first 2 of lkf). Also: `al-dalik` (ldlk) and `al-iklil` (lkl) both match lk.

**Multiple Arabic stars match lk**: al-kaff, al-iklil, al-dalik, sad al-akhbiya, al-simak al-ramih. This multiplicity weakens any single candidate.

**Hebrew readings**: `melekh` (king), `halakh` (walked), `malak` (angel) all share lk consonants but are semantically inappropriate for astronomical notation. Reject on semantic grounds.

**Disconfirmation pressure**:
- If lkaiin appears in Balneological at expected rates → undermines astronomical reading
- If lkaiin has no stable positional slot in Stars packets → no structural anchor
- The multiplicity of Arabic lk-containing star names (5+ matches) means no single name is preferred

**Verdict: Tier 2.** lk is a common consonant pair in both Arabic astronomical and Latin water vocabulary. The Stars-section concentration (80%) rules out Latin bath terms. Among Arabic astronomical terms, al-kaff is semantically best (palm/hand constellation). But with 24 total lexicon matches and 59.3% baseline, this remains exploratory.

---

### qol (stem: ql) — Section B, inner-function word OR=7.83

| Column | Arabic best | Note |
|--------|------------|------|
| Term | qalb (heart/Antares) | qalb al-aqrab (Antares), qalb al-asad (Regulus) |
| Consonants | qlb (ql ordered ✓) | 2 shared, exact ordered |
| Semantic fit | — | astronomical; but qol is B inner-function word |

**Critical override**: `qol` is an inner-function word (classified by behavioral profile: OR=7.83 B first-payload, high frequency, pan-folio distribution). Its behavior mirrors Hebrew *kol* (all/every) — a grammatical quantifier. Lexical alignment is inappropriate for tokens with demonstrated grammatical function. The qalb match is consonantally interesting but cannot override behavioral classification.

**Verdict: Rejected for lexical alignment.** qol's function-word behavior is primary evidence. Any lexical reading is subordinate to behavioral classification and currently unsupported.

---

### qokain (stem: qk) — Section S, EARLY-biased (0.248, p=0.007)

At the 2-con threshold, the only match in 200 entries is `aqua calida` (qkld, Latin "hot water") — semantically irrelevant for a Stars-section token. Zero Arabic astronomical or Hebrew terms match qk with 2 consonants.

**The null result stands and is meaningful**: The absence of qk from the Arabic/Hebrew root inventory reflects the real morphological structure — `qok-` is the INIT grammatical particle, not a content stem. The `-ain` suffix is the entity component. Any future lexical alignment should target the `-ain` suffix meaning directly (ʿayn = eye/spring/source), not the qk consonant pair.

**Verdict: NULL confirmed. qok- = grammatical INIT morpheme, not lexically alignable.**

---

### Tokens excluded (single consonant, below threshold)

| Token | Stem | Reason |
|-------|------|--------|
| laiin | l | 1-con — not testable |
| daiin | d | 1-con — not testable |
| okaiin | k | 1-con — not testable |
| raiin | r | 1-con — not testable |
| saiin | s | 1-con — not testable |
| ai!n | ∅ | no stem — the bare ʿayn morpheme |
| aiin | ∅ | no stem |

For these tokens, the `-ain` suffix itself is the candidate morpheme (Arabic ʿayn = eye/spring/entity marker). But bare ʿayn matches everything — it cannot discriminate.

---

## ayn-Compound Search Results

Arabic compound star names with ʿayn (ayn al-X = "eye of X"):
- ayn al-thawr (eye of the bull = Hyades area near Aldebaran)
- ayn al-asad (eye of the lion = epsilon Leonis)
- ayn al-aqrab (eye of the scorpion = pi Scorpii)
- ayn al-sagittarius (eye of Sagittarius)
- ain al-shams (eye of the sun = Heliopolis)
- ain al-maa (eye/spring of water)

**Critical result**: No -ain family stem (qk, lk, qt, ql, d, k, r, s, l) generates a 2-con match against any ʿayn-compound at the 2-con threshold. The ʿayn compounds all have consonant pattern nl-X (Arabic al- = l, plus ayn = n in our notation). Single-consonant stems cannot match the compound's full consonant skeleton.

**Interpretation**: The ʿayn connection in the -ain suffix is plausible as a morphological hypothesis (the suffix *class* = ʿayn), but no specific ayn-compound can be linked to any specific -ain token with current evidence. This is not a falsification — it reflects the methodological limitation of short stems.

---

## ROSETTA4 — sal Terminal Baseline Results (Preliminary)

**Packet reconstruction**: 439 B-section packets (paragraph-based grouping); 3 sal-containing packets found (vs 17 in ROSETTA2). **Discrepancy indicates different R1/R2 token set coverage between scripts** — results are not directly comparable.

**Key finding from ROSETTA4 baseline**: The tokens with the highest pre-R2 rates in B packets are:

| Token | Pre-R2 rate | Count |
|-------|------------|-------|
| ai!n | 66.7% | 2/3 |
| okol | 66.7% | 2/3 |
| sol | 62.5% | 10/16 |
| qokol | 50.0% | 6/12 |
| ol | 33.3% | 25/75 |
| sal | 33.3% | 1/3 |

**The terminal slot is dominated by ol/sol-type structural tokens, not lexical entities.** The immediately-pre-R2 position appears to be a structural/function-word slot (consistent with R6-type tokens). If sal appears there, it may be because it behaves like ol/sol morphologically (sl-stem tokens cluster together).

**ROSETTA4 verdict**: Methodologically inconclusive due to packet reconstruction discrepancy. The sal terminal-entity pattern requires re-testing with ROSETTA2-consistent packet methodology. The baseline result suggests the terminal slot is structural, not lexical — this is a pressure point against the terminal-entity hypothesis.

**What this implies for sal**: The Tier 1 Latin consonant alignment (sl → sal/salus) stands independently of positional claims. The terminal-entity positional claim is on weaker ground than previously stated.

---

## Summary Table (with competing readings and disconfirmation)

| Token | Stem | Arabic candidate | Latin candidate | Best reading | Tier | Disconfirmation |
|-------|------|-----------------|----------------|--------------|------|----------------|
| sal | sl | al-shaulah (POOR — wrong section) | **sal / salus** (STRONG) | Latin *sal/salus* | **Tier 1** | terminal pattern not confirmed by ROSETTA4 baseline |
| qotaiin | qt | **qatr** (drop of water; selective) | none | Arabic *qatr* | **Tier 2-3** | need positional analysis in Stars packets |
| lkaiin | lk | al-kaff (palm/Cassiopeia) | lacus (wrong section) | al-kaff (weakly) | **Tier 2** | 5+ lk-containing Arabic stars; no single preferred |
| qol | ql | qalb/Antares (consonant match) | — | **Rejected** | Reject | behavioral classification overrides lexical alignment |
| qokain | qk | NULL | aqua calida (irrelevant) | **NULL** | Null | confirms qok- = grammatical INIT particle |
| laiin–raiin | l,d,k,r,s | not testable | not testable | not testable | Excluded | 1-con below threshold |
| ai!n, aiin | ∅ | ʿayn (suffix class hypothesis) | — | ʿayn suffix | Morphological | positional LATE bias is supporting, not primary evidence |

---

## Updated Priority for ROSETTA3c

1. **qotaiin / qt**: Run positional analysis within Stars-section packets. Does qotaiin occupy a consistent structural slot? If EARLY: topic entity. If folio-variant: may label specific celestial features. The selectivity (7 matches) justifies deeper investigation.

2. **sal terminal pattern**: Rebuild with ROSETTA2-consistent R1/R2 token set. Test whether the terminal slot is dominated by structural tokens (ol/sol family) or accessible to lexical entities. Compute baseline for any-token appearing pre-R2.

3. **lkaiin / lk**: Compute positional behavior in Stars-section packets. Check whether lkaiin occupies EARLY positions (topic entity) or is positionally neutral. Cross-check with folios containing al-Sufi palm/Cassiopeia star descriptions.

4. **Symmetric lexicon expansion**: Greek astronomical terms (Ptolemy via Arabic), Persian star names (Ulugh Beg *Zij*). Currently the lexicon is skewed toward Arabic and Latin — adding a non-favored comparison set (e.g. Aramaic, Syriac astronomical vocabulary) would strengthen the comparative framework.

5. **ʿayn-compound 3-consonant test**: Build ayn-compound list where the full compound (ayn al-X) has 3+ consonants beyond the al-ayn prefix. Test all -ain stems against the X-component only (the star/body part name). This gives more discriminating tests.

---

## Methodological Lessons (applied from feedback)

- **Positional evidence is supporting, not primary**: Late bias for ai!n is interesting, not confirmatory.
- **Lexical alignment must outperform competing non-target readings**: sal satisfies this for Latin; qotaiin does not yet for Arabic.
- **Tier system enforces discipline**: Only sal reaches Tier 1 with current evidence.
- **Clean negatives are productive**: qokain null, qol behavioral override, ayn-compound failure are all informative, not failures.
- **Baseline is still high at 2-con**: The 59.3% 2-con baseline means even exact matches require semantic + section + positional corroboration before advancing to Tier 1.
