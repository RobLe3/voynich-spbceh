# ROSETTA2 — sal Packet-Internal Position Analysis
**Date**: 2026-03-19

---

## Summary

| Metric | Result |
|--------|--------|
| sal total occurrences | 44 |
| sal section enrichment (B) | 2.08× |
| sal section enrichment (Z) | 2.55× |
| sal in packet payloads | 17/44 = 38.6% |
| sal payload enrichment | **1.44×** |
| sal mean position in payloads | 0.552 (central, p=0.52 ns) |
| sal immediately before CLOSE (R2) | 4 cases |
| sal immediately after INIT (R1) | 3 cases |
| sal-family total (9 members) | 63 occurrences |
| sal-family B enrichment | 1.71× |

---

## Key Findings

### 1. sal is elevated inside packet payloads (1.44×)

`sal` appears in 38.6% of cases inside complete packet payloads, vs 26.7% for the full corpus. Payload enrichment: **1.44×** — higher than structural `ol` (1.35×), lower than inner-function `qol` (2.01×). This places `sal` in the same enrichment range as frame tokens, suggesting it is NOT a random content word but has a preferential association with the packet interior.

### 2. sal is NOT positionally biased within payloads

Mean relative position 0.552 (0=first, 1=last in payload), t-test p=0.52. `sal` is not systematically early or late within packets. This is the same result as `qol` (0.516, p=0.68) and `ol` (0.505, p=0.84) — all three central. No token analyzed shows positional bias within payloads.

### 3. sal appears in BOTH subject and object positions

In the 10 Balneological packets where `sal` appears:

| Folio | Rel. position | Interpretation |
|-------|--------------|----------------|
| f75r | 0.08 | **First payload token** — entity-subject slot |
| f82r | 0.20 | Near-first — entity-subject |
| f75v | 0.25 | Early — entity-subject |
| f77v | 0.67 | Mid-late |
| f80r (1) | 0.66 | Mid-late |
| f80r (2) | 0.81 | Late |
| f76r (2) | 0.92 | Near-last |
| f76r (1) | 1.00 | **Last payload token** — entity-object/product slot |
| f77r | 1.00 | Last — entity-object/product |
| f82r | — | mid |

**sal appears at both extremes** (first and last payload positions) in the Balneological section. This is consistent with `sal` functioning as **a named entity** (either the subject or the product/outcome of the packet procedure) rather than a structural connector. Entities are not positionally constrained in the same way function words are.

### 4. sal follows or precedes CLOSE tokens directly

- 4 cases where the token immediately following `sal` is a CLOSE (R2) marker → sal occupies the final entity slot before packet closure
- 3 cases where sal is preceded by INIT (R1) → sal is the first content token after packet initiation

The CLOSE-following pattern (4 cases) is particularly significant. If we interpret packets as structured procedures ("R1[initiate] + [entities] + R2[close]"), then sal-immediately-before-R2 suggests `sal` is the **terminal entity** of the procedure — potentially the **output, product, or result** being recorded.

### 5. Comparison with calibration tokens

| Token | n_in_pkts | Mean position | p_vs_0.5 | Payload enrich |
|-------|-----------|--------------|----------|----------------|
| `sal` | 17 | 0.552 | 0.52 ns | **1.44×** |
| `qol` | 78 | 0.516 | 0.68 ns | **2.01×** |
| `ol`  | 182 | 0.505 | 0.84 ns | **1.35×** |
| `daiin` | 148 | 0.489 | 0.67 ns | 0.74× (depleted) |
| `aiin` | 121 | 0.550 | 0.07 ns | — |

`daiin` (n=748, the most common token) is DEPLETED inside packets (0.74×). `sal` is enriched (1.44×). This is a meaningful structural difference: `daiin` is an inter-packet or framing token; `sal` is an intra-packet content token.

### 6. sal section enrichment

`sal` is enriched in B (2.08×), Z (2.55×), P (1.68×). It is DEPLETED in H (0.47×) and S (0.63×). The Zodiac (Z) enrichment (2.55×) is higher than Balneological — this was not expected and warrants investigation. Z section in the Takahashi transliteration corresponds to Zodiac-adjacent text, which may share subject matter with Balneological material.

Note: Previously reported enrichment of 3.54× for `sal` in Balneological was likely from a different normalization method (paragraph-level vs token-level). Current figure (2.08×) is the per-token enrichment.

---

## Revised Interpretation

`sal` is an intra-packet entity token (1.44× enrichment) that appears across the payload — not biased to early or late positions. It is compatible with the **entity-label hypothesis** (sal = a named entity within the procedure being recorded) but the positional ambiguity prevents distinguishing subject vs. object role.

The most informative finding is the **terminal sal** pattern (4 cases of sal immediately before R2 close): if sal = Latin *sal* (salt) or *salus* (health/well-being), the terminal position would correspond to recording "...resulting in [salt/health]" as the packet outcome. This is consistent with a balneological recipe format: list ingredients/procedures → record outcome.

---

## sal Morphological Family

| Token | n | Top section | Note |
|-------|---|-------------|------|
| `sal` | 44 | B (17) | Core form |
| `sal!` | 5 | H (4) | Uncertain-char variant |
| `saly` | 3 | Z (1), P (1), S (1) | Extended suffix |
| `salar` | 2 | A, S | Extended suffix |
| `saldam` | 2 | C, P | Compound |
| `saldy` | 2 | H, B | Extended suffix |
| `salkeedy` | 2 | B, S | CLOSE-suffix compound? |
| `salo` | 2 | P, S | Vocalic extension |
| `salal` | 1 | Z | Double-al extension |

Family B enrichment: 1.71×. The compound `salkeedy` (n=2: B and S) is notable — it combines `sal` with `keedy` (a CLOSE-type suffix component), possibly compressing the "sal + CLOSE" sequence into a single token.

---

## Status

**sal payload enrichment**: CONFIRMED (1.44×)
**sal positional bias**: NOT CONFIRMED (central, p=0.52)
**sal as terminal entity (before CLOSE)**: CANDIDATE (4/17 packet cases = 24%)
**sal as entity label**: SUPPORTED structurally; specific alignment (Latin sal/salus) remains hypothesis
**sal-family coherence**: PARTIAL (core `sal` is B-enriched; `sal!` is H-enriched; family is distributed)

---

## Files
- `ROSETTA2_sal_packet_position.py` — analysis script
- `ROSETTA2_sal_packet_results.json` — raw results
- `ROSETTA2_sal_packet_log.md` — this file
