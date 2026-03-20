#!/usr/bin/env python3
"""
P2.5 v2.0 — Anti-Projection Test with 6-role model (ACT+MODE merged into CONTENT)
Also computes: P1.2/P1.3/P1.4/P1.6 equivalents under the 6-role model.
"""

import csv
import json
import math
import random
from collections import defaultdict, Counter
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).parent.parent
D1_DIR = BASE_DIR / "data"
P1_DIR = BASE_DIR / "results"
OUT_DIR = BASE_DIR / "results"

# ──────────────────────────────────────────────────────────
# 6-Role Model v2.0: ACT + MODE merged into CONTENT
# ──────────────────────────────────────────────────────────
SPBCEH_6ROLE = {
    "INIT":    ["qokeedy","qokeey","qokedy","qokaiin","qokai!n","qokar","qokol","qoky","qokal","qokey","fachys"],
    "CLOSE":   ["chedy","shedy","chey","shey","cfhaiin","ykchdy","cheey","sheey","chdy","lchedy"],
    "LINK":    ["okaiin","okeey","otar","otedy","oteey","okar","okal"],
    "CONTENT": ["daiin","dain","dai!n","dar","dal","dol",    # former ACT
                 "shol","chol","shor","chor","cheol","sheol"], # former MODE
    "TIME":    ["aiin","aiiin","saiin","otaiin"],
    "REF":     ["ol","or","al"],
}

CLUSTER_TO_6ROLE = {}
for role, clusters in SPBCEH_6ROLE.items():
    for c in clusters:
        CLUSTER_TO_6ROLE[c] = role

# Original 7-role mapping (for comparison)
SPBCEH_7ROLE = {
    "INIT":    ["qokeedy","qokeey","qokedy","qokaiin","qokai!n","qokar","qokol","qoky","qokal","qokey","fachys"],
    "CLOSE":   ["chedy","shedy","chey","shey","cfhaiin","ykchdy","cheey","sheey","chdy","lchedy"],
    "LINK":    ["okaiin","okeey","otar","otedy","oteey","okar","okal"],
    "ACT":     ["daiin","dain","dai!n","dar","dal","dol"],
    "MODE":    ["shol","chol","shor","chor","cheol","sheol"],
    "TIME":    ["aiin","aiiin","saiin","otaiin"],
    "REF":     ["ol","or","al"],
}
CLUSTER_TO_7ROLE = {}
for role, clusters in SPBCEH_7ROLE.items():
    for c in clusters:
        CLUSTER_TO_7ROLE[c] = role

ROLES_6 = ["INIT","CLOSE","LINK","CONTENT","TIME","REF"]
ALL_CLUSTERS_6 = []
for role in ROLES_6:
    ALL_CLUSTERS_6.extend(SPBCEH_6ROLE[role])

print(f"6-role model: {len(ALL_CLUSTERS_6)} clusters across {len(ROLES_6)} roles")

