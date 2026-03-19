#!/usr/bin/env python3
"""
P1.5: Cross-transliteration robustness check.

Repeat P1.1 cluster frequency counts using takahashi.txt (standalone plain-text format),
then correlate with primary corpus results from p1_1_cluster_frequencies.csv.

Metrics:
  - Pearson + Spearman correlation for: total counts, %initial, %final
  - If correlations >0.8: cross-transliteration robustness confirmed
"""

import csv
import json
import math
import re
from collections import defaultdict, Counter
from pathlib import Path

BASE_DIR = Path("/Users/roble/Library/Mobile Documents/com~apple~CloudDocs/Blog Article/Voynich_Manusript")
SRC_DIR = BASE_DIR / "voynich_sources"
P1_DIR  = BASE_DIR / "research" / "P1_structural"

SPBCEH_CLUSTERS = {
    "INIT":  ["qokeedy","qokeey","qokedy","qokaiin","qokai!n","qokar","qokol","qoky","qokal","qokey","fachys"],
    "CLOSE": ["chedy","shedy","chey","shey","cfhaiin","ykchdy","cheey","sheey","chdy","lchedy"],
    "LINK":  ["okaiin","okeey","otar","otedy","oteey","okar","okal"],
    "ACT":   ["daiin","dain","dai!n","dar","dal","dol"],
    "MODE":  ["shol","chol","shor","chor","cheol","sheol"],
    "TIME":  ["aiin","aiiin","saiin","otaiin"],
    "REF":   ["ol","or","al"],
}
ALL_CLUSTERS = [c for cs in SPBCEH_CLUSTERS.values() for c in cs]
CLUSTER_SET = set(ALL_CLUSTERS)


# ──────────────────────────────────────────────────────────
# Parse takahashi.txt
# ──────────────────────────────────────────────────────────
def clean_token(tok):
    """Strip takahashi.txt special markers and return clean EVA token or None."""
    # Remove bracketed markers: <!@...>, <!...>, <$>, <->
    tok = re.sub(r'<[^>]*>', '', tok)
    # Remove uncertainty chars: !, ?, at start/end (they modify letters like 'dai!n')
    # Keep internal ! as it's part of some EVA tokens (e.g., dai!n)
    tok = tok.strip('?').strip()
    # Strip leading/trailing !
    tok = tok.strip('!')
    # Remove remaining non-EVA characters
    tok = re.sub(r'[^a-z!]', '', tok)
    if not tok or len(tok) < 1:
        return None
    return tok


def parse_takahashi(path):
    """
    Parse takahashi.txt into lines of clean EVA tokens.
    Returns: list of lists (each inner list = tokens on one line, in order)
    """
    lines_out = []
    with open(path, encoding='utf-8', errors='replace') as f:
        for raw_line in f:
            raw_line = raw_line.rstrip('\n')
            if not raw_line.strip():
                continue
            # Split on '.'
            parts = raw_line.split('.')
            tokens = []
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                tok = clean_token(part)
                if tok and len(tok) >= 2:  # minimum meaningful EVA token
                    tokens.append(tok)
            if tokens:
                lines_out.append(tokens)
    return lines_out


# ──────────────────────────────────────────────────────────
# Count cluster frequencies and positional percentages
# ──────────────────────────────────────────────────────────
def count_clusters(lines):
    """
    For each line, classify tokens by position (initial/medial/final/only).
    Returns: dict cluster -> {n_total, n_initial, n_medial, n_final, n_only}
    """
    counts = {c: {"n_total": 0, "n_initial": 0, "n_medial": 0, "n_final": 0, "n_only": 0}
              for c in ALL_CLUSTERS}

    for line in lines:
        n = len(line)
        for i, tok in enumerate(line):
            if tok not in CLUSTER_SET:
                continue
            counts[tok]["n_total"] += 1
            if n == 1:
                counts[tok]["n_only"] += 1
            elif i == 0:
                counts[tok]["n_initial"] += 1
            elif i == n - 1:
                counts[tok]["n_final"] += 1
            else:
                counts[tok]["n_medial"] += 1

    # Compute percentages
    for c, d in counts.items():
        total = d["n_total"]
        classified = total - d["n_only"]
        if classified > 0:
            d["pct_initial"] = d["n_initial"] / classified
            d["pct_medial"]  = d["n_medial"]  / classified
            d["pct_final"]   = d["n_final"]   / classified
        else:
            d["pct_initial"] = d["pct_medial"] = d["pct_final"] = 0.0

    return counts


