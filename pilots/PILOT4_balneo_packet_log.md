# PILOT4 — Balneological Packet Structure Analysis
**Date**: 2026-03-19

---

## Summary

| Metric | Result |
|--------|--------|
| Total packets reconstructed | 897 |
| Section B packets | **374 (41.7%)** |
| Section B as % of corpus tokens | 18.5% |
| B packet density vs corpus density | **2.26×** |
| Dominant B R2 (CLOSE) | `shedy` (31.6%) |
| `shedy` concentration in B | **59% of all shedy-closed packets** |
| `qol` as first-payload in B | OR=7.83, p<0.01 |
| `qokeedy` as first-payload in B | OR=20.61, p<0.0001 |
| Recurring B templates found | 2 (n≥2 each) |

---

## Key Findings

### 1. Section B is the most packet-dense section

Section B accounts for 41.7% of all reconstructed packets (374/897) while representing only 18.5% of corpus tokens. This gives a **packet density 2.26× the corpus average** — by far the highest of any section.

| Section | Packets | Token % | Packet density |
|---------|---------|---------|----------------|
| B | 374 (41.7%) | 18.5% | **2.26×** |
| S | 341 (38.0%) | 28.8% | 1.32× |
| H | 94 (10.5%) | 29.0% | 0.36× |
| P | 29 (3.2%) | 6.8% | 0.47× |

Interpretation: Balneological text is structurally the most packet-structured section of the manuscript. Each token in section B is more likely to be part of a complete R1→payload→R2 cycle than in any other section. This is consistent with a highly procedural or intensely experienced section that generates more discrete "recording events."

### 2. `shedy` is the Balneological-specific closure marker

Section B has a distinct R2 distribution: `shedy` (31.6% of B packets) vs `chedy` (24.3%). In Herbal (H), `chedy` dominates (22.3%) and `shedy` is less frequent (13.8%). In Stars (S), `chedy` (25.5%) and `shedy` (16.4%) are both present.

**`shedy` distribution across sections**: B=59%, S=28%, H=6%

This quantifies at the packet level the `ch/sh` alternation finding from Paper 2: `shedy` is the Balneological closure marker; `chedy` is more general. The `sh-` stem signals not just domain (Balneological) but specifically **packet termination in the Balneological domain**. This is a domain-specific grammatical variant — the clearest example of domain-coupling in the packet grammar.

### 3. First-payload slot in section B contains INIT tokens

The most striking structural finding: in section B, the most common first-payload tokens (the token immediately after the R1 initiator) are themselves INIT-classified tokens:

| First-payload token | n | % of B packets | OR vs other sections |
|--------------------|---|----------------|---------------------|
| `qokeedy` [INIT] | 13 | 4.1% | **20.61×, p<0.0001** |
| `qokal` [INIT] | 9 | 2.8% | 4.68×, p<0.05 |
| `qokaiin` [INIT] | 9 | 2.8% | — |
| `qokedy` [INIT] | 8 | 2.5% | — |
| `qol` [CONTENT] | 10 | 3.2% | **7.83×, p<0.01** |
| `ol` [REF] | 12 | 3.8% | — |

**INIT tokens appearing in payload positions** suggests one of:

**A. Nested packets**: R1→[sub-packet R1...R2]→outer-R2. If section B has hierarchical (nested) packet structure, it would have context-free rather than finite-state grammar complexity — a significant structural upgrade from the FSA model.

**B. Role bleed**: INIT tokens occasionally appear in medial contexts, particularly in the dense B section, due to scribal or notational flexibility.

**C. "Recall initiators"**: In a procedural notation, a new sub-procedure might be initiated inside an outer procedure (analogous to a function call inside a function body). Section B's high-complexity content (body-experiential states, bath procedures) may require this recursive structure.

Follow-up required: Count what fraction of B-packets where first-payload is INIT actually contain a nested R1...R2 sub-sequence within the outer packet.

### 4. `qol` as first-payload entity in section B

`qol` appears as the first payload token in 10/317 B packets (3.2%), enriched vs other sections at OR=7.83 (p<0.01). This means `qol` preferentially **leads** Balneological packet payloads — it is more likely to be the first content token after R1 in section B than in any other section.

Combined with the PILOT3 finding that `qol` is enriched inside packets overall (2.01× by ROSETTA2 method, 1.39× by PILOT3 method), `qol` appears to be a Balneological-specific inner-packet function word that occupies a leading position in B packet payloads.

### 5. `qokain` — hybrid INIT-prefix / CONTENT token

