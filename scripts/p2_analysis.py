#!/usr/bin/env python3
"""
Loop 2 — Paper 2 Cognitive Model Validation
Tasks: P2.1 (FSA), P2.2 (Sealed/Open), P2.3 (daiin), P2.4 (Entropy), P2.5 (Anti-Projection)
"""

import csv
import json
import math
import random
from collections import defaultdict, Counter
from pathlib import Path

random.seed(42)

BASE_DIR = Path("/Users/roble/Library/Mobile Documents/com~apple~CloudDocs/Blog Article/Voynich_Manusript")
D1_DIR = BASE_DIR / "research" / "D1_corpus"
P1_DIR = BASE_DIR / "research" / "P1_structural"
OUT_DIR = BASE_DIR / "research" / "P2_cognitive"
OUT_DIR.mkdir(exist_ok=True)

# ──────────────────────────────────────────────────────────
# SPBCEH role definitions (from P1 script)
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

CLUSTER_TO_ROLE = {}
for role, clusters in SPBCEH_CLUSTERS.items():
    for c in clusters:
        CLUSTER_TO_ROLE[c] = role

ALL_CLUSTERS = []
for role in ["INIT","CLOSE","LINK","ACT","MODE","TIME","REF"]:
    ALL_CLUSTERS.extend(SPBCEH_CLUSTERS[role])

ROLES = ["INIT","CLOSE","LINK","ACT","MODE","TIME","REF"]

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
            "is_para_start": row["is_para_start"] == "True",
            "is_para_end": row["is_para_end"] == "True",
            "tokens": tokens,
            "role_seq": [CLUSTER_TO_ROLE.get(t) for t in tokens],
        })

print(f"  Lines loaded: {len(lines_data)}")

# Build paragraph-level token sequences
paragraphs = defaultdict(list)
para_meta = {}
for line in lines_data:
    pid = line["paragraph_id"]
    paragraphs[pid].extend(line["tokens"])
    if pid not in para_meta:
        para_meta[pid] = {"section": line["section"], "currier": line["currier"], "folio_id": line["folio_id"]}

# ──────────────────────────────────────────────────────────
# P2.1 — FSA Conformance
# ──────────────────────────────────────────────────────────
print("\n=== P2.1: FSA Conformance ===")

def classify_fsa(role_seq):
    """
    Parse a role sequence through the SPBCEH packet FSA.
    States: IDLE, OPENED, PAYLOAD, CLOSED
    Returns (n_complete_packets, n_transitions, conformant_transitions, violations, last_state)
    """
    # FSA rules (v1.1 transition model):
    # IDLE -> INIT -> OPENED
    # OPENED -> {ACT,MODE,LINK,REF,TIME} -> PAYLOAD
    # OPENED -> CLOSE -> CLOSED  (empty packet — allowed)
    # PAYLOAD -> {ACT,MODE,LINK,REF,TIME} -> PAYLOAD  (self-loop)
    # PAYLOAD -> CLOSE -> CLOSED
    # CLOSED -> INIT -> OPENED  (new packet — the z=+9.75 signal)
    # CLOSED -> {ACT,MODE,LINK,REF,TIME} -> PAYLOAD  (continuation without re-init)
    # Any INIT in IDLE -> OPENED

    # Score each transition
    roles = [r for r in role_seq if r is not None]
    if not roles:
        return {"complete_packets": 0, "n_roles": 0, "conformant": 0, "violations": 0,
                "last_state": "IDLE", "violation_types": []}

    state = "IDLE"
    complete_packets = 0
    conformant = 0
    violations = 0
    violation_types = []
    n_roles = len(roles)

    for role in roles:
        if state == "IDLE":
            if role == "INIT":
                state = "OPENED"
                conformant += 1
            else:
                # Starting without INIT — violation (or IDLE continuation)
                violations += 1
                violation_types.append(f"non-INIT in IDLE: {role}")
                # Stay in IDLE; this token is "floating"

        elif state == "OPENED":
            if role in ("ACT","MODE","LINK","REF","TIME"):
                state = "PAYLOAD"
                conformant += 1
            elif role == "CLOSE":
                state = "CLOSED"
                complete_packets += 1
                conformant += 1
            elif role == "INIT":
                # Double init — violation
                violations += 1
                violation_types.append("double-INIT")
                state = "OPENED"  # restart

        elif state == "PAYLOAD":
            if role in ("ACT","MODE","LINK","REF","TIME"):
                conformant += 1  # self-loop
            elif role == "CLOSE":
                state = "CLOSED"
                complete_packets += 1
                conformant += 1
            elif role == "INIT":
                # INIT without prior CLOSE — violation
                violations += 1
                violation_types.append("INIT-without-CLOSE")
                state = "OPENED"

        elif state == "CLOSED":
            if role == "INIT":
                state = "OPENED"
                complete_packets += 1  # This starts a new packet confirmed
                conformant += 1
            elif role in ("ACT","MODE","LINK","REF","TIME"):
                # Continuation without re-init
                state = "PAYLOAD"
                conformant += 1
            elif role == "CLOSE":
                # Double close — violation
                violations += 1
                violation_types.append("double-CLOSE")
                state = "CLOSED"

    return {
        "complete_packets": complete_packets,
        "n_roles": n_roles,
        "conformant": conformant,
        "violations": violations,
        "last_state": state,
        "violation_types": violation_types,
    }