# ──────────────────────────────────────────────────────────
# Pearson and Spearman correlations
# ──────────────────────────────────────────────────────────
def pearson(x, y):
    n = len(x)
    if n < 3:
        return 0.0
    mx, my = sum(x)/n, sum(y)/n
    num = sum((xi-mx)*(yi-my) for xi, yi in zip(x, y))
    dx  = math.sqrt(sum((xi-mx)**2 for xi in x))
    dy  = math.sqrt(sum((yi-my)**2 for yi in y))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def spearman(x, y):
    n = len(x)
    if n < 3:
        return 0.0
    def ranks(v):
        sorted_v = sorted(enumerate(v), key=lambda t: t[1])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n-1 and sorted_v[j][1] == sorted_v[j+1][1]:
                j += 1
            avg = (i + 1 + j + 1) / 2
            for k in range(i, j+1):
                r[sorted_v[k][0]] = avg
            i = j + 1
        return r
    return pearson(ranks(x), ranks(y))


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
def main():
    print("P1.5 — Cross-transliteration robustness")

    # Load primary corpus P1.1 results
    primary = {}
    with open(P1_DIR / "p1_1_cluster_frequencies.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            primary[row["cluster"]] = {
                "n_total":     int(row["n_total"]),
                "pct_initial": float(row["pct_initial"]),
                "pct_final":   float(row["pct_final"]),
                "pct_medial":  float(row["pct_medial"]),
            }
    print(f"Primary corpus: {len(primary)} clusters loaded from P1.1")

    # Parse takahashi.txt
    tak_path = SRC_DIR / "takahashi.txt"
    print(f"Parsing {tak_path}...")
    lines = parse_takahashi(tak_path)
    total_lines = len(lines)
    total_tokens = sum(len(l) for l in lines)
    print(f"Lines: {total_lines}, Total tokens: {total_tokens}")

    # Count clusters
    tak_counts = count_clusters(lines)
    total_classified = sum(d["n_total"] for d in tak_counts.values())
    print(f"Classified tokens (SPBCEH clusters): {total_classified}")

    # Print cluster comparison table
    print("\nCluster counts comparison (primary vs takahashi.txt):")
    print(f"{'Cluster':<12} {'Role':<6} {'Primary_n':>10} {'Tak_n':>8} {'P_init%':>8} {'T_init%':>8} {'P_final%':>8} {'T_final%':>8}")

    role_map = {c: r for r, cs in SPBCEH_CLUSTERS.items() for c in cs}
    common_clusters = [c for c in ALL_CLUSTERS if c in primary and tak_counts[c]["n_total"] > 0]

    for c in ALL_CLUSTERS:
        p = primary.get(c, {})
        t = tak_counts.get(c, {})
        print(f"{c:<12} {role_map.get(c,'?'):<6} {p.get('n_total',0):>10} {t.get('n_total',0):>8} "
              f"{p.get('pct_initial',0)*100:>7.1f}% {t.get('pct_initial',0)*100:>7.1f}% "
              f"{p.get('pct_final',0)*100:>7.1f}% {t.get('pct_final',0)*100:>7.1f}%")

    # Filter to clusters present in both
    both = [c for c in ALL_CLUSTERS if c in primary and tak_counts[c]["n_total"] > 5]
    print(f"\nClusters with n>5 in takahashi.txt: {len(both)}")

    prim_n   = [primary[c]["n_total"]     for c in both]
    tak_n    = [tak_counts[c]["n_total"]  for c in both]
    prim_pi  = [primary[c]["pct_initial"] for c in both]
    tak_pi   = [tak_counts[c]["pct_initial"] for c in both]
    prim_pf  = [primary[c]["pct_final"]   for c in both]
    tak_pf   = [tak_counts[c]["pct_final"]   for c in both]

    r_n_p   = pearson(prim_n,  tak_n)
    r_n_s   = spearman(prim_n, tak_n)
    r_pi_p  = pearson(prim_pi,  tak_pi)
    r_pi_s  = spearman(prim_pi, tak_pi)
    r_pf_p  = pearson(prim_pf,  tak_pf)
    r_pf_s  = spearman(prim_pf, tak_pf)

    print(f"\nCorrelations (n={len(both)} clusters):")
    print(f"  Total counts:    Pearson r={r_n_p:.4f},  Spearman rho={r_n_s:.4f}")
    print(f"  %initial:        Pearson r={r_pi_p:.4f}, Spearman rho={r_pi_s:.4f}")
    print(f"  %final:          Pearson r={r_pf_p:.4f}, Spearman rho={r_pf_s:.4f}")

    # LINK medial check
    print("\nLINK cluster medial percentages (takahashi.txt):")
    for c in SPBCEH_CLUSTERS["LINK"]:
        t = tak_counts[c]
        if t["n_total"] > 0:
            print(f"  {c}: {t['pct_medial']*100:.1f}% medial (n={t['n_total']})")

    results = {
        "n_lines": total_lines,
        "n_tokens_total": total_tokens,
        "n_tokens_classified": total_classified,
        "n_clusters_compared": len(both),
        "pearson_total_counts":  r_n_p,
        "spearman_total_counts": r_n_s,
        "pearson_pct_initial":   r_pi_p,
        "spearman_pct_initial":  r_pi_s,
        "pearson_pct_final":     r_pf_p,
        "spearman_pct_final":    r_pf_s,
        "tak_cluster_counts": {c: tak_counts[c] for c in ALL_CLUSTERS},
    }

    out = P1_DIR / "p1_5_cross_transliteration_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out}")
    return results


if __name__ == "__main__":
    main()
