#!/usr/bin/env python3
"""
smoke_test.py — verify repo structure, key output artifacts, and headline metrics.

Does NOT re-run scripts. Checks that:
1. Required parsed data files exist (corpus_tokens.csv, corpus_lines.csv)
2. Key result files exist (Paper 1 + Paper 2 primary outputs)
3. Headline metrics in result files match expected values
4. Docs and claim registry files are present
5. Warns if raw IVTFF source corpus is absent (needed only to re-run parse_corpus.py)

Run from repo root: python scripts/smoke_test.py
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
PASS = []
FAIL = []
WARN = []


def check(label, condition, detail=""):
    if condition:
        PASS.append(label)
    else:
        FAIL.append(f"{label}{': ' + detail if detail else ''}")


def warn(label, condition, detail=""):
    if not condition:
        WARN.append(f"{label}{': ' + detail if detail else ''}")


# ── 0. Corpus source availability (informational) ────────────────────────────
corpus_src = BASE / "data" / "Lsi_ivtff_0d_v4j_fixed.txt"
warn(
    "data/Lsi_ivtff_0d_v4j_fixed.txt present (needed to re-run parse_corpus.py)",
    corpus_src.exists(),
    "download from https://www.voynich.nu/transcr.html and place in data/",
)

# ── 1. Parsed data files ──────────────────────────────────────────────────────
check("data/corpus_tokens.csv exists", (BASE / "data" / "corpus_tokens.csv").exists())
check("data/corpus_lines.csv exists", (BASE / "data" / "corpus_lines.csv").exists())

# ── 2. Paper 1 result files ──────────────────────────────────────────────────
check("results/p1_1_cluster_frequencies.csv exists",
      (BASE / "results" / "p1_1_cluster_frequencies.csv").exists())
check("results/p1_6_transition_matrix.json exists",
      (BASE / "results" / "p1_6_transition_matrix.json").exists())
check("results/p1_3_falsification_v1.1_results.json exists",
      (BASE / "results" / "p1_3_falsification_v1.1_results.json").exists())
check("results/p1_4_classification_results.json exists",
      (BASE / "results" / "p1_4_classification_results.json").exists())

# ── 3. Paper 2 primary result files ──────────────────────────────────────────
check("results/p2_all_results.json exists",
      (BASE / "results" / "p2_all_results.json").exists())
check("results/p2_5_v2_6role_results.json exists",
      (BASE / "results" / "p2_5_v2_6role_results.json").exists())

# ── 4. Paper 2 supporting result files ───────────────────────────────────────
check("results/PILOT4_balneo_packet_results.json exists",
      (BASE / "results" / "PILOT4_balneo_packet_results.json").exists())
check("results/DECODE3_qol_results.json exists",
      (BASE / "results" / "DECODE3_qol_results.json").exists())
check("results/ROSETTA3c_qotaiin_positional_results.json exists",
      (BASE / "results" / "ROSETTA3c_qotaiin_positional_results.json").exists())
check("results/R6_hebrew_alignment_results.json exists",
      (BASE / "results" / "R6_hebrew_alignment_results.json").exists())

# ── 5. Headline metric spot-checks ───────────────────────────────────────────

# Paper 1: R2→R1 z-score (7-role model, expected ≈ +9.75)
p1_6 = BASE / "results" / "p1_6_transition_matrix.json"
if p1_6.exists():
    data = json.loads(p1_6.read_text())
    try:
        z = data["zscores"]["CLOSE"]["INIT"]["z"]
        check("R2→R1 z-score (7-role) ≥ 9.0", float(z) >= 9.0, f"got {z:.3f}")
    except (KeyError, TypeError):
        FAIL.append("p1_6_transition_matrix.json: zscores.CLOSE.INIT.z key not found")

# Paper 1: SPBCEH section classification accuracy (7-role, expected ≈ 69.8%)
p1_4 = BASE / "results" / "p1_4_classification_results.json"
if p1_4.exists():
    data = json.loads(p1_4.read_text())
    acc = data.get("best_section_spbceh")
    if acc is not None:
        check("P1 SPBCEH section accuracy ≥ 0.60", float(acc) >= 0.60, f"got {acc:.3f}")
    else:
        FAIL.append("p1_4_classification_results.json: best_section_spbceh key not found")

# Paper 2: paragraph-level FSA conformance (expected 61.3%)
p2_all = BASE / "results" / "p2_all_results.json"
if p2_all.exists():
    data = json.loads(p2_all.read_text())
    try:
        fsa = data["p2_1"]["para_level"]["pct_conformant_trans"]
        check("P2 FSA paragraph conformance ≥ 60.0%", float(fsa) >= 60.0, f"got {fsa:.1f}%")
        check("P2 FSA paragraph conformance ≤ 63.0% (sanity bound)",
              float(fsa) <= 63.0, f"got {fsa:.1f}%")
    except (KeyError, TypeError):
        FAIL.append("p2_all_results.json: p2_1.para_level.pct_conformant_trans not found")

# Paper 2: 6-role classification accuracy (expected 64.7%)
p2_6role = BASE / "results" / "p2_5_v2_6role_results.json"
if p2_6role.exists():
    data = json.loads(p2_6role.read_text())
    acc6 = data.get("p14_cls_accuracy")
    if acc6 is not None:
        check("P2 6-role classification accuracy ≥ 0.60", float(acc6) >= 0.60,
              f"got {acc6:.3f}")
    else:
        FAIL.append("p2_5_v2_6role_results.json: p14_cls_accuracy key not found")
    # 6-role z-score (expected ≈ 9.71)
    z6 = data.get("p16_close_init_z")
    if z6 is not None:
        check("P2 6-role CLOSE→INIT z ≥ 9.0", float(z6) >= 9.0, f"got {z6:.3f}")
    else:
        FAIL.append("p2_5_v2_6role_results.json: p16_close_init_z key not found")

# ── 6. Docs and claim registry ───────────────────────────────────────────────
check("docs/CLAIM_REGISTRY.md exists", (BASE / "docs" / "CLAIM_REGISTRY.md").exists())
check("docs/TIER_REGISTRY.md exists", (BASE / "docs" / "TIER_REGISTRY.md").exists())
check("docs/EXPECTED_OUTPUTS.md exists", (BASE / "docs" / "EXPECTED_OUTPUTS.md").exists())
check("annex_maps/ANNEX_B8_verification_index.md exists",
      (BASE / "annex_maps" / "ANNEX_B8_verification_index.md").exists())

# ── Report ───────────────────────────────────────────────────────────────────
print(f"\nSmoke test: {len(PASS)} passed, {len(FAIL)} failed, {len(WARN)} warnings\n")
for p in PASS:
    print(f"  OK    {p}")
for w in WARN:
    print(f"  WARN  {w}")
for f in FAIL:
    print(f"  FAIL  {f}")

if FAIL:
    sys.exit(1)