# Run FSA on lines
line_results = []
for line in lines_data:
    res = classify_fsa(line["role_seq"])
    res["line_id"] = line["line_id"]
    res["section"] = line["section"]
    res["paragraph_id"] = line["paragraph_id"]
    line_results.append(res)

# Conformance: % of lines with at least one complete packet AND no violations
lines_with_roles = [r for r in line_results if r["n_roles"] > 0]
lines_with_packets = [r for r in lines_with_roles if r["complete_packets"] > 0]
lines_conformant = [r for r in lines_with_roles if r["violations"] == 0 and r["n_roles"] >= 2]
lines_perfect = [r for r in lines_with_roles if r["complete_packets"] > 0 and r["violations"] == 0]

pct_has_packet = 100 * len(lines_with_packets) / len(lines_with_roles)
pct_no_violations = 100 * len(lines_conformant) / len(lines_with_roles)
pct_perfect = 100 * len(lines_perfect) / len(lines_with_roles)

# Total conformant transitions
total_transitions = sum(r["n_roles"] for r in lines_with_roles)
total_conformant_trans = sum(r["conformant"] for r in lines_with_roles)
total_violations = sum(r["violations"] for r in lines_with_roles)
pct_conformant_trans = 100 * total_conformant_trans / total_transitions

print(f"Lines with assigned roles: {len(lines_with_roles)}")
print(f"Lines with >=1 complete packet: {len(lines_with_packets)} ({pct_has_packet:.1f}%)")
print(f"Lines with 0 FSA violations: {len(lines_conformant)} ({pct_no_violations:.1f}%)")
print(f"Lines perfect (packets + no violations): {len(lines_perfect)} ({pct_perfect:.1f}%)")
print(f"Total role transitions: {total_transitions}")
print(f"Conformant transitions: {total_conformant_trans} ({pct_conformant_trans:.1f}%)")
print(f"Violations: {total_violations} ({100-pct_conformant_trans:.1f}%)")

# Violation types
all_vtypes = []
for r in line_results:
    all_vtypes.extend(r["violation_types"])
vtype_counts = Counter(all_vtypes)
print("\nViolation types:")
for vt, cnt in vtype_counts.most_common():
    print(f"  {vt}: {cnt}")

# Section breakdown
section_conformance = defaultdict(lambda: {"total": 0, "conformant": 0})
for r in lines_with_roles:
    s = r["section"]
    section_conformance[s]["total"] += 1
    if r["violations"] == 0 and r["n_roles"] >= 2:
        section_conformance[s]["conformant"] += 1

print("\nSection conformance (no violations, n_roles>=2):")
for s in sorted(section_conformance):
    d = section_conformance[s]
    pct = 100 * d["conformant"] / d["total"] if d["total"] > 0 else 0
    print(f"  {s}: {d['conformant']}/{d['total']} ({pct:.1f}%)")

# Paragraph-level FSA
print("\n--- Paragraph-level FSA ---")
para_results = []
for pid, tokens in paragraphs.items():
    role_seq = [CLUSTER_TO_ROLE.get(t) for t in tokens]
    res = classify_fsa(role_seq)
    res["paragraph_id"] = pid
    res["section"] = para_meta[pid]["section"]
    res["folio_id"] = para_meta[pid]["folio_id"]
    para_results.append(res)

para_with_roles = [r for r in para_results if r["n_roles"] > 0]
para_with_packets = [r for r in para_with_roles if r["complete_packets"] > 0]
para_conformant = [r for r in para_with_roles if r["violations"] == 0 and r["n_roles"] >= 2]
para_perfect = [r for r in para_with_roles if r["complete_packets"] > 0 and r["violations"] == 0]

p_pct_has_packet = 100 * len(para_with_packets) / len(para_with_roles)
p_pct_no_violations = 100 * len(para_conformant) / len(para_with_roles)
p_pct_perfect = 100 * len(para_perfect) / len(para_with_roles)

p_total_trans = sum(r["n_roles"] for r in para_with_roles)
p_conformant_trans = sum(r["conformant"] for r in para_with_roles)
p_pct_trans = 100 * p_conformant_trans / p_total_trans

print(f"Paragraphs with roles: {len(para_with_roles)}")
print(f"Paragraphs with >=1 complete packet: {len(para_with_packets)} ({p_pct_has_packet:.1f}%)")
print(f"Paragraphs with 0 violations: {len(para_conformant)} ({p_pct_no_violations:.1f}%)")
print(f"Paragraphs perfect: {len(para_perfect)} ({p_pct_perfect:.1f}%)")
print(f"Paragraph transition conformance: {p_pct_trans:.1f}%")

