# R6 Hebrew Alignment Method Note
**Date**: 2026-03-19
**Status**: Active methods guidance — supports P2-CLAIM-018 (PROVISIONAL)
**Purpose**: Documents the scoring method, data source, normalization rules, and limitations for the R6 cluster Hebrew preposition alignment claim. Required reading before evaluating or extending P2-CLAIM-018.

---

## 1. Scope of the R6 Alignment Claim

**Claim ID**: P2-CLAIM-018 (Paper 2 §6.1)
**Statement**: R6 (Reference-like) cluster token types align with Hebrew grammatical prepositions and proclitic particles at a rate of approximately 52.6% of R6 token types tested.
**Status**: `PROVISIONAL` — alignment scoring method not yet fully documented; scoring logic requires explicit pre-specification and null-model comparison.
**Claim level**: `FAMILY-LEVEL` (applies to the R6 cluster family, not a single token)
**Transcription comparability**: `NORMALIZATION_REQUIRED`

---

## 2. Data Source

### 2.1 Voynich corpus
- **File**: `data/corpus_tokens.csv` (derived from Takahashi H IVTFF transliteration)
- **Format**: One row per token occurrence; columns include `cluster`, `role`, `section`, `folio_id`, `line_id`, `position_in_line`
- **Total tokens**: 37,045
- **Source transliteration**: Takahashi H (Eva-T alphabet, includes `!` glyph-variant marker)

### 2.2 R6 token pool
R6 (Reference-like) is the sixth role class in the SPBCEH six-role taxonomy. The R6 cluster set is defined by positional and transitional behavior (high frequency in reference/terminal positions within paragraphs), derived from `results/p1_1_cluster_frequencies.csv`.

**R6 token types identified in the corpus (partial list; complete list in `results/p1_1_cluster_frequencies.csv`)**:
- `ol` (n=504 corpus occurrences) — highest frequency R6 token; prominent in B and S sections
- `al` — short form; frequent as sentence-final or paragraph-boundary token
- `or` — less frequent; morphological variant of `ol`
- `ar` — short form; parallel to `al`
- Additional R6 types (exact set defined by role_map entries with `role = R6`)

**Note**: `qol` is NOT included in the R6 alignment pool for this claim. `qol` is classified as an inner-packet function word (Layer 2 of the three-layer model, P2-CLAIM-006), not a structural R6 token, despite its high section-profile correlation with `ol` (r=0.940).

### 2.3 Hebrew preposition and particle inventory
The comparison set consists of Hebrew grammatical words (prepositions, proclitic particles, and short grammatical forms). These are drawn from standard Biblical Hebrew and Mishnaic Hebrew grammar inventories. The pre-specified list used for the P2-CLAIM-018 scoring must be documented before the claim can be upgraded from PROVISIONAL.

**Known pre-specified forms (partial; complete list pending)**:
| Hebrew form | Transliteration | Consonants | Meaning |
|-------------|----------------|-----------|---------|
| ל | le/li | L | "to, for" (proclitic) |
| ב | be/ba | B | "in, with, by" (proclitic) |
| מ / מן | mi/min | M/MN | "from" |
| ו | ve | V/W | "and" (proclitic) |
| ה | ha | H | "the" (definite article; proclitic) |
| כ | ke/ka | K | "like, as" (proclitic) |
| על | al | ʿL | "on, upon" |
| אל | el | ʾL | "to, toward" |
| עם | im/ʿim | ʿM | "with" |
| אם | im | ʾM | "if" |
| כי | ki | KY | "because, for, that" |
| אשר | asher | ʾŠR | "that, which, who" |
| רק | rak | RQ | "only, but" |

---

## 3. Normalization Rules

### 3.1 EVA glyph-to-consonant normalization
The Voynich EVA transcription is a glyph-level transcription, not a phonological one. For the purposes of the R6 alignment claim, the following normalization is applied to extract the consonant skeleton of each R6 token type:

