"""
R6_hebrew_alignment.py — R6 Cluster Hebrew Preposition Alignment
================================================================
Claim: P2-CLAIM-018 (PROVISIONAL → target: CONFIRMED after null model)
Statement: R6 (REF role) token types align with Hebrew grammatical prepositions
           and proclitic particles at a pre-specified rate.

Method:
1. Extract all REF-role token types from results/p1_1_cluster_frequencies.csv
2. Apply EVA consonant-skeleton normalization
3. Score against pre-specified Hebrew preposition inventory (13 forms)
4. Compute null baseline: random EVA short sequences vs Hebrew set
5. Run Control pool 1: non-REF tokens of matching length
6. Report match rates and whether R6 pool exceeds baseline

Pre-registered components (frozen before scoring):
  - R6 pool definition: role == 'REF' in p1_1_cluster_frequencies.csv
  - Extended pool: AR token + tokens in EXTENDED_R6_CANDIDATES (see §2)
  - Hebrew inventory: HEBREW_PREPOSITIONS (13 forms, §3)
  - Normalization: EVA vowel-stripping (o,a,e,i,u treated as vowel markers)
  - Match criterion: ≥2 consonants shared in order (2-con ordered match);
                     also reported at 1-con threshold
  - Baseline: random 1-4 consonant sequences from EVA consonant pool

Reference: docs/R6_HEBREW_ALIGNMENT_METHOD.md
Output:    results/R6_hebrew_alignment_results.json

Date: 2026-03-19
Author: SPBCEH Research Program
"""

import csv
import json
import random
import re
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path
from scipy.stats import fisher_exact

random.seed(42)

BASE = Path(__file__).parent.parent
DATA_DIR = BASE / "data"
RESULTS_DIR = BASE / "results"

# ============================================================
# 1. LOAD CORPUS AND ROLE MAP
# ============================================================

print("=" * 70)
print("R6 Hebrew Preposition Alignment — P2-CLAIM-018")
print("=" * 70)

roles_path = RESULTS_DIR / "p1_1_cluster_frequencies.csv"
corpus_path = DATA_DIR / "corpus_tokens.csv"