p21_results = {
    "line_level": {
        "lines_with_roles": len(lines_with_roles),
        "lines_with_packets": len(lines_with_packets),
        "pct_has_packet": pct_has_packet,
        "lines_conformant": len(lines_conformant),
        "pct_no_violations": pct_no_violations,
        "lines_perfect": len(lines_perfect),
        "pct_perfect": pct_perfect,
        "total_transitions": total_transitions,
        "conformant_transitions": total_conformant_trans,
        "pct_conformant_trans": pct_conformant_trans,
        "violation_counts": dict(vtype_counts),
        "section_conformance": {s: dict(d) for s, d in section_conformance.items()},
    },
    "para_level": {
        "paragraphs_with_roles": len(para_with_roles),
        "paragraphs_with_packets": len(para_with_packets),
        "pct_has_packet": p_pct_has_packet,
        "paragraphs_conformant": len(para_conformant),
        "pct_no_violations": p_pct_no_violations,
        "paragraphs_perfect": len(para_perfect),
        "pct_perfect": p_pct_perfect,
        "pct_conformant_trans": p_pct_trans,
    }
}

# ──────────────────────────────────────────────────────────
# P2.2 — Sealed vs Open Session Analysis
# ──────────────────────────────────────────────────────────
print("\n=== P2.2: Sealed vs Open Sessions ===")

# Classify paragraphs as sealed or open
sealed = []
open_paras = []

for r in para_with_roles:
    # Sealed: ends in CLOSED state (last CLOSE without subsequent non-INIT)
    if r["last_state"] == "CLOSED":
        sealed.append(r)
    else:
        open_paras.append(r)

pct_sealed = 100 * len(sealed) / len(para_with_roles)
pct_open = 100 * len(open_paras) / len(para_with_roles)
print(f"Sealed paragraphs: {len(sealed)} ({pct_sealed:.1f}%)")
print(f"Open paragraphs: {len(open_paras)} ({pct_open:.1f}%)")

# Are open paragraphs more common at folio boundaries?
# Define "folio boundary" as: last paragraph for a given folio
folio_para_map = defaultdict(list)
for r in para_results:
    folio_para_map[r["folio_id"]].append(r)

# Last paragraph on each folio
folio_last_paras = set()
folio_non_last_paras = set()
for folio, paras in folio_para_map.items():
    valid = [p for p in paras if p["n_roles"] > 0]
    if valid:
        folio_last_paras.add(valid[-1]["paragraph_id"])
        for p in valid[:-1]:
            folio_non_last_paras.add(p["paragraph_id"])

open_at_boundary = sum(1 for r in open_paras if r["paragraph_id"] in folio_last_paras)
open_not_boundary = sum(1 for r in open_paras if r["paragraph_id"] in folio_non_last_paras)
sealed_at_boundary = sum(1 for r in sealed if r["paragraph_id"] in folio_last_paras)
sealed_not_boundary = sum(1 for r in sealed if r["paragraph_id"] in folio_non_last_paras)

total_at_boundary = open_at_boundary + sealed_at_boundary
total_not_boundary = open_not_boundary + sealed_not_boundary

pct_open_at_boundary = 100 * open_at_boundary / total_at_boundary if total_at_boundary > 0 else 0
pct_open_not_boundary = 100 * open_not_boundary / total_not_boundary if total_not_boundary > 0 else 0

print(f"\nAt folio boundaries: {open_at_boundary} open / {sealed_at_boundary} sealed ({pct_open_at_boundary:.1f}% open)")
print(f"Mid-folio: {open_not_boundary} open / {sealed_not_boundary} sealed ({pct_open_not_boundary:.1f}% open)")

# Fisher exact test (manual 2x2)
a, b = open_at_boundary, sealed_at_boundary
c, d = open_not_boundary, sealed_not_boundary
n = a + b + c + d

# Chi-squared 2x2
def chi2_2x2(a, b, c, d):
    n = a + b + c + d
    if n == 0:
        return 0, 1.0
    e11 = (a+b)*(a+c)/n
    e12 = (a+b)*(b+d)/n
    e21 = (c+d)*(a+c)/n
    e22 = (c+d)*(b+d)/n
    chi2 = 0
    for obs, exp in [(a,e11),(b,e12),(c,e21),(d,e22)]:
        if exp > 0:
            chi2 += (obs - exp)**2 / exp
    # p-value approximation (chi2 df=1)
    # Use simple lookup: chi2>3.84 -> p<0.05; >6.63 -> p<0.01; >10.83 -> p<0.001
    return chi2

chi2_val = chi2_2x2(a, b, c, d)
p_sig = "p<0.001" if chi2_val > 10.83 else ("p<0.01" if chi2_val > 6.63 else ("p<0.05" if chi2_val > 3.84 else "p>0.05"))
print(f"\nChi-squared (open at boundary vs not): χ²={chi2_val:.3f}, {p_sig}")