1. **Remove the `!` marker** if present (e.g., `oi!n` → `oin`); the `!` is an Eva-T glyph-variant marker, not a phoneme.
2. **EVA vowel candidates**: `a`, `o`, `e`, `i`, `y` are treated as potential vowel markers and may be excluded from the consonant skeleton for alignment purposes, or retained depending on the alignment model.
3. **EVA consonant candidates**: `q`, `k`, `ch`, `sh`, `d`, `t`, `n`, `l`, `r`, `f`, `m`, `g`, `j`, `p`, `s` are treated as consonant-bearing glyphs.

**Current practice for R6 alignment**: R6 tokens are short (typically 2–4 EVA glyphs). For `ol`, `al`, `or`, `ar`:
- `ol` → consonant `l` (if `o` = vowel marker)
- `al` → consonant `l` (if `a` = vowel marker)
- `or` → consonant `r`
- `ar` → consonant `r`

**Alternative normalization (full glyph sequence)**: Treat the full EVA sequence as the matching unit without vowel stripping. Under this model:
- `ol` → matches Hebrew `אל` (el = "to") or `על` (al = "on") at the `*l` pattern
- `al` → matches `אל` or `על` directly at the `al` pattern
- `or` → matches `אור` (or = "light") at the `or` pattern

**REQUIRED**: The exact normalization rule (vowel-stripping vs. full-glyph) must be pre-specified and held constant before scoring. The 52.6% figure in P2-CLAIM-018 must be tied to one of these two normalization approaches.

### 3.2 Hebrew consonant extraction
For Hebrew forms:
1. Remove vowel points (nikud) if present
2. Retain the consonant skeleton: e.g., `על` → `ʿL` (Ayin-Lamed); `אל` → `ʾL` (Aleph-Lamed)
3. For alignment matching: Ayin (`ʿ`) and Aleph (`ʾ`) are treated as gutturals; they may or may not be treated as distinct from each other depending on the alignment model

---

## 4. Alignment Procedure

### 4.1 Match criteria
A match is recorded when the consonant skeleton of an R6 EVA token type (after normalization in §3.1) is consistent with the consonant pattern of a Hebrew grammatical preposition or particle (after normalization in §3.2).

**Two-consonant minimum match**: At least 2 consonants must be matched in the same order (ordered exact match). This is consistent with the ROSETTA3b standard used for other lexical claims.

**Single-consonant match**: Short tokens (`ol` → `l`, `al` → `l`) may only contribute one consonant. These are weaker matches and should be labeled accordingly.

### 4.2 Scoring
- Count the number of R6 token types (not occurrences) that match at least one item in the pre-specified Hebrew preposition inventory.
- Divide by the total number of R6 token types tested.
- Report as a percentage.

**Current figure**: 52.6% — but the exact R6 type pool size, the matching procedure, and the comparison set are not yet fully documented in the repository. This is the reason for PROVISIONAL status.

---

## 5. Null Model and Baseline Expectation

### 5.1 Required null model
The 52.6% match rate must be compared against a baseline expected rate under random token selection or random consonant pairing.

**Minimum required baseline**:
- Random 2-con match baseline: What fraction of arbitrary 2-character EVA consonant sequences match any item in the Hebrew preposition inventory?
- Using the ROSETTA3b standard: this baseline is approximately 59.3% for the full 200-entry lexicon, but this is for a richer comparison set. For the restricted Hebrew preposition set (13 items in §2.3), the baseline will be lower.

**Required computation** (not yet done):
1. Generate all possible 1–2 consonant combinations from EVA consonant pool
2. Compute the fraction that match any Hebrew preposition consonant form
3. Compare 52.6% against this baseline

**Key question**: Is 52.6% above or below what would be expected if R6 tokens were random short sequences? If the Hebrew preposition inventory is small and R6 tokens are short (1–2 consonants), the expected match rate may be high even by chance.

### 5.2 Control design
- **Control pool 1**: Non-R6 token types of matching length distribution — what fraction match Hebrew prepositions?
- **Control pool 2**: R6 tokens tested against a non-Hebrew vocabulary (Latin, Arabic) of matching item count — does the Hebrew alignment stand out?
- **Neither control has been formally run**. This is the primary gap making P2-CLAIM-018 PROVISIONAL.