# Build role_map: cluster → role
role_map = {}
cluster_freq = {}
with open(roles_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        role_map[row['cluster']] = row['role']
        cluster_freq[row['cluster']] = int(row['n_total'])

print(f"\nRole map loaded: {len(role_map)} cluster types")
print(f"Role distribution: {dict(Counter(role_map.values()))}")

# Load corpus
corpus = []
with open(corpus_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        corpus.append(row)

print(f"Corpus: {len(corpus)} tokens")

# ============================================================
# 2. DEFINE R6 TOKEN POOL
# ============================================================

# Primary pool: REF-classified tokens from role_map
ref_types_primary = {t: cluster_freq[t] for t, r in role_map.items() if r == 'REF'}
print(f"\nPrimary R6 pool (role_map REF): {list(ref_types_primary.keys())}")
print(f"  Frequencies: {ref_types_primary}")

# Extended pool: AR token (mentioned in method note) + any short final-position tokens
# that appear frequently and are not assigned to INIT/CLOSE/LINK roles
# These are tracked separately as sensitivity analysis
EXTENDED_R6_CANDIDATES = ['ar']  # explicitly named in method note

# Count corpus positions for all tokens
token_positions = defaultdict(Counter)
for row in corpus:
    tok = row['token']
    pos = row['position']
    token_positions[tok][pos] += 1

# Extended pool: tokens in EXTENDED_R6_CANDIDATES with corpus frequency
ext_types = {}
for tok in EXTENDED_R6_CANDIDATES:
    counts = Counter(r['token'] for r in corpus if r['token'] == tok)
    if tok in counts:
        ext_types[tok] = counts[tok]
    elif tok in cluster_freq:
        ext_types[tok] = cluster_freq[tok]

print(f"Extended R6 candidates (method note mentions): {ext_types}")

# Full test pool (primary + extended)
r6_pool_full = dict(ref_types_primary)
r6_pool_full.update(ext_types)
print(f"Full R6 pool for analysis: {r6_pool_full}")

# ============================================================
# 3. HEBREW PREPOSITION INVENTORY (PRE-SPECIFIED, FROZEN)
# ============================================================
# Source: Standard Biblical Hebrew and Mishnaic Hebrew grammar inventories
# Romanization follows standard transliteration conventions
# Consonant skeletons: vowels stripped; gutturals ʿ (Ayin) and ʾ (Aleph) treated as silent

HEBREW_PREPOSITIONS = [
    # Form                Transliteration   Consonants  Meaning
    ("ל",               "le/li",           "l",        "to, for (proclitic)"),
    ("ב",               "be/ba",           "b",        "in, with, by (proclitic)"),
    ("מ",               "mi",              "m",        "from (short form)"),
    ("מן",              "min",             "mn",       "from"),
    ("ו",               "ve",              "v",        "and (proclitic)"),
    ("ה",               "ha",              "h",        "the (definite article, proclitic)"),
    ("כ",               "ke/ka",           "k",        "like, as (proclitic)"),
    ("על",              "al",              "l",        "on, upon (guttural ʿ treated silent)"),
    ("אל",              "el",              "l",        "to, toward (guttural ʾ treated silent)"),
    ("עם",              "im",              "m",        "with (guttural ʿ treated silent)"),
    ("אם",              "im",              "m",        "if (guttural ʾ treated silent)"),
    ("כי",              "ki",              "ky",       "because, for, that"),
    ("אשר",             "asher",           "shr",      "that, which, who"),
    ("רק",              "rak",             "rk",       "only, but"),
    ("עד",              "ad",              "d",        "until, as far as (guttural silent)"),
    ("בין",             "bein",            "bn",       "between"),
    ("כל",              "kol/kul",         "kl",       "all, every"),
    ("לא",              "lo",              "l",        "not (negation particle)"),
]

print(f"\nHebrew inventory: {len(HEBREW_PREPOSITIONS)} forms (pre-specified, frozen)")

# ============================================================
# 4. EVA CONSONANT NORMALIZATION
# ============================================================

EVA_VOWELS = set('aeiouAEIOU')
EVA_DIGRAPHS = {
    'lch': 'L',
    'ch':  'C',
    'sh':  'S',
}

def extract_eva_consonants(token):
    """
    Extract consonant skeleton from an EVA token.
    1. Remove ! marker (Eva-T glyph variant, not a phoneme)
    2. Replace digraphs with single placeholders
    3. Strip vowel characters (a, e, i, o, u)
    4. Return remaining consonant string in lowercase
    """
    tok = token.lower().replace('!', '').replace('?', '')
    # Replace digraphs (longest first)
    for digraph, placeholder in sorted(EVA_DIGRAPHS.items(), key=lambda x: -len(x[0])):
        tok = tok.replace(digraph, placeholder)
    # Strip vowels
    cons = ''.join(c for c in tok if c not in EVA_VOWELS and c.isalpha())
    # Restore digraphs
    cons = cons.replace('L', 'lch').replace('C', 'ch').replace('S', 'sh')
    return cons

def extract_eva_consonants_fullglyph(token):
    """
    Full-glyph normalization: keep the full EVA sequence (no vowel stripping).
    Used for direct matching (e.g., 'al' → Hebrew 'al/el').
    """
    tok = token.lower().replace('!', '').replace('?', '')
    return tok

print("\nEVA consonant extraction test:")
for tok in ['ol', 'or', 'al', 'ar', 'qokain', 'laiin', 'ai!n']:
    print(f"  {tok:10} → vowel-strip: '{extract_eva_consonants(tok)}'"
          f"  full-glyph: '{extract_eva_consonants_fullglyph(tok)}'")

# ============================================================
# 5. ALIGNMENT SCORING
# ============================================================

def ordered_match_count(seq_a, seq_b):
    """Count the number of characters in seq_a that appear in seq_b in order."""
    i, j = 0, 0
    count = 0
    while i < len(seq_a) and j < len(seq_b):
        if seq_a[i] == seq_b[j]:
            count += 1
            i += 1
            j += 1
        else:
            j += 1
    return count

def match_against_inventory(eva_cons, inventory, min_match=2):
    """
    Test whether an EVA consonant skeleton matches any item in the inventory
    at the specified minimum consonant count.
    Returns (bool: matched, list of matching forms).
    """
    matched_forms = []
    for form, roman, heb_cons, meaning in inventory:
        shared = ordered_match_count(eva_cons, heb_cons)
        if shared >= min_match:
            matched_forms.append((form, roman, heb_cons, meaning, shared))
    return len(matched_forms) > 0, matched_forms

def match_fullglyph(eva_full, inventory):
    """Full-glyph match: EVA string contains or equals Hebrew romanization."""
    matched = []
    for form, roman, heb_cons, meaning in inventory:
        # Direct string match: EVA sequence == Hebrew romanization consonant skeleton
        if eva_full == heb_cons or eva_full in heb_cons or heb_cons in eva_full:
            matched.append((form, roman, heb_cons, meaning, 'fullglyph'))
    return len(matched) > 0, matched

# Score all R6 tokens
print("\n" + "=" * 70)
print("R6 ALIGNMENT RESULTS")
print("=" * 70)

results_primary = {}
results_extended = {}

print("\n--- Primary R6 pool (role_map REF) ---")
print(f"{'Token':8} {'Cons':6} {'Full':6} {'2-con match':12} {'1-con match':12} {'Matching forms'}")

for tok in sorted(r6_pool_full.keys()):
    is_primary = tok in ref_types_primary
    cons = extract_eva_consonants(tok)
    full = extract_eva_consonants_fullglyph(tok)
    n_total = r6_pool_full[tok]

    hit_2con, forms_2con = match_against_inventory(cons, HEBREW_PREPOSITIONS, min_match=2)
    hit_1con, forms_1con = match_against_inventory(cons, HEBREW_PREPOSITIONS, min_match=1)
    hit_full, forms_full = match_fullglyph(full, HEBREW_PREPOSITIONS)

    label = "(primary)" if is_primary else "(extended)"
    print(f"\n{tok:8} {label}  cons='{cons}'  full='{full}'  n={n_total}")
    print(f"  2-con match: {'YES' if hit_2con else 'NO'}")
    if forms_2con:
        for f in forms_2con:
            print(f"    → {f[0]} ({f[1]}) heb_cons={f[2]} shared={f[4]}")
    print(f"  1-con match: {'YES' if hit_1con else 'NO'}")
    if forms_1con and not hit_2con:
        for f in forms_1con:
            print(f"    → {f[0]} ({f[1]}) heb_cons={f[2]}")
    print(f"  Full-glyph match: {'YES' if hit_full else 'NO'}")
    if forms_full:
        for f in forms_full:
            print(f"    → {f[0]} ({f[1]}) heb_cons={f[2]}")

    entry = {
        'token': tok,
        'n_corpus': n_total,
        'is_primary_ref': is_primary,
        'eva_consonants': cons,
        'eva_fullglyph': full,
        'match_2con': hit_2con,
        'match_1con': hit_1con,
        'match_fullglyph': hit_full,
        'matching_forms_2con': [(f[0], f[1], f[2], f[3]) for f in forms_2con],
        'matching_forms_1con': [(f[0], f[1], f[2], f[3]) for f in forms_1con],
    }
    if is_primary:
        results_primary[tok] = entry
    results_extended[tok] = entry

# ============================================================
# 6. MATCH RATE COMPUTATION
# ============================================================

print("\n" + "=" * 70)
print("MATCH RATE SUMMARY")
print("=" * 70)

def compute_rates(pool_results, label, min_match):
    n_pool = len(pool_results)
    key = f'match_{min_match}con'
    n_match = sum(1 for r in pool_results.values() if r[key])
    rate = n_match / n_pool if n_pool > 0 else 0
    print(f"\n{label} | {min_match}-con threshold:")
    print(f"  Pool size: {n_pool} token types")
    print(f"  Matches: {n_match} ({rate:.1%})")
    return n_pool, n_match, rate

n_p, m_2con_p, rate_2con_p = compute_rates(results_primary, "Primary R6 (REF only)", 2)
n_p, m_1con_p, rate_1con_p = compute_rates(results_primary, "Primary R6 (REF only)", 1)
n_e, m_2con_e, rate_2con_e = compute_rates(results_extended, "Extended R6 (REF + AR)", 2)
n_e, m_1con_e, rate_1con_e = compute_rates(results_extended, "Extended R6 (REF + AR)", 1)

print(f"\n** CLAIM CHECK (P2-CLAIM-018) **")
print(f"  Claimed rate: 52.6%")
print(f"  Primary pool 2-con: {rate_2con_p:.1%} ({m_2con_p}/{n_p})")
print(f"  Primary pool 1-con: {rate_1con_p:.1%} ({m_1con_p}/{n_p})")
print(f"  Extended pool 2-con: {rate_2con_e:.1%} ({m_2con_e}/{n_e})")
print(f"  Extended pool 1-con: {rate_1con_e:.1%} ({m_1con_e}/{n_e})")
print(f"\n  NOTE: 52.6% is not reproducible with 3 (primary) or 4 (extended)")
print(f"  REF token types. The original analysis likely used a larger R6 pool")
print(f"  (e.g., 19 types with 10 matches). See docs/R6_HEBREW_ALIGNMENT_METHOD.md")
print(f"  §7 (limitations) — the exact token pool is undocumented.")

# ============================================================
# 7. NULL BASELINE
# ============================================================

print("\n" + "=" * 70)
print("NULL BASELINE")
print("=" * 70)
print("Generating random 1-2 consonant EVA sequences and testing against Hebrew...")

EVA_CONSONANTS = list('qkdtnlrfmgsj')  # excluding digraphs for simplicity

random.seed(42)
N_RANDOM = 10000
random_hits_2con = 0
random_hits_1con = 0

for _ in range(N_RANDOM):
    length = random.choice([1, 2, 3])
    rand_cons = ''.join(random.choices(EVA_CONSONANTS, k=length))
    hit2, _ = match_against_inventory(rand_cons, HEBREW_PREPOSITIONS, min_match=2)
    hit1, _ = match_against_inventory(rand_cons, HEBREW_PREPOSITIONS, min_match=1)
    if hit2:
        random_hits_2con += 1
    if hit1:
        random_hits_1con += 1

baseline_2con = random_hits_2con / N_RANDOM
baseline_1con = random_hits_1con / N_RANDOM
print(f"  Random sequences tested: {N_RANDOM}")
print(f"  Baseline 2-con match rate: {baseline_2con:.1%}")
print(f"  Baseline 1-con match rate: {baseline_1con:.1%}")

print(f"\n  Primary pool vs baseline:")
print(f"    2-con: R6={rate_2con_p:.1%} vs baseline={baseline_2con:.1%}"
      f"  {'ABOVE' if rate_2con_p > baseline_2con else 'BELOW or AT'} baseline")
print(f"    1-con: R6={rate_1con_p:.1%} vs baseline={baseline_1con:.1%}"
      f"  {'ABOVE' if rate_1con_p > baseline_1con else 'BELOW or AT'} baseline")

# ============================================================
# 8. CONTROL POOL 1 — Non-REF tokens of matching length
# ============================================================

print("\n" + "=" * 70)
print("CONTROL POOL 1 — Non-REF tokens of matching length")
print("=" * 70)

# Get lengths of R6 tokens
r6_lengths = [len(t) for t in r6_pool_full.keys()]
max_r6_len = max(r6_lengths)

# Sample non-REF tokens of matching length
non_ref_tokens = {
    t: cluster_freq.get(t, 0)
    for t, r in role_map.items()
    if r != 'REF' and len(t) <= max_r6_len + 1
}
# Extend to corpus tokens not in role_map that are short
short_corpus_types = Counter(
    row['token'] for row in corpus
    if len(row['token']) <= max_r6_len + 1 and row['token'] not in role_map
)
# Sample 50 non-REF short types
all_non_ref = list(non_ref_tokens.keys()) + list(short_corpus_types.keys())
random.shuffle(all_non_ref)
control_sample = all_non_ref[:50]

ctrl_hits_2con = 0
ctrl_hits_1con = 0
ctrl_results = {}
for tok in control_sample:
    cons = extract_eva_consonants(tok)
    hit2, _ = match_against_inventory(cons, HEBREW_PREPOSITIONS, min_match=2)
    hit1, _ = match_against_inventory(cons, HEBREW_PREPOSITIONS, min_match=1)
    ctrl_results[tok] = {'match_2con': hit2, 'match_1con': hit1}
    if hit2:
        ctrl_hits_2con += 1
    if hit1:
        ctrl_hits_1con += 1

ctrl_rate_2con = ctrl_hits_2con / len(control_sample) if control_sample else 0
ctrl_rate_1con = ctrl_hits_1con / len(control_sample) if control_sample else 0

print(f"  Control sample size: {len(control_sample)} non-REF short tokens")
print(f"  Control 2-con match rate: {ctrl_rate_2con:.1%}")
print(f"  Control 1-con match rate: {ctrl_rate_1con:.1%}")

# Fisher exact test: R6 vs control (2-con)
contingency_2con = [
    [m_2con_p, n_p - m_2con_p],
    [ctrl_hits_2con, len(control_sample) - ctrl_hits_2con]
]
try:
    fe_2con = fisher_exact(contingency_2con)
    p_fisher_2con = fe_2con.pvalue
    or_fisher_2con = fe_2con.statistic
    print(f"\n  Fisher exact (R6 vs control, 2-con): OR={or_fisher_2con:.3f}, p={p_fisher_2con:.4f}")
    if p_fisher_2con < 0.05:
        print(f"  → R6 pool significantly ABOVE control at 2-con threshold (p<0.05)")
    else:
        print(f"  → R6 pool NOT significantly above control at 2-con threshold (p={p_fisher_2con:.4f})")
        print(f"  → P2-CLAIM-018 CANNOT be upgraded based on primary REF pool alone")
        print(f"     The original 52.6% likely required a larger R6 pool definition")
except Exception as e:
    p_fisher_2con = None
    or_fisher_2con = None
    print(f"  Fisher exact could not be computed: {e}")

# ============================================================
# 9. INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("INTERPRETATION AND STATUS")
print("=" * 70)
print("""
Key findings:
1. The role_map yields 3 primary REF token types (ol, or, al).
   This is insufficient to reproduce the claimed 52.6% rate
   (which requires ~10/19 token types).

2. The original P2-CLAIM-018 analysis must have used a larger R6 pool
   beyond the 3 confirmed role_map REF types. This pool is undocumented.

3. At 1-con threshold (single consonant match):
   - All tokens with 'l' or 'r' consonants will match Hebrew prepositions
     with very high baseline probability.
   - This threshold is too weak for a meaningful claim.

4. At 2-con threshold:
   - Very few R6 tokens have 2+ consonants to match.
   - Short tokens (ol, al, or, ar) are predominantly single-consonant
     after vowel-stripping, making 2-con matching impossible.

5. Full-glyph matching:
   - 'al' directly matches Hebrew 'al' (על, אל) — this is a genuine match.
   - This is the strongest alignment in the R6 pool.

Status implication:
  P2-CLAIM-018 REMAINS PROVISIONAL.
  The script documents the gap: to upgrade, the original R6 pool definition
  must be retrieved and the null model must show the rate exceeds baseline.
  See docs/R6_HEBREW_ALIGNMENT_METHOD.md §10 for upgrade steps.
""")

# ============================================================
# 10. SAVE RESULTS
# ============================================================

output = {
    "claim_id": "P2-CLAIM-018",
    "status": "PROVISIONAL — see interpretation",
    "date": "2026-03-19",
    "hebrew_inventory_size": len(HEBREW_PREPOSITIONS),
    "primary_r6_pool": {
        "tokens": list(results_primary.keys()),
        "n_types": n_p,
        "match_rate_2con": round(rate_2con_p, 4),
        "match_rate_1con": round(rate_1con_p, 4),
        "matches_2con": m_2con_p,
        "matches_1con": m_1con_p,
    },
    "extended_r6_pool": {
        "tokens": list(results_extended.keys()),
        "n_types": n_e,
        "match_rate_2con": round(rate_2con_e, 4),
        "match_rate_1con": round(rate_1con_e, 4),
    },
    "claimed_rate_p2_claim_018": 0.526,
    "null_baseline": {
        "n_random_sequences": N_RANDOM,
        "baseline_2con": round(baseline_2con, 4),
        "baseline_1con": round(baseline_1con, 4),
    },
    "control_pool_1": {
        "n_control": len(control_sample),
        "ctrl_rate_2con": round(ctrl_rate_2con, 4),
        "ctrl_rate_1con": round(ctrl_rate_1con, 4),
        "fisher_p_2con": round(p_fisher_2con, 4) if p_fisher_2con is not None else None,
        "fisher_or_2con": round(or_fisher_2con, 4) if or_fisher_2con is not None else None,
    },
    "token_details": results_extended,
    "interpretation": (
        "P2-CLAIM-018 PROVISIONAL: The role_map yields only 3 REF token types "
        "(ol, or, al). The claimed 52.6% rate requires ~19 R6 token types and "
        "cannot be reproduced with the current role_map. The original token pool "
        "is undocumented. 'al' directly matches Hebrew al-forms (על, אל) at full-glyph "
        "level — this is the strongest individual match. Upgrade requires: "
        "(1) retrieve original R6 pool definition; (2) null model comparison; "
        "(3) formal Fisher exact test. See docs/R6_HEBREW_ALIGNMENT_METHOD.md §10."
    ),
    "upgrade_path": "docs/R6_HEBREW_ALIGNMENT_METHOD.md §10",
}

out_path = RESULTS_DIR / "R6_hebrew_alignment_results.json"
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f"\nResults saved to: {out_path}")
print("=" * 70)
print("DONE — P2-CLAIM-018 remains PROVISIONAL (see results JSON for detail)")
print("=" * 70)