# ──────────────────────────────────────────────────────────
# Load corpus
# ──────────────────────────────────────────────────────────
print("Loading corpus...")
lines_data = []
with open(D1_DIR / "corpus_lines.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tokens = row["tokens"].split() if row["tokens"] else []
        lines_data.append({
            "folio_id": row["folio_id"],
            "line_id": row["line_id"],
            "section": row["section"],
            "currier": row["currier"],
            "paragraph_id": int(row["paragraph_id"]),
            "tokens": tokens,
        })
print(f"  Lines: {len(lines_data)}")

# ──────────────────────────────────────────────────────────
# Shared scoring functions
# ──────────────────────────────────────────────────────────
def shannon_entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return sum(-c/total * math.log2(c/total) for c in counts.values() if c > 0)

def compute_mapping_scores(cluster_to_role_map, lines_data_in, n_shuffle=200):
    # n_shuffle=200 (increased from 50 for Markov structure stability)
    """Score a mapping on TS, classification accuracy, Markov structure."""
    all_roles = sorted(set(cluster_to_role_map.values()))

    # Build role sequences
    mapped_lines = []
    for line in lines_data_in:
        r_seq = [cluster_to_role_map.get(t) for t in line["tokens"] if cluster_to_role_map.get(t)]
        mapped_lines.append({
            "folio_id": line["folio_id"],
            "section": line["section"],
            "role_seq": r_seq,
        })

    # Transition matrix (Laplace smoothed)
    bigrams = defaultdict(lambda: defaultdict(int))
    role_totals = defaultdict(int)
    for ml in mapped_lines:
        rseq = ml["role_seq"]
        for i in range(len(rseq)-1):
            bigrams[rseq[i]][rseq[i+1]] += 1
            role_totals[rseq[i]] += 1

    K = len(all_roles)
    trans_probs = {}
    for r1 in all_roles:
        total = role_totals[r1] + K
        trans_probs[r1] = {r2: (bigrams[r1][r2]+1)/total for r2 in all_roles}

    # TS: log-prob
    log_prob_sum = 0.0
    n_bigrams = 0
    for ml in mapped_lines:
        rseq = ml["role_seq"]
        for i in range(len(rseq)-1):
            r1, r2 = rseq[i], rseq[i+1]
            lp = math.log(trans_probs.get(r1,{}).get(r2,1e-10))
            log_prob_sum += lp
            n_bigrams += 1
    ts_score = log_prob_sum / n_bigrams if n_bigrams > 0 else -999

    # Classification: 1-NN leave-one-folio-out
    folio_vecs = defaultdict(lambda: defaultdict(int))
    folio_sects = {}
    folio_tots = defaultdict(int)
    for ml in mapped_lines:
        fid = ml["folio_id"]
        folio_sects[fid] = ml["section"]
        for r in ml["role_seq"]:
            folio_vecs[fid][r] += 1
            folio_tots[fid] += 1

    folio_freq = {}
    for fid, counts in folio_vecs.items():
        tot = folio_tots[fid]
        folio_freq[fid] = {r: counts.get(r,0)/tot for r in all_roles}

    folios = list(folio_freq.keys())
    correct = 0
    for i, test_fid in enumerate(folios):
        tv = folio_freq[test_fid]
        ts = folio_sects[test_fid]
        best_sim, best_sec = -1, None
        for j, train_fid in enumerate(folios):
            if i == j: continue
            trv = folio_freq[train_fid]
            dot = sum(tv.get(r,0)*trv.get(r,0) for r in all_roles)
            n1 = math.sqrt(sum(v**2 for v in tv.values()))
            n2 = math.sqrt(sum(v**2 for v in trv.values()))
            sim = dot/(n1*n2) if n1*n2 > 0 else 0
            if sim > best_sim:
                best_sim = sim
                best_sec = folio_sects[train_fid]
        if best_sec == ts:
            correct += 1
    cls_acc = correct / len(folios) if folios else 0

    # Markov structure: mean |z| vs shuffled
    obs_counts = {(r1,r2): bigrams[r1][r2] for r1 in all_roles for r2 in all_roles}
    shuffled_counts = defaultdict(list)
    for _ in range(n_shuffle):
        sb = defaultdict(lambda: defaultdict(int))
        for ml in mapped_lines:
            rseq = list(ml["role_seq"])
            random.shuffle(rseq)
            for i in range(len(rseq)-1):
                sb[rseq[i]][rseq[i+1]] += 1
        for r1 in all_roles:
            for r2 in all_roles:
                shuffled_counts[(r1,r2)].append(sb[r1][r2])

    total_abs_z, n_cells = 0.0, 0
    for (r1,r2), sh_vals in shuffled_counts.items():
        obs = obs_counts.get((r1,r2),0)
        mean_sh = sum(sh_vals)/len(sh_vals)
        std_sh = math.sqrt(sum((v-mean_sh)**2 for v in sh_vals)/len(sh_vals))
        if std_sh > 0:
            total_abs_z += abs((obs-mean_sh)/std_sh)
            n_cells += 1
    markov_struct = total_abs_z/n_cells if n_cells > 0 else 0

    return {"ts_score": ts_score, "cls_accuracy": cls_acc, "markov_struct": markov_struct}

# ──────────────────────────────────────────────────────────
# P1.2 equivalent: Section profiles under 6-role model
# ──────────────────────────────────────────────────────────
print("\n=== B2a: Section profiles (6-role model) ===")

section_role_counts = defaultdict(lambda: defaultdict(int))
section_total = defaultdict(int)
for line in lines_data:
    s = line["section"]
    for t in line["tokens"]:
        r = CLUSTER_TO_6ROLE.get(t)
        if r:
            section_role_counts[s][r] += 1
            section_total[s] += 1

print("Section role frequencies (% of assigned tokens per section):")
for s in sorted(section_role_counts):
    tot = section_total[s]
    dist = {r: 100*section_role_counts[s][r]/tot for r in ROLES_6}
    print(f"  {s}: " + "  ".join(f"{r}={dist[r]:.1f}%" for r in ROLES_6))

# Kruskal-Wallis proxy: check if each role varies across sections
# Use per-folio frequencies for KW
folio_6role = defaultdict(lambda: defaultdict(int))
folio_totals_6 = defaultdict(int)
folio_sections_6 = {}
for line in lines_data:
    fid = line["folio_id"]
    folio_sections_6[fid] = line["section"]
    for t in line["tokens"]:
        r = CLUSTER_TO_6ROLE.get(t)
        if r:
            folio_6role[fid][r] += 1
            folio_totals_6[fid] += 1

# Simple variance ratio (between-section / within-section) as KW proxy
print("\nRole section-differentiation (variance ratio proxy):")
for role in ROLES_6:
    by_section = defaultdict(list)
    for fid, counts in folio_6role.items():
        tot = folio_totals_6[fid]
        if tot > 0:
            freq = counts.get(role, 0) / tot
            by_section[folio_sections_6[fid]].append(freq)

    section_means = {s: sum(v)/len(v) for s, v in by_section.items() if v}
    grand_mean = sum(sum(v) for v in by_section.values()) / sum(len(v) for v in by_section.values())

    between_var = sum(len(v)*(section_means[s]-grand_mean)**2
                      for s, v in by_section.items() if v)
    within_var = sum(sum((x-section_means[s])**2 for x in v)
                     for s, v in by_section.items() if v)

    ratio = between_var/within_var if within_var > 0 else 0
    print(f"  {role}: variance ratio = {ratio:.4f} (higher = more section-differentiated)")

# ──────────────────────────────────────────────────────────
# P1.6 equivalent: Markov transition matrix (6x6)
# ──────────────────────────────────────────────────────────
print("\n=== B2b: 6-role Markov transition matrix ===")

bigrams_6 = defaultdict(lambda: defaultdict(int))
for line in lines_data:
    roles = [CLUSTER_TO_6ROLE.get(t) for t in line["tokens"]]
    roles = [r for r in roles if r is not None]
    for i in range(len(roles)-1):
        bigrams_6[roles[i]][roles[i+1]] += 1

# Z-scores vs shuffled (200 permutations for accuracy)
print("Computing 6-role transition z-scores (200 shuffles)...")
shuffled_6 = defaultdict(list)
for _ in range(200):
    sb = defaultdict(lambda: defaultdict(int))
    for line in lines_data:
        roles = [CLUSTER_TO_6ROLE.get(t) for t in line["tokens"]]
        roles = [r for r in roles if r is not None]
        random.shuffle(roles)
        for i in range(len(roles)-1):
            sb[roles[i]][roles[i+1]] += 1
    for r1 in ROLES_6:
        for r2 in ROLES_6:
            shuffled_6[(r1,r2)].append(sb[r1][r2])

print("\n6-role Z-score matrix (FROM → TO):")
header = "From\\To".ljust(10) + "".join(r.ljust(10) for r in ROLES_6)
print(header)
close_init_z_6 = 0
for r1 in ROLES_6:
    row = r1.ljust(10)
    for r2 in ROLES_6:
        obs = bigrams_6[r1][r2]
        sh = shuffled_6[(r1,r2)]
        mean_sh = sum(sh)/len(sh)
        std_sh = math.sqrt(sum((v-mean_sh)**2 for v in sh)/len(sh))
        z = (obs-mean_sh)/std_sh if std_sh > 0 else 0
        if r1 == "CLOSE" and r2 == "INIT":
            close_init_z_6 = z
        marker = "*" if abs(z) >= 3 else " "
        row += f"{z:+.2f}{marker}".ljust(10)
    print(row)

print(f"\nCLOSE→INIT z-score (6-role): {close_init_z_6:.3f}")
print(f"CLOSE→INIT z-score (7-role was): +9.75")

# ──────────────────────────────────────────────────────────
# P1.3 equivalent: Falsification under 6-role model
# ──────────────────────────────────────────────────────────
print("\n=== B2c: Falsification test (6-role model) ===")

# Build role sequences
def build_role_sequences(cluster_map, lines_data_in):
    seqs = []
    for line in lines_data_in:
        rseq = [cluster_map.get(t) for t in line["tokens"]]
        rseq = [r for r in rseq if r is not None]
        seqs.append(rseq)
    return seqs

seqs_6 = build_role_sequences(CLUSTER_TO_6ROLE, lines_data)
seqs_6_inv = build_role_sequences({c: ("CLOSE" if r=="INIT" else "INIT" if r=="CLOSE" else r)
                                    for c, r in CLUSTER_TO_6ROLE.items()}, lines_data)

# TS (Transition Surprise) for original vs inverted
def compute_ts(seqs, n_roles_list):
    """Compute mean log-prob under own Markov model."""
    all_roles = n_roles_list
    K = len(all_roles)
    bigrams = defaultdict(lambda: defaultdict(int))
    role_tots = defaultdict(int)
    for rseq in seqs:
        for i in range(len(rseq)-1):
            bigrams[rseq[i]][rseq[i+1]] += 1
            role_tots[rseq[i]] += 1
    trans = {}
    for r1 in all_roles:
        total = role_tots[r1] + K
        trans[r1] = {r2: (bigrams[r1][r2]+1)/total for r2 in all_roles}
    log_sum, n = 0.0, 0
    for rseq in seqs:
        for i in range(len(rseq)-1):
            r1, r2 = rseq[i], rseq[i+1]
            log_sum += math.log(trans.get(r1,{}).get(r2,1e-10))
            n += 1
    return log_sum/n if n > 0 else -999

# Score inverted sequences under original model
def compute_ts_cross(train_seqs, test_seqs, all_roles):
    """Score test_seqs under Markov model trained on train_seqs."""
    K = len(all_roles)
    bigrams = defaultdict(lambda: defaultdict(int))
    role_tots = defaultdict(int)
    for rseq in train_seqs:
        for i in range(len(rseq)-1):
            bigrams[rseq[i]][rseq[i+1]] += 1
            role_tots[rseq[i]] += 1
    trans = {}
    for r1 in all_roles:
        total = role_tots[r1] + K
        trans[r1] = {r2: (bigrams[r1][r2]+1)/total for r2 in all_roles}
    log_sum, n = 0.0, 0
    for rseq in test_seqs:
        for i in range(len(rseq)-1):
            r1, r2 = rseq[i], rseq[i+1]
            log_sum += math.log(trans.get(r1,{}).get(r2,1e-10))
            n += 1
    return log_sum/n if n > 0 else -999

# Shuffled baseline for TS
shuffled_ts_6 = []
for _ in range(200):
    shuf_seqs = [list(s) for s in seqs_6]
    for s in shuf_seqs:
        random.shuffle(s)
    shuffled_ts_6.append(compute_ts(shuf_seqs, ROLES_6))

ts_orig_6 = compute_ts(seqs_6, ROLES_6)
ts_inv_6 = compute_ts(seqs_6_inv, ROLES_6)
mean_ts_sh = sum(shuffled_ts_6)/len(shuffled_ts_6)
std_ts_sh = math.sqrt(sum((v-mean_ts_sh)**2 for v in shuffled_ts_6)/len(shuffled_ts_6))

z_orig_vs_shuf = (ts_orig_6 - mean_ts_sh)/std_ts_sh if std_ts_sh > 0 else 0
z_inv_vs_orig = (ts_inv_6 - ts_orig_6)/std_ts_sh if std_ts_sh > 0 else 0

print(f"TS (6-role original): {ts_orig_6:.4f}")
print(f"TS (6-role inverted INIT↔CLOSE): {ts_inv_6:.4f}")
print(f"TS (shuffled mean): {mean_ts_sh:.4f}, std={std_ts_sh:.4f}")
print(f"Z(original vs shuffled): {z_orig_vs_shuf:.3f}")
print(f"Z(inverted vs original): {z_inv_vs_orig:.3f} ({'original wins' if ts_orig_6 > ts_inv_6 else 'inverted wins'})")

# SLS: Sequential Logic Score — count conformant bigrams (CLOSE→INIT is canonical)
# Under 6-role model: canonical transitions are {CLOSE→INIT, INIT→CONTENT, CONTENT→CONTENT, CONTENT→CLOSE}
CANONICAL_6 = {("CLOSE","INIT"), ("INIT","CONTENT"), ("CONTENT","CONTENT"),
               ("CONTENT","CLOSE"), ("CLOSE","CONTENT"), ("CONTENT","LINK"),
               ("CONTENT","TIME"), ("CONTENT","REF")}

def compute_sls(seqs, canonical):
    n_conform, n_total = 0, 0
    for rseq in seqs:
        for i in range(len(rseq)-1):
            pair = (rseq[i], rseq[i+1])
            if pair in canonical:
                n_conform += 1
            n_total += 1
    return n_conform/n_total if n_total > 0 else 0

sls_orig_6 = compute_sls(seqs_6, CANONICAL_6)
sls_inv_6 = compute_sls(seqs_6_inv, CANONICAL_6)

# Shuffled SLS
shuffled_sls_6 = []
for _ in range(200):
    shuf_seqs = [list(s) for s in seqs_6]
    for s in shuf_seqs:
        random.shuffle(s)
    shuffled_sls_6.append(compute_sls(shuf_seqs, CANONICAL_6))
mean_sls_sh = sum(shuffled_sls_6)/len(shuffled_sls_6)
std_sls_sh = math.sqrt(sum((v-mean_sls_sh)**2 for v in shuffled_sls_6)/len(shuffled_sls_6))

z_sls_orig = (sls_orig_6 - mean_sls_sh)/std_sls_sh if std_sls_sh > 0 else 0
z_sls_inv = (sls_inv_6 - mean_sls_sh)/std_sls_sh if std_sls_sh > 0 else 0

print(f"\nSLS (6-role original): {sls_orig_6:.4f} (z={z_sls_orig:.3f})")
print(f"SLS (6-role inverted): {sls_inv_6:.4f} (z={z_sls_inv:.3f})")

# P1.4 equivalent: Section classification with 6-role vectors
print("\n=== B2d: Section classification (6-role model) ===")
scores_6 = compute_mapping_scores(CLUSTER_TO_6ROLE, lines_data, n_shuffle=0)
print(f"6-role 1-NN classification accuracy: {scores_6['cls_accuracy']:.4f}")
print(f"(7-role was: 0.698)")

# ──────────────────────────────────────────────────────────
# P2.5 v2.0: Anti-Projection Test with 6-role model
# ──────────────────────────────────────────────────────────
print("\n=== P2.5 v2.0: Anti-Projection Test (6-role model) ===")

all_6_clusters = list(CLUSTER_TO_6ROLE.keys())
all_6_roles_flat = [CLUSTER_TO_6ROLE[c] for c in all_6_clusters]

all_mappings_6 = [("6ROLE_ORIGINAL", CLUSTER_TO_6ROLE)]

# 20 random permutations of 6-role labels
for i in range(20):
    shuffled = all_6_roles_flat.copy()
    random.shuffle(shuffled)
    all_mappings_6.append((f"RANDOM_{i+1:02d}", dict(zip(all_6_clusters, shuffled))))

# 10 hand-crafted alternatives
def swap_6(base_map, swaps):
    new_map = base_map.copy()
    for cluster, new_role in swaps:
        if cluster in new_map:
            new_map[cluster] = new_role
    return new_map

crafted_6 = [
    # Original 7-role mapping (as a challenger to the 6-role original)
    ("7ROLE_ORIGINAL", CLUSTER_TO_7ROLE),
    # Swap INIT and CLOSE
    ("CRAFT_SWAP_IC", {c: ("CLOSE" if r=="INIT" else "INIT" if r=="CLOSE" else r)
                       for c, r in CLUSTER_TO_6ROLE.items()}),
    # Move daiin from CONTENT to TIME
    ("CRAFT_daiin_TIME", swap_6(CLUSTER_TO_6ROLE, [("daiin","TIME")])),
    # Move LINK → CONTENT
    ("CRAFT_LINK_CONTENT", {c: ("CONTENT" if r=="LINK" else r)
                             for c, r in CLUSTER_TO_6ROLE.items()}),
    # Move chedy from CLOSE to CONTENT
    ("CRAFT_chedy_CONTENT", swap_6(CLUSTER_TO_6ROLE, [("chedy","CONTENT")])),
    # Move REF → LINK
    ("CRAFT_REF_LINK", {c: ("LINK" if r=="REF" else r)
                        for c, r in CLUSTER_TO_6ROLE.items()}),
    # Move all CLOSE → CONTENT
    ("CRAFT_CLOSE_CONTENT", {c: ("CONTENT" if r=="CLOSE" else r)
                              for c, r in CLUSTER_TO_6ROLE.items()}),
    # Merge TIME → CONTENT (5-role model)
    ("CRAFT_5ROLE_merge_TIME", {c: ("CONTENT" if r=="TIME" else r)
                                 for c, r in CLUSTER_TO_6ROLE.items()}),
    # Merge REF → CONTENT (5-role model alt)
    ("CRAFT_5ROLE_merge_REF", {c: ("CONTENT" if r=="REF" else r)
                                for c, r in CLUSTER_TO_6ROLE.items()}),
    # Split CONTENT back by daiin (put daiin-family in TIME)
    ("CRAFT_daiin_family_TIME", swap_6(CLUSTER_TO_6ROLE,
        [("daiin","TIME"),("dain","TIME"),("dai!n","TIME"),("dar","TIME"),("dal","TIME"),("dol","TIME")])),
]
all_mappings_6.extend(crafted_6)

print(f"Total mappings: {len(all_mappings_6)}")
print("Scoring all mappings...")

results_6 = []
for idx, (name, mapping) in enumerate(all_mappings_6):
    if idx % 5 == 0:
        print(f"  [{idx+1}/{len(all_mappings_6)}] {name}...")
    scores = compute_mapping_scores(mapping, lines_data, n_shuffle=200)
    results_6.append({
        "name": name,
        "is_original": name == "6ROLE_ORIGINAL",
        "ts_score": scores["ts_score"],
        "cls_accuracy": scores["cls_accuracy"],
        "markov_struct": scores["markov_struct"],
    })

def rank_all(results, metric, higher_is_better=True):
    sorted_r = sorted(results, key=lambda x: x[metric], reverse=higher_is_better)
    for rank, r in enumerate(sorted_r, 1):
        r[f"rank_{metric}"] = rank

rank_all(results_6, "ts_score")
rank_all(results_6, "cls_accuracy")
rank_all(results_6, "markov_struct")

orig_6 = next(r for r in results_6 if r["is_original"])

print(f"\n--- 6-Role Anti-Projection Results ---")
print(f"6-Role SPBCEH (CONTENT = merged ACT+MODE):")
print(f"  TS score: {orig_6['ts_score']:.4f}  Rank: {orig_6['rank_ts_score']}/{len(results_6)}")
print(f"  Classification: {orig_6['cls_accuracy']:.4f}  Rank: {orig_6['rank_cls_accuracy']}/{len(results_6)}")
print(f"  Markov structure: {orig_6['markov_struct']:.4f}  Rank: {orig_6['rank_markov_struct']}/{len(results_6)}")

top3_count_6 = sum(1 for m in ["rank_ts_score","rank_cls_accuracy","rank_markov_struct"]
                   if orig_6[m] <= 3)
top5_count_6 = sum(1 for m in ["rank_ts_score","rank_cls_accuracy","rank_markov_struct"]
                   if orig_6[m] <= 5)

verdict_6 = ("✅ PASSED" if top3_count_6 >= 2 else
             ("⚠️ PARTIAL" if top5_count_6 >= 2 else "❌ RF5b STILL TRIGGERED"))

print(f"\n  Top-3 on ≥2/3 metrics: {top3_count_6}/3 → {verdict_6}")
print(f"  Top-5 on: {top5_count_6}/3 metrics")

# Where did the 7-role original land?
r7 = next((r for r in results_6 if r["name"] == "7ROLE_ORIGINAL"), None)
if r7:
    print(f"\n  7-Role original as challenger:")
    print(f"    TS rank: {r7['rank_ts_score']}, Classification rank: {r7['rank_cls_accuracy']}, Markov rank: {r7['rank_markov_struct']}")

# Top 5 for each metric
for metric, label in [("ts_score","TS"), ("cls_accuracy","Classification"), ("markov_struct","Markov")]:
    sorted_r = sorted(results_6, key=lambda x: x[f"rank_{metric}"])
    print(f"\nTop 5 by {label}:")
    for r in sorted_r[:5]:
        mark = " ← 6-ROLE ORIGINAL" if r["is_original"] else ""
        mark2 = " ← 7-ROLE" if r["name"]=="7ROLE_ORIGINAL" else ""
        print(f"  #{r[f'rank_{metric}']} {r['name']}: {r[metric]:.4f}{mark}{mark2}")

# ──────────────────────────────────────────────────────────
# P2.4 rerun: Entropy Decomposition (6-role model)
# ──────────────────────────────────────────────────────────
print("\n=== P2.4 rerun (6-role model) ===")

role_bigrams_6 = defaultdict(lambda: defaultdict(int))
role_counts_6 = defaultdict(int)
for line in lines_data:
    roles = [CLUSTER_TO_6ROLE.get(t) for t in line["tokens"] if CLUSTER_TO_6ROLE.get(t)]
    for r in roles:
        role_counts_6[r] += 1
    for i in range(len(roles)-1):
        role_bigrams_6[roles[i]][roles[i+1]] += 1

H_unigram_6 = shannon_entropy(role_counts_6)
total_bg_6 = sum(sum(v.values()) for v in role_bigrams_6.values())
H_structural_6 = sum(
    (sum(nc.values())/total_bg_6) * shannon_entropy(nc)
    for nc in role_bigrams_6.values()
)

# Variant entropy (H(cluster|role)) under 6-role model
variant_h_6 = {}
for role in ROLES_6:
    cluster_counts = Counter()
    for line in lines_data:
        for t in line["tokens"]:
            if CLUSTER_TO_6ROLE.get(t) == role:
                cluster_counts[t] += 1
    h = shannon_entropy(cluster_counts)
    n_c = len(SPBCEH_6ROLE[role])
    variant_h_6[role] = {"H": h, "H_max": math.log2(n_c) if n_c > 1 else 0,
                          "n_clusters": n_c, "total": sum(cluster_counts.values())}

total_assigned_6 = sum(v["total"] for v in variant_h_6.values())
H_variant_6 = sum((v["total"]/total_assigned_6)*v["H"] for v in variant_h_6.values())

print(f"H(role unigram, 6-role): {H_unigram_6:.4f} bits")
print(f"H(structural, 6-role): {H_structural_6:.4f} bits")
print(f"H(variant, 6-role): {H_variant_6:.4f} bits")
print(f"Prediction holds (H_structural < H_variant)? {H_structural_6 < H_variant_6}")
print(f"  Difference: {H_variant_6 - H_structural_6:.4f} bits ({'positive = prediction holds' if H_variant_6 > H_structural_6 else 'negative = reversed'})")
print("\nH(cluster|role) per 6-role:")
for role in ROLES_6:
    v = variant_h_6[role]
    print(f"  {role}: H={v['H']:.4f}, n={v['n_clusters']} clusters, tokens={v['total']}")

# ──────────────────────────────────────────────────────────
# Save results
# ──────────────────────────────────────────────────────────
output = {
    "model": "6-role (ACT+MODE merged as CONTENT)",
    "p25_v2": {
        "n_mappings": len(results_6),
        "original_scores": {
            "ts": orig_6["ts_score"],
            "cls": orig_6["cls_accuracy"],
            "markov": orig_6["markov_struct"],
        },
        "original_ranks": {
            "ts": orig_6["rank_ts_score"],
            "cls": orig_6["rank_cls_accuracy"],
            "markov": orig_6["rank_markov_struct"],
        },
        "top3_count": top3_count_6,
        "top5_count": top5_count_6,
        "verdict": verdict_6,
        "all_results": results_6,
    },
    "p14_cls_accuracy": scores_6["cls_accuracy"],
    "p16_close_init_z": close_init_z_6,
    "p24_entropy": {
        "H_structural": H_structural_6,
        "H_variant": H_variant_6,
        "prediction_holds": H_structural_6 < H_variant_6,
    },
    "p13_ts": {
        "ts_original": ts_orig_6,
        "ts_inverted": ts_inv_6,
        "ts_shuffled_mean": mean_ts_sh,
        "z_orig_vs_shuffled": z_orig_vs_shuf,
    },
}

with open(OUT_DIR / "p2_5_v2_6role_results.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nSaved: p2_5_v2_6role_results.json")
print("\n=== Track B Complete ===")