---

## 6. What Is Measured, Inferred, and Not Yet Proven

| Category | Description |
|----------|-------------|
| **Measured** | The fraction of R6 token types whose EVA consonant skeleton is consistent with Hebrew preposition consonant forms, using a pre-specified comparison set |
| **Inferred** | That R6 tokens preferentially match Hebrew grammatical forms relative to chance or relative to non-R6 tokens |
| **Not yet proven** | That the match rate is above baseline; that R6 tokens encode Hebrew prepositions specifically (vs. any short grammatical words in any candidate language); that the match reflects phonological or semantic content |
| **Explicitly not claimed** | That the Voynich manuscript is in Hebrew; that R6 tokens are deciphered prepositions; that the match is sufficient to constrain the manuscript's language |

---

## 7. Limitations

1. **Scoring not fully documented**: The exact token pool, comparison set, and matching rules for the 52.6% figure are not yet fully specified in the repository. This is the primary reason P2-CLAIM-018 is PROVISIONAL.

2. **No null model comparison**: The 52.6% rate has not been compared against a baseline for random short EVA sequences or for non-Hebrew vocabulary. Without this, the rate cannot be interpreted as above-chance.

3. **Short token problem**: Many R6 tokens are very short (2–4 EVA glyphs), making consonant-level alignment ambiguous. A single consonant match (`l` → Hebrew `ל`) is very weak evidence.

4. **Ayin/Aleph ambiguity**: Hebrew `ʿ` (Ayin) and `ʾ` (Aleph) are phonologically distinct but may map to the same EVA glyph; this introduces alignment ambiguity for forms beginning with gutturals.

5. **Transcription comparability**: R6 tokens (`ol`, `al`, `or`, `ar`) are present in both Takahashi H and ZL Eva-, so direct cross-transliteration testing is possible (`NORMALIZATION_REQUIRED` due to count differences). However, the scoring method must first be documented before replication can proceed.

---

## 8. Supported Claim IDs

| Claim ID | Support role | Status |
|----------|-------------|--------|
| P2-CLAIM-018 | Primary claim supported by this method | `PROVISIONAL` (pending null model and full documentation) |
| P1-CLAIM-006 | Background support: `qok-` prefix exclusive to R1; R6 tokens are structurally distinct from R1 | `CONFIRMED` (independently) |

---

## 9. Repo Traceability

| Item | Path | Notes |
|------|------|-------|
| R6 token role assignments | `results/p1_1_cluster_frequencies.csv` (column `role = R6`) | Definitive R6 type list |
| Partial alignment script | `scripts/ROSETTA3_ain_stem_alignment.py` | Partial implementation; scoring not complete for R6 |
| Target: complete alignment script | `scripts/R6_hebrew_alignment.py` (not yet created) | Required for CONFIRMED status upgrade |
| Target: R6 scoring output | `results/R6_hebrew_alignment_results.json` (not yet created) | Required for CONFIRMED status upgrade |

---

## 10. Steps Required for CONFIRMED Status

P2-CLAIM-018 can be upgraded from `PROVISIONAL` to `CONFIRMED` when all of the following are complete:

- [ ] Pre-specify the exact R6 token pool (list all R6 type strings from `results/p1_1_cluster_frequencies.csv`)
- [ ] Pre-specify the Hebrew preposition inventory (freeze the comparison set)
- [ ] Pre-specify the normalization rule (vowel-stripping vs. full-glyph)
- [ ] Pre-specify the match criterion (1-con vs. 2-con minimum)
- [ ] Compute the null baseline (random 2-con match rate against the pre-specified Hebrew set)
- [ ] Run Control pool 1 (non-R6 tokens of matching length)
- [ ] Run Control pool 2 (R6 tokens vs. non-Hebrew vocabulary)
- [ ] Write `scripts/R6_hebrew_alignment.py` with reproducible output
- [ ] Confirm 52.6% is above baseline with p-value or effect size
- [ ] Update `docs/CLAIM_REGISTRY.md` P2-CLAIM-018 status and this document