`qokain` (n=69, 3.91× Balneological) is **not** an INIT packet-initiator. It has 94% medial position → it appears inside packets, not at their start. It carries the `qok-` INIT-prefix morpheme (shared with R1 tokens like `qokeedy`, `qokal`) but functions as an inner-packet CONTENT token.

This is the first confirmed case of a token that shares INIT-prefix morphology but functions at the content layer. Two interpretations:
- `qokain` = a content-layer reference to the initiating entity ("the initiator of this [bath]" as a mid-packet reference)
- `qokain` = a morphological variant of `qokai!n` [INIT] that shifted to medial/content use in the Balneological section

The `-ain` suffix in `qokain` links it to the `-ain` entity-label family investigated in PILOT2 and planned in PILOT5. `qokain` may be an entity label (`qok-` + `-ain` = [initiating] + [spring/eye?]) that functions in mid-packet context in section B.

### 6. Recurring Balneological packet templates

| Template (R1 | first_payload | R2) | n | Note |
|---|---|---|---|----|
| `qokai!n \| qokeey \| shedy` | 2 | B-specific; shedy closure |
| `qokeedy \| r \| shedy` | 2 | B-specific; shedy closure |

Both recurring B-specific templates close with `shedy`, consistent with finding #2. The second template (`qokeedy | r | shedy`) is notable: `r` is an extremely short token — possibly an abbreviated entity label or a positional marker. Only two tokens in B packets have payload of just `r`: this is a compressed packet structure.

---

## Revised Model: Section B Grammar

The standard FSA packet grammar appears insufficient for section B. Evidence for enhanced complexity:

1. **Packet density 2.26× average**: B generates more packet cycles per token
2. **First-payload INIT tokens (4.1% = qokeedy)**: Suggests nested or recursive structure
3. **shedy as domain-specific R2**: B has a grammatical variant of the closure token
4. **qol leading payloads (OR=7.83)**: B has a preferred inner-function word that leads packet content

Proposed revision: Section B may operate a **two-level packet grammar** — outer packets (R1→content→R2) containing inner sub-packets (INIT→short-payload→CLOSE), with `qol` as the inner-packet trigger. This would be the strongest evidence yet that the Voynich notation exceeds finite-state complexity in at least one section.

---

## Status

**B section as most packet-dense**: CONFIRMED (2.26× average density)
**shedy as B-specific R2 variant**: CONFIRMED (59% of all shedy-closed packets in B)
**qol as B first-payload entity**: CONFIRMED (OR=7.83, p<0.01)
**Nested packet structure in B**: CANDIDATE — needs direct count of sub-sequences
**qokain as hybrid INIT-prefix / CONTENT token**: CONFIRMED (94% medial)
**Recurring B-specific templates**: IDENTIFIED (n=2, low count — suggestive only)

---

## Next Steps

- **PILOT5**: Count nested packet sub-sequences in B directly — test whether first-payload INIT tokens initiate sub-packets that close before the outer R2
- **PILOT6**: `-ain` suffix sub-folio analysis (Stars section, per instructions 2b)
- **ROSETTA3**: Medieval Latin balneological lexicon alignment for sal / salus cluster

---

## Files
- `PILOT4_balneo_packet_structure.py` — analysis script
- `PILOT4_balneo_packet_results.json` — raw results
- `PILOT4_balneo_packet_log.md` — this file

---

## Addendum: Nested Packet Hypothesis — REFUTED

Follow-up test (2026-03-19): Among 67 B-section outer packets where first-payload token is INIT-classified, **0/67 contain an internal CLOSE token** within the outer payload. 

**Nested packet hypothesis: NOT SUPPORTED.**

The INIT tokens in B first-payload positions are genuine role-bleed, not sub-packet initiators. The Balneological grammar is finite-state but with elevated INIT-in-content-position rate.

### Cross-section INIT-bleed rate:

| Section | Total packets | INIT first-payload | Rate |
|---------|-------------|-------------------|------|
| B | 374 | 67 | **17.9%** |
| S | 341 | 27 | 7.9% |
| H | 94 | 6 | 6.4% |
| P | 29 | 0 | 0.0% |

Section B INIT-bleed is 2.26× higher than Stars, 2.80× higher than Herbal. This is a real grammatical property of the Balneological section: INIT-morpheme tokens have a higher rate of appearing in content/payload positions in B than in any other section. Revised interpretation: In section B, the `qok-` morpheme functions as both a structural initiator AND a content-layer entity reference at elevated rates.
