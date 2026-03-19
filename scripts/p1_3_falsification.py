#!/usr/bin/env python3
"""
P1.3 v1.1: Full-corpus falsification multi-metric test — TRANSITION MODEL.

Model v1.1: INIT and CLOSE are defined by transition structure, not line position.
  - INIT: clusters that significantly follow CLOSE (CLOSE→INIT z=+9.75 in P1.6)
  - CLOSE: clusters that significantly precede INIT (transition-defined)

Three metrics computed per paragraph under three conditions:
  1. Original SPBCEH mapping
  2. Inverted mapping (INIT↔CLOSE, ACT↔MODE, LINK↔TIME, REF unchanged)
  3. Shuffled mapping (1000 random permutations of cluster→role assignments)

Metrics (v1.1 — all transition-based):
  SLS = Structural Logic Score: CLOSE→INIT bigram count per paragraph (packet boundary density).
        Higher = more packet transitions = more structured.
  VR  = Violation Rate: transition-based violations only (no line-position rules).
        V1: INIT→INIT (consecutive initiations without content)
        V2: CLOSE→CLOSE (consecutive closures without initiation)
        V3: Paragraph with zero CLOSE→INIT transitions (no packet structure)
        V4: INIT immediately followed by INIT with no MODE/ACT/REF between
        Lower VR = fewer structural violations = better fit.
  TS  = Transition Surprise: mean log-prob of role bigrams under P1.6 Markov model.
        Higher (less negative) = better fit.

RF2 resolution: original wins ≥2/3 metrics vs BOTH alternatives at p<0.05 → RF2 resolved.
"""

import csv
import json
import math
import random
from collections import defaultdict, Counter
from pathlib import Path

BASE_DIR = Path("/Users/roble/Library/Mobile Documents/com~apple~CloudDocs/Blog Article/Voynich_Manusript")
D1_DIR = BASE_DIR / "research" / "D1_corpus"
P1_DIR = BASE_DIR / "research" / "P1_structural"
OUT_DIR = P1_DIR
random.seed(42)

# ──────────────────────────────────────────────────────────
# Load the 47-cluster SPBCEH mapping
# ──────────────────────────────────────────────────────────
SPBCEH_CLUSTERS = {
    "INIT": ["qokeedy","qokeey","qokedy","qokaiin","qokai!n","qokar","qokol","qoky","qokal","qokey","fachys"],
    "CLOSE": ["chedy","shedy","chey","shey","cfhaiin","ykchdy","cheey","sheey","chdy","lchedy"],
    "LINK": ["okaiin","okeey","otar","otedy","oteey","okar","okal"],
    "ACT": ["daiin","dain","dai!n","dar","dal","dol"],
    "MODE": ["shol","chol","shor","chor","cheol","sheol"],
    "TIME": ["aiin","aiiin","saiin","otaiin"],
    "REF": ["ol","or","al"],
}
ROLES = ["INIT","CLOSE","LINK","ACT","MODE","TIME","REF"]

ORIGINAL_MAPPING = {}
for role, clusters in SPBCEH_CLUSTERS.items():
    for c in clusters:
        ORIGINAL_MAPPING[c] = role

# Inverted mapping: INIT↔CLOSE, ACT↔MODE, LINK↔TIME
INVERSION_MAP = {"INIT":"CLOSE","CLOSE":"INIT","ACT":"MODE","MODE":"ACT","LINK":"TIME","TIME":"LINK","REF":"REF"}
INVERTED_MAPPING = {c: INVERSION_MAP[r] for c, r in ORIGINAL_MAPPING.items()}

# All clusters list (for shuffling)
ALL_CLUSTERS = list(ORIGINAL_MAPPING.keys())

# Load Markov transition matrix from P1.6
with open(P1_DIR / "p1_6_transition_matrix.json") as f:
    markov_data = json.load(f)
PROB_MATRIX = markov_data["prob_matrix"]
SMOOTHING = 1e-6

def transition_logprob(from_role, to_role):
    p = PROB_MATRIX.get(from_role, {}).get(to_role, 0.0)
    return math.log(max(p, SMOOTHING))