# Section breakdown
section_sealed = defaultdict(lambda: {"sealed": 0, "open": 0})
for r in sealed:
    section_sealed[r["section"]]["sealed"] += 1
for r in open_paras:
    section_sealed[r["section"]]["open"] += 1

print("\nSealed/Open by section:")
for s in sorted(section_sealed):
    d = section_sealed[s]
    tot = d["sealed"] + d["open"]
    pct_s = 100 * d["sealed"] / tot if tot > 0 else 0
    print(f"  {s}: sealed={d['sealed']}, open={d['open']} ({pct_s:.1f}% sealed)")

p22_results = {
    "total_paragraphs": len(para_with_roles),
    "sealed": len(sealed),
    "open": len(open_paras),
    "pct_sealed": pct_sealed,
    "pct_open": pct_open,
    "open_at_boundary": open_at_boundary,
    "sealed_at_boundary": sealed_at_boundary,
    "open_not_boundary": open_not_boundary,
    "sealed_not_boundary": sealed_not_boundary,
    "pct_open_at_boundary": pct_open_at_boundary,
    "pct_open_not_boundary": pct_open_not_boundary,
    "chi2": chi2_val,
    "p_sig": p_sig,
    "section_breakdown": {s: dict(d) for s, d in section_sealed.items()},
}

# ──────────────────────────────────────────────────────────
# P2.3 — daiin Frequency Analysis
# ──────────────────────────────────────────────────────────
print("\n=== P2.3: daiin Frequency & Periodicity ===")

# Build full token sequence in corpus order
all_tokens_ordered = []
for line in lines_data:
    for t in line["tokens"]:
        all_tokens_ordered.append((t, line["section"], line["folio_id"]))

print(f"Total tokens: {len(all_tokens_ordered)}")

