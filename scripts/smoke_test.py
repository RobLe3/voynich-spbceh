#!/usr/bin/env python3
"""
smoke_test.py — verify repo structure and key output artifacts exist.

Does NOT re-run scripts. Checks that:
1. Required data files exist (corpus_tokens.csv)
2. Key result files exist
3. Headline metrics in result files match expected values

Run from repo root: python scripts/smoke_test.py
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
PASS = []
FAIL = []


def check(label, condition, detail=""):
    if condition:
        PASS.append(label)
    else:
        FAIL.append(f"{label}{': ' + detail if detail else ''}")


# ── 1. Data files ────────────────────────────────────────────────────────────
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

# ── 3. Paper 2 result files ──────────────────────────────────────────────────
check("results/PILOT4_balneo_packet_results.json exists",
      (BASE / "results" / "PILOT4_balneo_packet_results.json").exists())
check("results/DECODE3_qol_results.json exists",
      (BASE / "results" / "DECODE3_qol_results.json").exists())
check("results/ROSETTA3c_qotaiin_positional_results.json exists",
      (BASE / "results" / "ROSETTA3c_qotaiin_positional_results.json").exists())
check("results/R6_hebrew_alignment_results.json exists",
      (BASE / "results" / "R6_hebrew_alignment_results.json").exists())

# ── 4. Headline metric spot-checks ───────────────────────────────────────────
p1_6 = BASE / "results" / "p1_6_transition_matrix.json"
if p1_6.exists():
    data = json.loads(p1_6.read_text())
    z = data.get("R2_to_R1_z_score") or data.get("z_score")
    if z is not None:
        check("R2→R1 z-score ≥ 9.0", float(z) >= 9.0, f"got {z}")
    else:
        FAIL.append("p1_6_transition_matrix.json: R2_to_R1_z_score key not found")

p1_4 = BASE / "results" / "p1_4_classification_results.json"
if p1_4.exists():
    data = json.loads(p1_4.read_text())
    acc = data.get("best_section_accuracy") or data.get("section_accuracy")
    if acc is not None:
        check("Section classification ≥ 0.60", float(acc) >= 0.60, f"got {acc}")
    else:
        FAIL.append("p1_4_classification_results.json: best_section_accuracy key not found")

# ── 5. Docs and claim registry ───────────────────────────────────────────────
check("docs/CLAIM_REGISTRY.md exists", (BASE / "docs" / "CLAIM_REGISTRY.md").exists())
check("docs/TIER_REGISTRY.md exists", (BASE / "docs" / "TIER_REGISTRY.md").exists())
check("annex_maps/ANNEX_B8_verification_index.md exists",
      (BASE / "annex_maps" / "ANNEX_B8_verification_index.md").exists())

# ── Report ───────────────────────────────────────────────────────────────────
print(f"\nSmoke test: {len(PASS)} passed, {len(FAIL)} failed\n")
for p in PASS:
    print(f"  OK  {p}")
for f in FAIL:
    print(f"  FAIL  {f}")

if FAIL:
    sys.exit(1)