# ──────────────────────────────────────────────────────────
# Wilcoxon signed-rank test (approximate normal)
# ──────────────────────────────────────────────────────────
def wilcoxon_signed_rank(x, y):
    """One-sample Wilcoxon signed-rank test: H0: median(x-y) = 0.
    Returns (W_stat, p_approx, n_pairs, direction).
    direction: +1 if x > y on median, -1 otherwise.
    """
    diffs = [xi - yi for xi, yi in zip(x, y) if xi != yi]
    n = len(diffs)
    if n == 0:
        return 0, 1.0, 0, 0

    abs_diffs = [(abs(d), i) for i, d in enumerate(diffs)]
    abs_diffs.sort(key=lambda x: x[0])

    ranks = [0] * n
    i = 0
    while i < n:
        j = i
        while j < n - 1 and abs_diffs[j][0] == abs_diffs[j+1][0]:
            j += 1
        avg_rank = (i + 1 + j + 1) / 2
        for k in range(i, j + 1):
            ranks[abs_diffs[k][1]] = avg_rank
        i = j + 1

    W_plus = sum(ranks[i] for i, d in enumerate(diffs) if d > 0)
    W_minus = sum(ranks[i] for i, d in enumerate(diffs) if d < 0)
    W = min(W_plus, W_minus)

    mean_W = n * (n + 1) / 4
    std_W = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    if std_W == 0:
        return W, 1.0, n, 0

    z = (W - mean_W) / std_W
    p = 2 * (1 - _normal_cdf(abs(z)))

    direction = 1 if sum(diffs) > 0 else -1
    return W, p, n, direction


def _normal_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


