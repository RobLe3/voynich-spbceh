#!/usr/bin/env python3
"""
P1.1: Full corpus cluster frequency count with positional bias analysis.
P1.6: Markov 7x7 role bigram transition matrix.
P1.2: Section-specific role frequency profiles.

For each of 47 SPBCEH clusters:
  - Total occurrences
  - Line-initial %, line-medial %, line-final % with 95% Wilson CIs
  - Chi-squared test vs uniform positional distribution
"""

import csv
import json
import math
from collections import defaultdict, Counter
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
D1_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "results"
OUT_DIR.mkdir(exist_ok=True)

# ──────────────────────────────────────────────────────────
# 47 SPBCEH Canonical Clusters (role → cluster list)
# Sourced from: CLAUDE.md, artifacts/clue3.md, artifacts/clue4.md
# ──────────────────────────────────────────────────────────
SPBCEH_CLUSTERS = {
    "INIT": [
        # Initiator clusters — expected >65% line-initial
        "qokeedy",   # primary initiator
        "qokeey",    # common variant
        "qokedy",    # focused perception initiator
        "qokaiin",   # re-entry initiator
        "qokai!n",   # illegible variant of qokaiin
        "qokar",     # variant
        "qokol",     # variant
        "qoky",      # minimal form
        "qokal",     # variant
        "qokey",     # variant
        "fachys",    # alternate initiator (f1r first word)
    ],
    "CLOSE": [
        # Closure clusters — expected >65% line-final
        "chedy",     # primary closure
        "shedy",     # emotional closure
        "chey",      # short closure
        "shey",      # short emotional closure
        "cfhaiin",   # compound closure
        "ykchdy",    # recursive closure
        "cheey",     # elongated closure
        "sheey",     # elongated emotional closure
        "chdy",      # minimal closure
        "lchedy",    # prefixed closure
    ],
    "LINK": [
        # Link/transition clusters — expected >70% medial
        "okaiin",    # primary link
        "okeey",     # link variant
        "otar",      # temporal modifier
        "otedy",     # affect transfer
        "oteey",     # variant
        "okar",      # link variant
        "okal",      # link variant
    ],
    "ACT": [
        # Action/pulse clusters — rhythmic recurrence
        "daiin",     # primary ACT pulse
        "dain",      # short form
        "dai!n",     # illegible variant
        "dar",       # pulse variant
        "dal",       # pulse variant
        "dol",       # pulse variant
    ],
    "MODE": [
        # Mode/state clusters — section-differential
        "shol",      # emotional state
        "chol",      # emotional state
        "shor",      # mode variant
        "chor",      # mode variant
        "cheol",     # compound mode
        "sheol",     # compound emotional mode
    ],
    "TIME": [
        # Temporal clusters — flexible position, pairs/triplets
        "aiin",      # primary temporal
        "aiiin",     # elongated temporal
        "saiin",     # prefixed temporal
        "otaiin",    # prefixed temporal
    ],
    "REF": [
        # Reference clusters — high frequency, domain-neutral
        "ol",        # primary reference
        "or",        # alternate reference
        "al",        # reference
    ],
}

# Flatten: cluster → role (no overlaps)
CLUSTER_TO_ROLE = {}
for role, clusters in SPBCEH_CLUSTERS.items():
    for cluster in clusters:
        CLUSTER_TO_ROLE[cluster] = role

# All 47 clusters in order
ALL_CLUSTERS = []
for role in ["INIT", "CLOSE", "LINK", "ACT", "MODE", "TIME", "REF"]:
    ALL_CLUSTERS.extend(SPBCEH_CLUSTERS[role])

print(f"Total clusters defined: {len(ALL_CLUSTERS)}")
assert len(ALL_CLUSTERS) == 47, f"Expected 47 clusters, got {len(ALL_CLUSTERS)}"

# ──────────────────────────────────────────────────────────
# Wilson confidence interval for proportion
# ──────────────────────────────────────────────────────────
def wilson_ci(k, n, z=1.96):
    """95% Wilson CI for proportion k/n."""
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return p, max(0, center - margin), min(1, center + margin)