# Count and locate daiin
def analyze_token_rhythm(token_name, all_tokens):
    positions = [i for i, (t, s, f) in enumerate(all_tokens) if t == token_name]
    n = len(positions)
    if n < 2:
        return {"count": n, "positions": [], "inter_distances": [], "stats": {}}

    inter = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    mean_d = sum(inter) / len(inter)
    var_d = sum((d - mean_d)**2 for d in inter) / len(inter)
    std_d = math.sqrt(var_d)
    cv = std_d / mean_d if mean_d > 0 else 0

    # Distribution test: Coefficient of Variation
    # Exponential dist has CV=1; periodic has CV<0.5; clustered has CV>1
    shape = "exponential-like (CV~1)" if abs(cv - 1.0) < 0.2 else (
        "periodic/rhythmic (CV<0.5)" if cv < 0.5 else (
        "clustered (CV>1.5)" if cv > 1.5 else "moderate variation"))

    # Histogram of inter-distances (buckets of 5)
    max_d = max(inter)
    bucket_size = max(1, max_d // 20)
    hist = defaultdict(int)
    for d in inter:
        hist[(d // bucket_size) * bucket_size] += 1

    return {
        "count": n,
        "n_inter_distances": len(inter),
        "mean_distance": mean_d,
        "std_distance": std_d,
        "min_distance": min(inter),
        "max_distance": max(inter),
        "cv": cv,
        "distribution_shape": shape,
        "quartiles": sorted(inter)[len(inter)//4:3*len(inter)//4:len(inter)//4],
    }

daiin_stats = analyze_token_rhythm("daiin", all_tokens_ordered)
print(f"daiin: n={daiin_stats['count']}, mean_gap={daiin_stats['mean_distance']:.1f}, "
      f"CV={daiin_stats['cv']:.3f} → {daiin_stats['distribution_shape']}")

# Also analyze primary CLOSE and INIT tokens
for token in ["chedy", "qokeedy", "chol", "aiin"]:
    stats = analyze_token_rhythm(token, all_tokens_ordered)
    if stats["count"] > 0:
        print(f"{token}: n={stats['count']}, mean_gap={stats['mean_distance']:.1f}, CV={stats['cv']:.3f} → {stats['distribution_shape']}")

# daiin by section
daiin_by_section = defaultdict(list)
for i, (t, s, f) in enumerate(all_tokens_ordered):
    if t == "daiin":
        daiin_by_section[s].append(i)

print("\ndaiin by section:")
total_by_section = defaultdict(int)
for t, s, f in all_tokens_ordered:
    total_by_section[s] += 1
for s in sorted(daiin_by_section):
    n = len(daiin_by_section[s])
    tot = total_by_section[s]
    rate = 1000 * n / tot if tot > 0 else 0
    print(f"  {s}: {n} occurrences ({rate:.1f} per 1000 tokens)")

# RF7 check: is daiin exponentially distributed?
cv = daiin_stats['cv']
rf7 = "TRIGGERED" if abs(cv - 1.0) < 0.3 else "CLEAR"
print(f"\nRF7 check: CV={cv:.3f} → {rf7}")

p23_results = {
    "daiin": daiin_stats,
    "rf7_status": rf7,
    "section_distribution": {s: len(v) for s, v in daiin_by_section.items()},
    "section_rates_per_1000": {
        s: round(1000 * len(daiin_by_section[s]) / total_by_section[s], 2)
        for s in daiin_by_section if total_by_section[s] > 0
    },
}

# ──────────────────────────────────────────────────────────
# P2.4 — Entropy Decomposition
# ──────────────────────────────────────────────────────────
print("\n=== P2.4: Entropy Decomposition ===")

def shannon_entropy(counts):
    """Compute Shannon entropy from a dict of counts."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    ent = 0.0
    for c in counts.values():
        if c > 0:
            p = c / total
            ent -= p * math.log2(p)
    return ent

# 1. Structural entropy: H(role_n | role_{n-1}) = H(role bigrams) - H(roles)
# Build role bigram counts from all lines
role_bigrams = defaultdict(lambda: defaultdict(int))
role_counts_total = defaultdict(int)

for line in lines_data:
    roles = [r for r in line["role_seq"] if r is not None]
    for i, r in enumerate(roles):
        role_counts_total[r] += 1
    for i in range(len(roles) - 1):
        role_bigrams[roles[i]][roles[i+1]] += 1

# H(roles) — unigram entropy
H_role_unigram = shannon_entropy(role_counts_total)

# H(role | prev_role) — conditional entropy
# = sum_r P(r) * H(next | prev=r)
total_bigrams = sum(sum(v.values()) for v in role_bigrams.values())
H_structural = 0.0
for from_role, next_counts in role_bigrams.items():
    p_from = sum(next_counts.values()) / total_bigrams
    H_cond = shannon_entropy(next_counts)
    H_structural += p_from * H_cond

print(f"H(role unigram) = {H_role_unigram:.4f} bits")
print(f"H(role | prev_role) = {H_structural:.4f} bits  [structural entropy]")
print(f"  Reduction from bigram conditioning: {H_role_unigram - H_structural:.4f} bits")

# Shuffled baseline: randomize role sequences within each line 1000x
def shuffle_entropy(lines_data, n_permutations=1000):
    """Compute H(role|prev) for shuffled role sequences."""
    h_vals = []
    for _ in range(n_permutations):
        rb = defaultdict(lambda: defaultdict(int))
        for line in lines_data:
            roles = [r for r in line["role_seq"] if r is not None]
            random.shuffle(roles)
            for i in range(len(roles) - 1):
                rb[roles[i]][roles[i+1]] += 1
        tb = sum(sum(v.values()) for v in rb.values())
        h = 0.0
        for fr, nc in rb.items():
            pf = sum(nc.values()) / tb
            h += pf * shannon_entropy(nc)
        h_vals.append(h)
    return h_vals

print("Computing shuffled baseline (100 permutations)...")
shuffled_h = shuffle_entropy(lines_data, n_permutations=100)
mean_shuffled_h = sum(shuffled_h) / len(shuffled_h)
std_shuffled_h = math.sqrt(sum((h - mean_shuffled_h)**2 for h in shuffled_h) / len(shuffled_h))
z_structural = (H_structural - mean_shuffled_h) / std_shuffled_h if std_shuffled_h > 0 else 0

print(f"Shuffled H(role|prev): mean={mean_shuffled_h:.4f}, std={std_shuffled_h:.4f}")
print(f"Z-score (structural vs shuffled): {z_structural:.3f}")

# 2. Variant entropy: H(cluster | role) for each role
variant_h_by_role = {}
for role in ROLES:
    cluster_counts = Counter()
    for line in lines_data:
        for t, r in zip(line["tokens"], line["role_seq"]):
            if r == role:
                cluster_counts[t] += 1
    h = shannon_entropy(cluster_counts)
    n_clusters = len(SPBCEH_CLUSTERS[role])
    h_max = math.log2(n_clusters) if n_clusters > 1 else 0
    variant_h_by_role[role] = {
        "H": h,
        "H_max": h_max,
        "n_clusters": n_clusters,
        "total_tokens": sum(cluster_counts.values()),
    }

H_variant_weighted = 0.0
total_assigned = sum(v["total_tokens"] for v in variant_h_by_role.values())
for role, v in variant_h_by_role.items():
    w = v["total_tokens"] / total_assigned if total_assigned > 0 else 0
    H_variant_weighted += w * v["H"]

print(f"\nH(cluster | role) per role:")
for role in ROLES:
    v = variant_h_by_role[role]
    print(f"  {role}: H={v['H']:.4f} bits (max={v['H_max']:.4f}, n={v['n_clusters']} clusters, "
          f"tokens={v['total_tokens']})")
print(f"\nWeighted H(variant) = {H_variant_weighted:.4f} bits")
print(f"H(structural) = {H_structural:.4f} bits")

prediction_holds = H_structural < H_variant_weighted
print(f"\nPrediction holds (H_structural < H_variant)? {prediction_holds}")
print(f"  Difference: {H_variant_weighted - H_structural:.4f} bits")

p24_results = {
    "H_role_unigram": H_role_unigram,
    "H_structural": H_structural,
    "H_shuffled_mean": mean_shuffled_h,
    "H_shuffled_std": std_shuffled_h,
    "z_structural_vs_shuffled": z_structural,
    "H_variant_weighted": H_variant_weighted,
    "variant_h_by_role": variant_h_by_role,
    "prediction_holds": prediction_holds,
}

# ──────────────────────────────────────────────────────────
# P2.5 — Anti-Projection Test
# ──────────────────────────────────────────────────────────
print("\n=== P2.5: Anti-Projection Test ===")

# Load P1.6 data for Markov scoring
with open(P1_DIR / "p1_6_transition_matrix.json") as f:
    p16_data = json.load(f)

ORIG_PROB_MATRIX = p16_data["prob_matrix"]

def compute_mapping_scores(cluster_to_role_map, lines_data_in):
    """
    Score a role mapping on three metrics:
    1. TS (Transition Score): Markov log-probability of observed sequences
    2. Section classification accuracy (KNN-like: train/test on folios)
    3. Markov structure score: sum of |z-scores| of the 7x7 bigram matrix
    """
    roles = list(set(cluster_to_role_map.values()))

    # Build role sequences for all lines
    mapped_lines = []
    for line in lines_data_in:
        r_seq = [cluster_to_role_map.get(t) for t in line["tokens"]]
        r_seq = [r for r in r_seq if r is not None]
        mapped_lines.append({
            "line_id": line["line_id"],
            "section": line["section"],
            "folio_id": line["folio_id"],
            "role_seq": r_seq,
        })

    # TS: Markov log-prob
    # Build transition matrix
    bigrams = defaultdict(lambda: defaultdict(int))
    role_totals = defaultdict(int)
    for ml in mapped_lines:
        rseq = ml["role_seq"]
        for i in range(len(rseq) - 1):
            bigrams[rseq[i]][rseq[i+1]] += 1
            role_totals[rseq[i]] += 1

    # Compute transition probs with Laplace smoothing
    all_roles_in_map = sorted(set(cluster_to_role_map.values()))
    K = len(all_roles_in_map)
    trans_probs = {}
    for r1 in all_roles_in_map:
        total = role_totals[r1] + K  # Laplace smoothing
        trans_probs[r1] = {}
        for r2 in all_roles_in_map:
            trans_probs[r1][r2] = (bigrams[r1][r2] + 1) / total

    # TS: log-prob of observed sequences under this model
    log_prob_sum = 0.0
    n_bigrams = 0
    for ml in mapped_lines:
        rseq = ml["role_seq"]
        for i in range(len(rseq) - 1):
            r1, r2 = rseq[i], rseq[i+1]
            if r1 in trans_probs and r2 in trans_probs.get(r1, {}):
                log_prob_sum += math.log(trans_probs[r1][r2])
                n_bigrams += 1

    ts_score = log_prob_sum / n_bigrams if n_bigrams > 0 else -999

    # Section classification: build per-folio role frequency vectors, classify by majority section
    # Simplification: per-folio role distributions, then leave-one-out on folios
    folio_vecs = defaultdict(lambda: defaultdict(int))
    folio_sections = {}
    folio_totals = defaultdict(int)
    for ml in mapped_lines:
        fid = ml["folio_id"]
        folio_sections[fid] = ml["section"]
        for r in ml["role_seq"]:
            folio_vecs[fid][r] += 1
            folio_totals[fid] += 1

    # Normalize to frequencies
    folio_freq = {}
    for fid, counts in folio_vecs.items():
        tot = folio_totals[fid]
        folio_freq[fid] = {r: counts.get(r, 0) / tot for r in all_roles_in_map}

    # 1-NN classification (leave-one-out)
    folios = list(folio_freq.keys())
    correct = 0
    for i, test_fid in enumerate(folios):
        test_vec = folio_freq[test_fid]
        test_sec = folio_sections[test_fid]
        best_sim = -1
        best_sec = None
        for j, train_fid in enumerate(folios):
            if i == j:
                continue
            train_vec = folio_freq[train_fid]
            # Cosine similarity
            dot = sum(test_vec.get(r, 0) * train_vec.get(r, 0) for r in all_roles_in_map)
            n1 = math.sqrt(sum(v**2 for v in test_vec.values()))
            n2 = math.sqrt(sum(v**2 for v in train_vec.values()))
            sim = dot / (n1 * n2) if n1 * n2 > 0 else 0
            if sim > best_sim:
                best_sim = sim
                best_sec = folio_sections[train_fid]
        if best_sec == test_sec:
            correct += 1

    cls_acc = correct / len(folios) if folios else 0

    # Markov structure score: sum of absolute z-scores
    # Compute z-scores vs shuffled (100 permutations)
    obs_bigrams_flat = {}
    for r1 in all_roles_in_map:
        for r2 in all_roles_in_map:
            obs_bigrams_flat[(r1, r2)] = bigrams[r1][r2]

    # Shuffled distribution (50 permutations for speed)
    shuffled_counts = defaultdict(list)
    for _ in range(50):
        sb = defaultdict(lambda: defaultdict(int))
        for ml in mapped_lines:
            rseq = list(ml["role_seq"])
            random.shuffle(rseq)
            for i in range(len(rseq) - 1):
                sb[rseq[i]][rseq[i+1]] += 1
        for r1 in all_roles_in_map:
            for r2 in all_roles_in_map:
                shuffled_counts[(r1, r2)].append(sb[r1][r2])

    total_abs_z = 0.0
    n_cells = 0
    for (r1, r2), sh_vals in shuffled_counts.items():
        obs = obs_bigrams_flat.get((r1, r2), 0)
        mean_sh = sum(sh_vals) / len(sh_vals)
        std_sh = math.sqrt(sum((v - mean_sh)**2 for v in sh_vals) / len(sh_vals))
        if std_sh > 0:
            z = abs((obs - mean_sh) / std_sh)
            total_abs_z += z
            n_cells += 1

    markov_struct_score = total_abs_z / n_cells if n_cells > 0 else 0

    return {
        "ts_score": ts_score,
        "cls_accuracy": cls_acc,
        "markov_struct": markov_struct_score,
    }

# Generate alternative mappings
print("Generating alternative mappings...")

# Original mapping
original_mapping = CLUSTER_TO_ROLE.copy()

# Helper: get role sizes
role_sizes = {r: len(c) for r, c in SPBCEH_CLUSTERS.items()}

# 20 random permutations
all_mappings = [("ORIGINAL", original_mapping)]

# Random permutations: shuffle ALL cluster-to-role assignments randomly
all_clusters_list = list(original_mapping.keys())
all_roles_list = list(original_mapping.values())

for i in range(20):
    shuffled_roles = all_roles_list.copy()
    random.shuffle(shuffled_roles)
    alt_map = dict(zip(all_clusters_list, shuffled_roles))
    all_mappings.append((f"RANDOM_{i+1:02d}", alt_map))

# 10 hand-crafted "plausible" alternative mappings
# Keep same role labels, but swap cluster assignments strategically

def swap_clusters(base_map, swaps):
    """Create a new mapping by swapping specific cluster role assignments."""
    new_map = base_map.copy()
    for cluster, new_role in swaps:
        if cluster in new_map:
            new_map[cluster] = new_role
    return new_map

crafted_alts = [
    # Alt 1: Move daiin from ACT to TIME (daiin is rhythmic, could be temporal)
    ("CRAFT_01_daiin_as_TIME", swap_clusters(original_mapping, [("daiin", "TIME")])),
    # Alt 2: Move chedy from CLOSE to ACT (chedy is high frequency, could be action)
    ("CRAFT_02_chedy_as_ACT", swap_clusters(original_mapping, [("chedy", "ACT")])),
    # Alt 3: Move qokeedy from INIT to MODE (frequent in biological, could be mode)
    ("CRAFT_03_qokeedy_as_MODE", swap_clusters(original_mapping, [("qokeedy", "MODE")])),
    # Alt 4: Move aiin from TIME to ACT (aiin is frequent, could be action)
    ("CRAFT_04_aiin_as_ACT", swap_clusters(original_mapping, [("aiin", "ACT")])),
    # Alt 5: Swap INIT and CLOSE role labels completely
    ("CRAFT_05_swap_INIT_CLOSE", {c: ("CLOSE" if r == "INIT" else ("INIT" if r == "CLOSE" else r))
                                   for c, r in original_mapping.items()}),
    # Alt 6: Move ol,or,al from REF to LINK (they're connective)
    ("CRAFT_06_REF_as_LINK", swap_clusters(original_mapping,
        [("ol","LINK"),("or","LINK"),("al","LINK")])),
    # Alt 7: Move shol,chol from MODE to CLOSE (they occur at line-end sometimes)
    ("CRAFT_07_MODE_as_CLOSE", swap_clusters(original_mapping,
        [("shol","CLOSE"),("chol","CLOSE")])),
    # Alt 8: Move daiin,dain from ACT to REF (they're high-frequency, could be reference)
    ("CRAFT_08_ACT_as_REF", swap_clusters(original_mapping,
        [("daiin","REF"),("dain","REF")])),
    # Alt 9: Merge ACT and MODE into one (call it ACT)
    ("CRAFT_09_merge_ACT_MODE", {c: ("ACT" if r in ("ACT","MODE") else r)
                                  for c, r in original_mapping.items()}),
    # Alt 10: Move LINK clusters to REF (linking = referencing?)
    ("CRAFT_10_LINK_as_REF", {c: ("REF" if r == "LINK" else r)
                               for c, r in original_mapping.items()}),
]
all_mappings.extend(crafted_alts)

print(f"Total mappings to evaluate: {len(all_mappings)}")
print("Computing scores (this takes a few minutes)...")

results = []
for idx, (name, mapping) in enumerate(all_mappings):
    if idx % 5 == 0:
        print(f"  [{idx+1}/{len(all_mappings)}] Scoring {name}...")
    scores = compute_mapping_scores(mapping, lines_data)
    results.append({
        "name": name,
        "is_original": name == "ORIGINAL",
        "ts_score": scores["ts_score"],
        "cls_accuracy": scores["cls_accuracy"],
        "markov_struct": scores["markov_struct"],
    })

# Rank on each metric
def rank_results(results, metric, higher_is_better=True):
    sorted_r = sorted(results, key=lambda x: x[metric], reverse=higher_is_better)
    for rank, r in enumerate(sorted_r, 1):
        r[f"rank_{metric}"] = rank
    return sorted_r

rank_results(results, "ts_score", higher_is_better=True)
rank_results(results, "cls_accuracy", higher_is_better=True)
rank_results(results, "markov_struct", higher_is_better=True)

orig = next(r for r in results if r["is_original"])

print(f"\n--- Anti-Projection Results ---")
print(f"Original SPBCEH mapping:")
print(f"  TS score: {orig['ts_score']:.4f}  Rank: {orig['rank_ts_score']}/{len(results)}")
print(f"  Classification: {orig['cls_accuracy']:.4f}  Rank: {orig['rank_cls_accuracy']}/{len(results)}")
print(f"  Markov structure: {orig['markov_struct']:.4f}  Rank: {orig['rank_markov_struct']}/{len(results)}")

# Count metrics where original is top 3
top3_count = sum(1 for m in ["rank_ts_score", "rank_cls_accuracy", "rank_markov_struct"]
                 if orig[m] <= 3)
top5_count = sum(1 for m in ["rank_ts_score", "rank_cls_accuracy", "rank_markov_struct"]
                 if orig[m] <= 5)

print(f"\n  Top-3 on ≥2/3 metrics? {top3_count}/3 → {'✅ PASSED' if top3_count >= 2 else ('⚠️ PARTIAL' if top5_count >= 2 else '❌ RF5b TRIGGERED')}")
print(f"  Top-5 on: {top5_count}/3 metrics")

# RF5b check
rf5b = "TRIGGERED" if top3_count < 2 and top5_count < 2 else (
    "PARTIAL" if top3_count < 2 else "CLEAR")
print(f"\n  RF5b: {rf5b}")

# Show top 5 for each metric
for metric, label in [("ts_score","TS"), ("cls_accuracy","Classification"), ("markov_struct","Markov")]:
    sorted_r = sorted(results, key=lambda x: x[f"rank_{metric}"])
    print(f"\nTop 5 by {label}:")
    for r in sorted_r[:5]:
        mark = " ← ORIGINAL" if r["is_original"] else ""
        print(f"  #{r[f'rank_{metric}']} {r['name']}: {r[metric]:.4f}{mark}")

# Statistics on alternatives
alt_results = [r for r in results if not r["is_original"]]
for metric, label in [("ts_score","TS"), ("cls_accuracy","Classification"), ("markov_struct","Markov")]:
    vals = [r[metric] for r in alt_results]
    mean_v = sum(vals) / len(vals)
    max_v = max(vals)
    print(f"\nAlternatives {label}: mean={mean_v:.4f}, max={max_v:.4f}, original={orig[metric]:.4f}")
    margin = orig[metric] - max_v
    print(f"  Margin above best alternative: {margin:.4f} ({'positive = original wins' if margin > 0 else 'NEGATIVE = alternative wins'})")

p25_results = {
    "n_mappings": len(results),
    "original_ranks": {
        "ts": orig["rank_ts_score"],
        "cls": orig["rank_cls_accuracy"],
        "markov": orig["rank_markov_struct"],
    },
    "original_scores": {
        "ts": orig["ts_score"],
        "cls": orig["cls_accuracy"],
        "markov": orig["markov_struct"],
    },
    "top3_count": top3_count,
    "top5_count": top5_count,
    "rf5b": rf5b,
    "all_results": results,
}

# ──────────────────────────────────────────────────────────
# Save all results
# ──────────────────────────────────────────────────────────
print("\n=== Saving results ===")

output = {
    "p2_1": p21_results,
    "p2_2": p22_results,
    "p2_3": p23_results,
    "p2_4": p24_results,
    "p2_5": p25_results,
}

with open(OUT_DIR / "p2_all_results.json", "w") as f:
    json.dump(output, f, indent=2)

print("Saved: p2_all_results.json")
print("\n=== Loop 2 Analysis Complete ===")