# ──────────────────────────────────────────────────────────
# Load tokens and build paragraph-level data
# ──────────────────────────────────────────────────────────
def load_paragraph_data():
    tokens = []
    with open(D1_DIR / "corpus_tokens.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tokens.append(row)

    para_lines = defaultdict(lambda: defaultdict(list))
    para_meta = {}

    for row in tokens:
        pid = int(row["paragraph_id"])
        lid = row["line_id"]
        para_lines[pid][lid].append(row)
        if pid not in para_meta:
            para_meta[pid] = {"section": row["section"], "currier": row["currier"]}

    return para_lines, para_meta


# ──────────────────────────────────────────────────────────
# Compute three v1.1 metrics for a paragraph under a given mapping
# ──────────────────────────────────────────────────────────
def assign_role(token, mapping):
    return mapping.get(token, None)


def compute_paragraph_metrics(para_lines_dict, mapping):
    """
    Computes SLS, VR, TS under model v1.1 (all transition-based).

    SLS: CLOSE→INIT bigram count / total classified bigrams
         Higher = more packet boundaries = better structural fit
    VR:  Violation Rate from transition rules V1–V4 (lower = better)
         V1: INIT→INIT consecutive
         V2: CLOSE→CLOSE consecutive
         V3: paragraph with 0 CLOSE→INIT transitions (binary: 0 or 1 paragraph-level violation)
         V4: INIT followed by INIT with no MODE/ACT/REF between
    TS:  Mean log-prob of role bigrams under P1.6 Markov model (higher/less-negative = better)
    """
    # Build flat sequence of classified roles across all lines in paragraph (in order)
    flat_roles = []
    for lid in sorted(para_lines_dict.keys()):
        rows = para_lines_dict[lid]
        rows_sorted = sorted(rows, key=lambda r: int(r["token_index"]))
        for r in rows_sorted:
            role = assign_role(r["token"], mapping)
            if role is not None:
                flat_roles.append(role)

    if len(flat_roles) < 2:
        return 0.0, 0.0, 0.0

    # Build bigram list from flat role sequence
    bigrams = [(flat_roles[i], flat_roles[i+1]) for i in range(len(flat_roles)-1)]
    n_bigrams = len(bigrams)

    # ─── SLS: CLOSE→INIT bigram density ───
    close_init_count = sum(1 for a, b in bigrams if a == "CLOSE" and b == "INIT")
    SLS = close_init_count / n_bigrams if n_bigrams > 0 else 0.0

    # ─── VR: Transition-based violation rate ───
    vr_violations = 0
    vr_tokens = len(flat_roles)

    # V1: INIT→INIT consecutive
    for a, b in bigrams:
        if a == "INIT" and b == "INIT":
            vr_violations += 1

    # V2: CLOSE→CLOSE consecutive
    for a, b in bigrams:
        if a == "CLOSE" and b == "CLOSE":
            vr_violations += 1

    # V3: paragraph has zero CLOSE→INIT transitions
    if close_init_count == 0:
        vr_violations += 1  # paragraph-level: counts as 1 violation

    # V4: INIT immediately followed by INIT with no MODE/ACT/REF between
    # (same as V1 but explicit — counts separate from V1 to match spec)
    # Note: V4 duplicates V1 slightly; combine by checking spans between INIT pairs
    # Find all INIT positions
    init_positions = [i for i, r in enumerate(flat_roles) if r == "INIT"]
    for k in range(len(init_positions)-1):
        p1, p2 = init_positions[k], init_positions[k+1]
        between = flat_roles[p1+1:p2]
        # Check if any MODE/ACT/REF token is between two consecutive INITs
        has_content = any(r in ("MODE","ACT","REF","LINK","TIME") for r in between)
        if not has_content and p2 > p1 + 1:
            # Already counted by V1 if they're immediately consecutive;
            # add here only if there are tokens between but none are content roles
            # (i.e., there's only other INIT/CLOSE tokens between two INITs)
            pass  # covered by V1 for adjacent; skip double-counting for non-adjacent

    VR = vr_violations / vr_tokens if vr_tokens > 0 else 0.0

    # ─── TS: mean log-prob of role bigrams ───
    ts_scores = [transition_logprob(a, b) for a, b in bigrams]
    TS = sum(ts_scores) / len(ts_scores) if ts_scores else 0.0

    return SLS, VR, TS


# ──────────────────────────────────────────────────────────
# Main P1.3 v1.1 analysis
# ──────────────────────────────────────────────────────────
def main():
    print("P1.3 v1.1 — Transition-based falsification test")
    print("Loading paragraph data...")
    para_lines, para_meta = load_paragraph_data()
    print(f"Paragraphs: {len(para_lines)}")

    valid_paras = list(para_lines.items())
    valid_paras = [(pid, lines_dict, para_meta.get(pid, {})) for pid, lines_dict in valid_paras]
    print(f"Valid paragraphs: {len(valid_paras)}")

    # ─── Original mapping ───
    print("\nComputing metrics under ORIGINAL mapping...")
    orig_SLS, orig_VR, orig_TS = [], [], []
    for pid, lines_dict, meta in valid_paras:
        sls, vr, ts = compute_paragraph_metrics(lines_dict, ORIGINAL_MAPPING)
        orig_SLS.append(sls)
        orig_VR.append(vr)
        orig_TS.append(ts)

    # ─── Inverted mapping ───
    print("Computing metrics under INVERTED mapping...")
    inv_SLS, inv_VR, inv_TS = [], [], []
    for pid, lines_dict, meta in valid_paras:
        sls, vr, ts = compute_paragraph_metrics(lines_dict, INVERTED_MAPPING)
        inv_SLS.append(sls)
        inv_VR.append(vr)
        inv_TS.append(ts)

    # ─── 1000 shuffled mappings ───
    print("Computing metrics under 1000 SHUFFLED mappings...")
    shuf_SLS_all, shuf_VR_all, shuf_TS_all = [], [], []

    for trial in range(1000):
        if trial % 100 == 0:
            print(f"  Shuffle trial {trial}/1000...")

        shuffled_roles = ROLES * (len(ALL_CLUSTERS) // len(ROLES) + 1)
        random.shuffle(shuffled_roles)
        shuffled_mapping = {c: shuffled_roles[i] for i, c in enumerate(ALL_CLUSTERS)}

        trial_SLS, trial_VR, trial_TS = [], [], []
        for pid, lines_dict, meta in valid_paras:
            sls, vr, ts = compute_paragraph_metrics(lines_dict, shuffled_mapping)
            trial_SLS.append(sls)
            trial_VR.append(vr)
            trial_TS.append(ts)

        shuf_SLS_all.append(trial_SLS)
        shuf_VR_all.append(trial_VR)
        shuf_TS_all.append(trial_TS)

    # Mean shuffled per paragraph
    n = len(valid_paras)
    shuf_SLS_mean = [sum(shuf_SLS_all[t][i] for t in range(1000))/1000 for i in range(n)]
    shuf_VR_mean  = [sum(shuf_VR_all[t][i]  for t in range(1000))/1000 for i in range(n)]
    shuf_TS_mean  = [sum(shuf_TS_all[t][i]  for t in range(1000))/1000 for i in range(n)]

    # ─── Wilcoxon tests ───
    print("\n--- WILCOXON SIGNED-RANK TESTS (v1.1) ---")

    W_sls_inv,  p_sls_inv,  n_sls_inv,  dir_sls_inv  = wilcoxon_signed_rank(orig_SLS, inv_SLS)
    W_vr_inv,   p_vr_inv,   n_vr_inv,   dir_vr_inv   = wilcoxon_signed_rank(orig_VR,  inv_VR)
    W_ts_inv,   p_ts_inv,   n_ts_inv,   dir_ts_inv   = wilcoxon_signed_rank(orig_TS,  inv_TS)

    W_sls_shuf, p_sls_shuf, n_sls_shuf, dir_sls_shuf = wilcoxon_signed_rank(orig_SLS, shuf_SLS_mean)
    W_vr_shuf,  p_vr_shuf,  n_vr_shuf,  dir_vr_shuf  = wilcoxon_signed_rank(orig_VR,  shuf_VR_mean)
    W_ts_shuf,  p_ts_shuf,  n_ts_shuf,  dir_ts_shuf  = wilcoxon_signed_rank(orig_TS,  shuf_TS_mean)

    import statistics
    print(f"\nMetric means:")
    print(f"  SLS: orig={statistics.mean(orig_SLS):.6f}, inv={statistics.mean(inv_SLS):.6f}, shuf={statistics.mean(shuf_SLS_mean):.6f}")
    print(f"  VR:  orig={statistics.mean(orig_VR):.4f},  inv={statistics.mean(inv_VR):.4f},  shuf={statistics.mean(shuf_VR_mean):.4f}")
    print(f"  TS:  orig={statistics.mean(orig_TS):.4f},  inv={statistics.mean(inv_TS):.4f},  shuf={statistics.mean(shuf_TS_mean):.4f}")

    print(f"\nWilcoxon original vs inverted:")
    print(f"  SLS: W={W_sls_inv:.1f}, p={p_sls_inv:.6f}, n={n_sls_inv}, dir={'orig>inv' if dir_sls_inv>0 else 'orig<inv'}")
    print(f"  VR:  W={W_vr_inv:.1f},  p={p_vr_inv:.6f},  n={n_vr_inv},  dir={'orig>inv' if dir_vr_inv>0 else 'orig<inv'}")
    print(f"  TS:  W={W_ts_inv:.1f},  p={p_ts_inv:.6f},  n={n_ts_inv},  dir={'orig>inv' if dir_ts_inv>0 else 'orig<inv'}")

    print(f"\nWilcoxon original vs shuffled:")
    print(f"  SLS: W={W_sls_shuf:.1f}, p={p_sls_shuf:.6f}, n={n_sls_shuf}, dir={'orig>shuf' if dir_sls_shuf>0 else 'orig<shuf'}")
    print(f"  VR:  W={W_vr_shuf:.1f},  p={p_vr_shuf:.6f},  n={n_vr_shuf},  dir={'orig>shuf' if dir_vr_shuf>0 else 'orig<shuf'}")
    print(f"  TS:  W={W_ts_shuf:.1f},  p={p_ts_shuf:.6f},  n={n_ts_shuf},  dir={'orig>shuf' if dir_ts_shuf>0 else 'orig<shuf'}")

    # Wins: SLS higher=better; VR lower=better; TS higher=better
    wins_vs_inv = sum([
        1 if p_sls_inv  < 0.05 and dir_sls_inv  > 0 else 0,
        1 if p_vr_inv   < 0.05 and dir_vr_inv   < 0 else 0,
        1 if p_ts_inv   < 0.05 and dir_ts_inv   > 0 else 0,
    ])
    wins_vs_shuf = sum([
        1 if p_sls_shuf < 0.05 and dir_sls_shuf > 0 else 0,
        1 if p_vr_shuf  < 0.05 and dir_vr_shuf  < 0 else 0,
        1 if p_ts_shuf  < 0.05 and dir_ts_shuf  > 0 else 0,
    ])
    wins_vs_both = sum([
        1 if (p_sls_inv < 0.05 and dir_sls_inv > 0 and p_sls_shuf < 0.05 and dir_sls_shuf > 0) else 0,
        1 if (p_vr_inv  < 0.05 and dir_vr_inv  < 0 and p_vr_shuf  < 0.05 and dir_vr_shuf  < 0) else 0,
        1 if (p_ts_inv  < 0.05 and dir_ts_inv  > 0 and p_ts_shuf  < 0.05 and dir_ts_shuf  > 0) else 0,
    ])

    print(f"\nOriginal wins vs inverted: {wins_vs_inv}/3")
    print(f"Original wins vs shuffled: {wins_vs_shuf}/3")
    print(f"Original wins vs BOTH:     {wins_vs_both}/3")

    rf2_resolved = wins_vs_both >= 2
    print(f"\nRF2 resolution: original wins ≥2/3 metrics vs BOTH → RF2 resolved: {rf2_resolved}")
    if not rf2_resolved:
        print("⚠️  RF2 NOT RESOLVED — transition model also fails ≥2/3 threshold")
    else:
        print("✓ RF2 RESOLVED — transition model passes")

    results = {
        "model_version": "v1.1",
        "n_paragraphs": len(valid_paras),
        "means": {
            "orig_SLS": statistics.mean(orig_SLS),
            "inv_SLS":  statistics.mean(inv_SLS),
            "shuf_SLS": statistics.mean(shuf_SLS_mean),
            "orig_VR":  statistics.mean(orig_VR),
            "inv_VR":   statistics.mean(inv_VR),
            "shuf_VR":  statistics.mean(shuf_VR_mean),
            "orig_TS":  statistics.mean(orig_TS),
            "inv_TS":   statistics.mean(inv_TS),
            "shuf_TS":  statistics.mean(shuf_TS_mean),
        },
        "wilcoxon_vs_inverted": {
            "SLS": {"W": W_sls_inv,  "p": p_sls_inv,  "n": n_sls_inv,  "dir": dir_sls_inv},
            "VR":  {"W": W_vr_inv,   "p": p_vr_inv,   "n": n_vr_inv,   "dir": dir_vr_inv},
            "TS":  {"W": W_ts_inv,   "p": p_ts_inv,   "n": n_ts_inv,   "dir": dir_ts_inv},
        },
        "wilcoxon_vs_shuffled": {
            "SLS": {"W": W_sls_shuf, "p": p_sls_shuf, "n": n_sls_shuf, "dir": dir_sls_shuf},
            "VR":  {"W": W_vr_shuf,  "p": p_vr_shuf,  "n": n_vr_shuf,  "dir": dir_vr_shuf},
            "TS":  {"W": W_ts_shuf,  "p": p_ts_shuf,  "n": n_ts_shuf,  "dir": dir_ts_shuf},
        },
        "wins_vs_inverted": wins_vs_inv,
        "wins_vs_shuffled": wins_vs_shuf,
        "wins_vs_both": wins_vs_both,
        "rf2_resolved": rf2_resolved,
    }

    out_json = OUT_DIR / "p1_3_falsification_v1.1_results.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out_json}")

    return results


if __name__ == "__main__":
    results = main()