def kruskal_wallis(groups):
    """Kruskal-Wallis H-test for k independent samples (stdlib-only).
    groups: list of lists of numeric values.
    Returns: (H, p, k, N)
    """
    k = len(groups)
    ns = [len(g) for g in groups]
    N = sum(ns)
    if N == 0 or k < 2:
        return 0.0, 1.0, k, N
    # Build flat list with group identity preserved
    all_obs = []
    for gi, g in enumerate(groups):
        for v in g:
            all_obs.append((v, gi))
    all_obs_sorted = sorted(all_obs, key=lambda x: x[0])
    # Assign averaged ranks for tied values
    ranks_by_group = [0.0] * k
    i = 0
    while i < N:
        j = i
        while j < N and all_obs_sorted[j][0] == all_obs_sorted[i][0]:
            j += 1
        avg_rank = (i + j + 1) / 2.0  # 1-indexed average rank
        for idx in range(i, j):
            ranks_by_group[all_obs_sorted[idx][1]] += avg_rank
        i = j
    H = 12.0 / (N * (N + 1)) * sum(
        ranks_by_group[gi] ** 2 / ns[gi] for gi in range(k) if ns[gi] > 0
    ) - 3 * (N + 1)
    p = chi2_sf(H, k - 1)
    return H, p, k, N


def chi2_uniform(counts):
    """Chi-squared test for 3 positional categories vs uniform distribution.
    counts = [initial_count, medial_count, final_count] (or more)
    Returns (chi2, p, df)
    """
    total = sum(counts)
    if total == 0:
        return 0.0, 1.0, len(counts) - 1
    k = len(counts)
    expected = total / k
    chi2 = sum((c - expected) ** 2 / expected for c in counts)
    df = k - 1
    # p-value using chi2 distribution
    p = chi2_sf(chi2, df)
    return chi2, p, df


def chi2_sf(x, df):
    """Survival function (upper tail) of chi-squared distribution."""
    if x <= 0:
        return 1.0
    a = df / 2.0
    x2 = x / 2.0
    return 1.0 - _regularized_lower_gamma(a, x2)


def _regularized_lower_gamma(a, x):
    if x < 0:
        return 0.0
    if x == 0:
        return 0.0
    if x < a + 1:
        return _gamma_series(a, x)
    else:
        return 1.0 - _gamma_cf(a, x)


def _gamma_series(a, x):
    MAX_ITER = 200
    EPS = 1e-12
    ap = a
    delta = 1.0 / a
    total = delta
    for _ in range(MAX_ITER):
        ap += 1
        delta *= x / ap
        total += delta
        if abs(delta) < abs(total) * EPS:
            break
    return total * math.exp(-x + a * math.log(x) - _log_gamma(a))


def _gamma_cf(a, x):
    MAX_ITER = 200
    EPS = 1e-12
    FPMIN = 1e-300
    b = x + 1.0 - a
    c = 1.0 / FPMIN
    d = 1.0 / b
    h = d
    for i in range(1, MAX_ITER + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < FPMIN:
            d = FPMIN
        c = b + an / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    return math.exp(-x + a * math.log(x) - _log_gamma(a)) * h


def _log_gamma(x):
    g = 7
    c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
         771.32342877765313, -176.61502916214059, 12.507343278686905,
         -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
    if x < 0.5:
        return math.log(math.pi) - math.log(abs(math.sin(math.pi * x))) - _log_gamma(1 - x)
    x -= 1
    a = c[0]
    t = x + g + 0.5
    for i in range(1, g + 2):
        a += c[i] / (x + i)
    return 0.5 * math.log(2 * math.pi) + (x + 0.5) * math.log(t) - t + math.log(a)


# ──────────────────────────────────────────────────────────
# Load token data
# ──────────────────────────────────────────────────────────
def load_tokens():
    tokens = []
    with open(D1_DIR / "corpus_tokens.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tokens.append(row)
    return tokens


# ──────────────────────────────────────────────────────────
# P1.1: Cluster frequency & positional bias
# ──────────────────────────────────────────────────────────
def run_p1_1(tokens):
    print("\n" + "="*70)
    print("P1.1: CLUSTER FREQUENCY & POSITIONAL BIAS")
    print("="*70)

    # Count per cluster: total, initial, medial, final, only (single-token line)
    cluster_pos = defaultdict(lambda: Counter())
    for row in tokens:
        tok = row["token"]
        pos = row["position"]
        if tok in CLUSTER_TO_ROLE:
            cluster_pos[tok][pos] += 1

    results = []
    for cluster in ALL_CLUSTERS:
        role = CLUSTER_TO_ROLE[cluster]
        counts = cluster_pos[cluster]
        n_initial = counts.get("initial", 0)
        n_medial = counts.get("medial", 0)
        n_final = counts.get("final", 0)
        n_only = counts.get("only", 0)  # single-token lines
        n_total = n_initial + n_medial + n_final + n_only

        # For positional analysis, "initial" includes "only" (single-token line is both initial and final)
        n_init_effective = n_initial + n_only
        n_final_effective = n_final + n_only
        n_pos_total = n_total  # denominator for positional %

        if n_total == 0:
            results.append({
                "cluster": cluster, "role": role,
                "n_total": 0, "n_initial": 0, "n_medial": 0, "n_final": 0, "n_only": 0,
                "pct_initial": 0, "ci_init_lo": 0, "ci_init_hi": 0,
                "pct_medial": 0, "ci_med_lo": 0, "ci_med_hi": 0,
                "pct_final": 0, "ci_fin_lo": 0, "ci_fin_hi": 0,
                "chi2": 0, "p_chi2": 1.0, "df": 2,
            })
            continue

        p_init, ci_init_lo, ci_init_hi = wilson_ci(n_init_effective, n_pos_total)
        p_med, ci_med_lo, ci_med_hi = wilson_ci(n_medial, n_pos_total)
        p_fin, ci_fin_lo, ci_fin_hi = wilson_ci(n_final_effective, n_pos_total)

        # Chi-squared: use initial, medial, final counts (not "only")
        chi2, p_chi2, df = chi2_uniform([n_initial, n_medial, n_final + n_only])

        results.append({
            "cluster": cluster, "role": role,
            "n_total": n_total,
            "n_initial": n_initial, "n_medial": n_medial, "n_final": n_final, "n_only": n_only,
            "pct_initial": p_init, "ci_init_lo": ci_init_lo, "ci_init_hi": ci_init_hi,
            "pct_medial": p_med, "ci_med_lo": ci_med_lo, "ci_med_hi": ci_med_hi,
            "pct_final": p_fin, "ci_fin_lo": ci_fin_lo, "ci_fin_hi": ci_fin_hi,
            "chi2": chi2, "p_chi2": p_chi2, "df": df,
        })

    # Print results
    print(f"\n{'Cluster':12} {'Role':6} {'N':6} {'%Init':7} {'[CI]':15} {'%Med':7} {'%Fin':7} {'[CI]':15} {'chi2':8} {'p':8} {'sig':4}")
    print("-" * 100)
    for r in results:
        if r["n_total"] == 0:
            continue
        sig = "***" if r["p_chi2"] < 0.001 else ("**" if r["p_chi2"] < 0.01 else ("*" if r["p_chi2"] < 0.05 else "ns"))
        print(f"{r['cluster']:12} {r['role']:6} {r['n_total']:6d} "
              f"{r['pct_initial']:7.3f} [{r['ci_init_lo']:.3f},{r['ci_init_hi']:.3f}] "
              f"{r['pct_medial']:7.3f} {r['pct_final']:7.3f} "
              f"[{r['ci_fin_lo']:.3f},{r['ci_fin_hi']:.3f}] "
              f"{r['chi2']:8.3f} {r['p_chi2']:8.4f} {sig:4}")

    # Check SPBCEH predictions
    print("\n--- SPBCEH PREDICTION CHECK ---")
    print("INIT clusters: expected >65% line-initial")
    for r in results:
        if r["role"] == "INIT" and r["n_total"] > 0:
            passes = r["pct_initial"] > 0.65
            print(f"  {r['cluster']:12}: {r['pct_initial']:.3f} {'✓' if passes else '✗'} (n={r['n_total']})")

    print("CLOSE clusters: expected >65% line-final")
    for r in results:
        if r["role"] == "CLOSE" and r["n_total"] > 0:
            passes = r["pct_final"] > 0.65
            print(f"  {r['cluster']:12}: {r['pct_final']:.3f} {'✓' if passes else '✗'} (n={r['n_total']})")

    print("LINK clusters: expected >70% medial")
    for r in results:
        if r["role"] == "LINK" and r["n_total"] > 0:
            passes = r["pct_medial"] > 0.70
            print(f"  {r['cluster']:12}: {r['pct_medial']:.3f} {'✓' if passes else '✗'} (n={r['n_total']})")

    # Save to CSV
    out_csv = OUT_DIR / "p1_1_cluster_frequencies.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    print(f"\nSaved: {out_csv}")

    return results


# ──────────────────────────────────────────────────────────
# P1.6: Markov 7x7 role bigram transition matrix
# ──────────────────────────────────────────────────────────
def run_p1_6(tokens):
    print("\n" + "="*70)
    print("P1.6: MARKOV 7×7 ROLE BIGRAM TRANSITION MATRIX")
    print("="*70)

    ROLES = ["INIT", "CLOSE", "LINK", "ACT", "MODE", "TIME", "REF"]

    # Assign role to each token
    # Build per-line role sequences
    line_sequences = defaultdict(list)
    for row in tokens:
        role = CLUSTER_TO_ROLE.get(row["token"])
        if role:
            line_sequences[row["line_id"]].append({
                "role": role, "position": row["position"],
                "token_index": int(row["token_index"]),
            })

    # Sort each line by token_index and extract role sequence
    transitions = Counter()  # (from_role, to_role) -> count
    total_bigrams = 0
    for line_id, toks in line_sequences.items():
        toks_sorted = sorted(toks, key=lambda x: x["token_index"])
        roles = [t["role"] for t in toks_sorted]
        for i in range(len(roles) - 1):
            transitions[(roles[i], roles[i + 1])] += 1
            total_bigrams += 1

    print(f"\nTotal role bigrams: {total_bigrams}")

    # Build 7x7 count matrix
    matrix = {}
    for from_role in ROLES:
        matrix[from_role] = {}
        for to_role in ROLES:
            matrix[from_role][to_role] = transitions.get((from_role, to_role), 0)

    # Print count matrix
    print(f"\nBigram count matrix (FROM → TO):")
    header = f"{'':8}" + "".join(f"{r:7}" for r in ROLES)
    print(header)
    for from_role in ROLES:
        row_counts = [matrix[from_role][to_role] for to_role in ROLES]
        row_total = sum(row_counts)
        row_str = f"{from_role:8}" + "".join(f"{c:7d}" for c in row_counts)
        print(row_str + f"  [n={row_total}]")

    # Transition probability matrix (row-normalized)
    print(f"\nTransition probability matrix (row-normalized):")
    print(header)
    prob_matrix = {}
    for from_role in ROLES:
        row_total = sum(matrix[from_role][to_role] for to_role in ROLES)
        prob_matrix[from_role] = {}
        row_probs = []
        for to_role in ROLES:
            p = matrix[from_role][to_role] / row_total if row_total > 0 else 0.0
            prob_matrix[from_role][to_role] = p
            row_probs.append(p)
        row_str = f"{from_role:8}" + "".join(f"{p:7.3f}" for p in row_probs)
        print(row_str)

    # Shuffled baseline: 1000 permutations
    print(f"\nComputing shuffled baseline (1000 permutations)...")
    import random
    random.seed(42)

    # Collect all role sequences for shuffling
    all_line_roles = []
    for line_id, toks in line_sequences.items():
        toks_sorted = sorted(toks, key=lambda x: x["token_index"])
        roles = [t["role"] for t in toks_sorted]
        if len(roles) >= 2:
            all_line_roles.append(roles)

    # Shuffle within each line 1000 times and collect mean bigram counts
    shuffle_bigrams = defaultdict(list)
    for trial in range(1000):
        trial_transitions = Counter()
        for roles in all_line_roles:
            shuffled = roles[:]
            random.shuffle(shuffled)
            for i in range(len(shuffled) - 1):
                trial_transitions[(shuffled[i], shuffled[i + 1])] += 1
        for from_role in ROLES:
            for to_role in ROLES:
                shuffle_bigrams[(from_role, to_role)].append(
                    trial_transitions.get((from_role, to_role), 0)
                )

    # Compute z-scores
    print("\nZ-scores vs shuffled baseline (observed - expected) / std:")
    print(header)
    zscores = {}
    for from_role in ROLES:
        row_z = []
        zscores[from_role] = {}
        for to_role in ROLES:
            observed = transitions.get((from_role, to_role), 0)
            shuffled = shuffle_bigrams[(from_role, to_role)]
            mean_shuf = sum(shuffled) / len(shuffled)
            std_shuf = (sum((x - mean_shuf)**2 for x in shuffled) / len(shuffled)) ** 0.5
            z = (observed - mean_shuf) / std_shuf if std_shuf > 0 else 0.0
            row_z.append(z)
            zscores[from_role][to_role] = {
                "observed": observed, "mean_shuffled": mean_shuf,
                "std_shuffled": std_shuf, "z": z
            }
        row_str = f"{from_role:8}" + "".join(f"{z:7.2f}" for z in row_z)
        print(row_str)

    # Save results
    out_json = OUT_DIR / "p1_6_transition_matrix.json"
    with open(out_json, "w") as f:
        json.dump({
            "roles": ROLES,
            "total_bigrams": total_bigrams,
            "count_matrix": matrix,
            "prob_matrix": prob_matrix,
            "zscores": zscores,
        }, f, indent=2)
    print(f"\nSaved: {out_json}")

    return matrix, prob_matrix, zscores


# ──────────────────────────────────────────────────────────
# P1.2: Section role profiles
# ──────────────────────────────────────────────────────────
def run_p1_2(tokens):
    print("\n" + "="*70)
    print("P1.2: SECTION ROLE FREQUENCY PROFILES")
    print("="*70)

    ROLES = ["INIT", "CLOSE", "LINK", "ACT", "MODE", "TIME", "REF"]
    SECTIONS = ["H", "S", "B", "P", "C", "T", "Z", "A"]
    SECTION_LABELS = {
        "H": "Herbal", "S": "Stars/Recipes", "B": "Biological",
        "P": "Pharmaceutical", "C": "Cosmological", "T": "Text-only",
        "Z": "Zodiac", "A": "Astrological",
    }

    # Per-folio role frequency vectors
    folio_data = defaultdict(lambda: {"section": "?", "total": 0, "roles": Counter()})
    for row in tokens:
        fid = row["folio_id"]
        folio_data[fid]["section"] = row["section"]
        folio_data[fid]["total"] += 1
        role = CLUSTER_TO_ROLE.get(row["token"])
        if role:
            folio_data[fid]["roles"][role] += 1

    # Per-folio normalized frequency vectors
    folio_profiles = []
    for fid, data in folio_data.items():
        total = data["total"]
        if total == 0:
            continue
        profile = {"folio_id": fid, "section": data["section"], "n_tokens": total}
        for role in ROLES:
            profile[f"freq_{role}"] = data["roles"].get(role, 0) / total
        folio_profiles.append(profile)

    # Compute section means and ANOVA
    import statistics

    print(f"\n{'Section':8} {'N_folios':9} " + " ".join(f"{'mean_'+r:12}" for r in ROLES))
    section_data = {}
    for sec in SECTIONS:
        sec_profiles = [p for p in folio_profiles if p["section"] == sec]
        if not sec_profiles:
            continue
        section_data[sec] = {
            "n": len(sec_profiles),
            "means": {},
            "stds": {},
            "values": {},
        }
        row_str = f"{sec:8} {len(sec_profiles):9}"
        for role in ROLES:
            vals = [p[f"freq_{role}"] for p in sec_profiles]
            mean = statistics.mean(vals)
            std = statistics.stdev(vals) if len(vals) > 1 else 0.0
            section_data[sec]["means"][role] = mean
            section_data[sec]["stds"][role] = std
            section_data[sec]["values"][role] = vals
            row_str += f" {mean:12.5f}"
        print(row_str + f"  ({SECTION_LABELS.get(sec, sec)})")

    # Kruskal-Wallis across all 8 sections for each role
    print("\n--- Kruskal-Wallis: role frequency variation across sections ---")
    kw_results = {}
    for role in ROLES:
        groups = []
        for sec in SECTIONS:
            if sec in section_data:
                vals = section_data[sec]["values"][role]
                if len(vals) >= 2:
                    groups.append(vals)
        if len(groups) < 2:
            continue
        H, p, k, n = kruskal_wallis(groups)
        sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
        print(f"  {role}: H={H:.3f}, p={p:.4f} {sig}  (k={k} sections, n={n} folios)")
        kw_results[role] = {"H": H, "p": p, "sig": sig, "k": k, "n": n}

    # Save section profiles CSV
    out_csv = OUT_DIR / "p1_2_section_profiles.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["folio_id", "section", "n_tokens"] + [f"freq_{r}" for r in ROLES]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(folio_profiles)
    print(f"\nSaved: {out_csv}")

    # Save heatmap data JSON
    heatmap = {}
    for sec in SECTIONS:
        if sec in section_data:
            heatmap[sec] = {
                "n_folios": section_data[sec]["n"],
                "means": section_data[sec]["means"],
                "stds": section_data[sec]["stds"],
            }
    out_json = OUT_DIR / "p1_2_heatmap_data.json"
    with open(out_json, "w") as f:
        json.dump({"heatmap": heatmap, "kw_results": kw_results}, f, indent=2)
    print(f"Saved: {out_json}")

    return section_data, kw_results


if __name__ == "__main__":
    tokens = load_tokens()
    print(f"Loaded {len(tokens)} tokens")

    # P1.1
    p1_1_results = run_p1_1(tokens)

    # P1.6
    count_matrix, prob_matrix, zscores = run_p1_6(tokens)

    # P1.2
    section_data, kw_results = run_p1_2(tokens)

    print("\n" + "="*70)
    print("ALL P1.1, P1.6, P1.2 ANALYSES COMPLETE")
    print("="*70)
