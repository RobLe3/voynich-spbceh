#!/usr/bin/env python3
"""
ROSETTA3d: Stolfi ZL Positional Replication
Date: 2026-03-19

Tests whether the positional biases found in Takahashi H (qokain EARLY Stars,
laiin LATE Stars) replicate in the Stolfi ZL transliteration.

Also tests ai!n corpus-wide LATE — which cannot be tested in ZL (! is
Takahashi-specific) and is documented as TRANSCRIPTION_MISMATCH.

Uses same methodology as ROSETTA3c:
- Same packet reconstruction logic (R1/R2 from role_map)
- Same relative-position metric: pos / (len-1) within packet payload
- Same null model: one-sample Wilcoxon signed-rank vs H0=0.5
- Same significance threshold: p < 0.05
"""

import re
import csv
import json
from collections import defaultdict
from scipy import stats
import numpy as np

# ── Section mapping: folio prefix → section code ────────────────────────────
# Based on standard Voynich section assignments used in Takahashi corpus
FOLIO_SECTION = {}

def assign_section(folio_str):
    """Assign section based on folio number."""
    m = re.match(r'f(\d+)', folio_str)
    if not m:
        return 'U'
    n = int(m.group(1))
    if 1 <= n <= 66:
        return 'H'   # Herbal
    elif 67 <= n <= 73:
        return 'C'   # Cosmological/Circular
    elif n == 74:
        return 'C'
    elif 75 <= n <= 84:
        return 'B'   # Balneological
    elif 85 <= n <= 102:
        return 'P'   # Pharmaceutical
    elif 103 <= n <= 116:
        return 'S'   # Stars/Zodiac
    else:
        return 'U'


# ── Parse ZL IVTFF file ──────────────────────────────────────────────────────
def parse_zl_ivtff(filepath):
    """
    Parse IVTFF 2.0 format ZL file into list of token records.
    Returns list of dicts: folio_id, paragraph_id, line_id, token, position,
    line_length, section.
    """
    records = []
    current_folio = None
    current_para = None
    para_counter = 0

    with open(filepath, encoding='utf-8', errors='replace') as f:
        for raw_line in f:
            line = raw_line.strip()

            # Folio header line: <f1r>  <! ... >
            folio_m = re.match(r'^<(f\d+[rv]\d*)>\s+<!', line)
            if folio_m:
                current_folio = folio_m.group(1)
                current_para = None
                para_counter = 0
                continue

            # Text line: <f1r.1,@P0>  tokens
            text_m = re.match(r'^<([^,>]+),([^>]*)>\s+(.*)', line)
            if not text_m:
                continue

            line_id = text_m.group(1)   # e.g. f1r.1
            line_type = text_m.group(2)  # e.g. @P0, +P0, =Pt
            token_str = text_m.group(3)

            # Determine folio from line_id
            folio_m2 = re.match(r'^(f\d+[rv]\d*)', line_id)
            if not folio_m2:
                continue
            folio_id = folio_m2.group(1)

            # Track paragraphs: @ = start of new paragraph, + = continuation
            if line_type.startswith('@'):
                para_counter += 1
                current_para = f"P{para_counter}"
            elif line_type.startswith('*'):
                para_counter += 1
                current_para = f"P{para_counter}"

            if current_para is None:
                current_para = "P0"

            # Extract tokens: split on . and spaces, strip markup
            # Remove <$>, <%>, <!...>, {...}, [a:b] → take first option
            token_str = re.sub(r'<!([^>]*)>', '', token_str)
            token_str = re.sub(r'<%>', '', token_str)
            token_str = re.sub(r'<\$>', '', token_str)
            token_str = re.sub(r'\{([^}]*)\}', lambda m: m.group(1).split(',')[0], token_str)
            token_str = re.sub(r'\[([^\]]*)\]', lambda m: m.group(1).split(':')[0], token_str)
            token_str = re.sub(r'<->', '', token_str)

            raw_tokens = re.split(r'[.\s,]+', token_str.strip())
            tokens = [t for t in raw_tokens if t and not t.startswith('@') and not t.startswith('%')]

            section = assign_section(folio_id)
            para_id = f"{folio_id}_{current_para}"

            for pos, tok in enumerate(tokens):
                records.append({
                    'folio_id': folio_id,
                    'paragraph_id': para_id,
                    'line_id': line_id,
                    'token': tok,
                    'position': pos,
                    'line_length': len(tokens),
                    'section': section,
                })

    return records


# ── Load role map from Takahashi cluster frequencies ─────────────────────────
def load_role_map(csv_path):
    """Load role assignments from p1_1_cluster_frequencies.csv."""
    role_map = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            role_map[row['cluster']] = row['role']
    return role_map


# ── Packet reconstruction (same logic as ROSETTA3c) ─────────────────────────
def reconstruct_packets(records, role_map, section_filter=None):
    """
    Reconstruct packets from token records.
    Packet: R1 token → payload tokens → R2 token (first R2 after R1).
    Groups by (folio_id, paragraph_id).
    Returns list of dicts: {folio_id, para_id, r1_token, payload, r2_token}.
    """
    R1_TOKENS = {t for t, r in role_map.items() if r == 'INIT'}
    R2_TOKENS = {t for t, r in role_map.items() if r == 'CLOSE'}

    by_para = defaultdict(list)
    for rec in records:
        if section_filter and rec['section'] != section_filter:
            continue
        by_para[(rec['folio_id'], rec['paragraph_id'])].append(rec)

    packets = []
    for (folio_id, para_id), tok_list in by_para.items():
        tok_list.sort(key=lambda x: (x['line_id'], x['position']))
        tokens = [r['token'] for r in tok_list]

        i = 0
        while i < len(tokens):
            if tokens[i] in R1_TOKENS:
                r1 = tokens[i]
                payload = []
                i += 1
                while i < len(tokens) and tokens[i] not in R2_TOKENS and tokens[i] not in R1_TOKENS:
                    payload.append(tokens[i])
                    i += 1
                if i < len(tokens) and tokens[i] in R2_TOKENS:
                    packets.append({
                        'folio_id': folio_id,
                        'para_id': para_id,
                        'r1': r1,
                        'payload': payload,
                        'r2': tokens[i],
                    })
                    i += 1
            else:
                i += 1

    return packets


# ── Positional bias test ─────────────────────────────────────────────────────
def test_positional_bias(packets, target_token):
    """
    For each packet, find all positions of target_token in payload.
    Compute relative position: pos_index / (len(payload) - 1).
    Returns (n, mean_pos, p_value) using Wilcoxon signed-rank vs H0=0.5.
    """
    positions = []
    for pkt in packets:
        payload = pkt['payload']
        if not payload or target_token not in payload:
            continue
        n_payload = len(payload)
        for idx, tok in enumerate(payload):
            if tok == target_token:
                if n_payload == 1:
                    rel = 0.5
                else:
                    rel = idx / (n_payload - 1)
                positions.append(rel)

    if len(positions) < 5:
        return len(positions), np.mean(positions) if positions else None, None

    result = stats.wilcoxon(
        [p - 0.5 for p in positions],
        alternative='two-sided'
    )
    return len(positions), float(np.mean(positions)), float(result.pvalue)


# ── Direction label ──────────────────────────────────────────────────────────
def direction_label(mean, pval, alpha=0.05):
    if pval is None:
        return 'INSUFFICIENT_N'
    if pval >= alpha:
        return 'CENTRAL'
    return 'EARLY' if mean < 0.5 else 'LATE'


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    ZL_FILE = 'data/ZL3b-n.txt'
    ROLE_MAP_FILE = 'results/p1_1_cluster_frequencies.csv'
    OUTPUT_FILE = 'results/ROSETTA3d_stolfi_zl_results.json'

    print("=" * 65)
    print("ROSETTA3d: Stolfi ZL Positional Replication")
    print("=" * 65)

    # Reference values from Takahashi H
    TAKAHASHI_REF = {
        'qokain_stars': {'n': 7, 'mean': 0.248, 'p': 0.007, 'direction': 'EARLY'},
        'laiin_stars':  {'n': 5, 'mean': 0.875, 'p': 0.007, 'direction': 'LATE'},
        'ai!n_corpus':  {'n': 23, 'mean': 0.686, 'p': 0.005, 'direction': 'LATE'},
        'ai!n_stars':   {'n': 19, 'mean': 0.668, 'p': 0.023, 'direction': 'LATE'},
    }

    print("\nLoading ZL transliteration...")
    records = parse_zl_ivtff(ZL_FILE)
    print(f"  Total token records: {len(records)}")

    section_counts = defaultdict(int)
    for r in records:
        section_counts[r['section']] += 1
    print(f"  By section: {dict(section_counts)}")

    print("\nLoading role map...")
    role_map = load_role_map(ROLE_MAP_FILE)
    R1_count = sum(1 for v in role_map.values() if v == 'INIT')
    R2_count = sum(1 for v in role_map.values() if v == 'CLOSE')
    print(f"  R1 (INIT) tokens: {R1_count}")
    print(f"  R2 (CLOSE) tokens: {R2_count}")

    # ── Packet reconstruction ─────────────────────────────────────────────
    print("\nReconstructing packets (all sections)...")
    all_packets = reconstruct_packets(records, role_map)
    print(f"  Total packets: {len(all_packets)}")

    stars_packets = reconstruct_packets(records, role_map, section_filter='S')
    print(f"  Stars section packets: {len(stars_packets)}")

    b_packets = reconstruct_packets(records, role_map, section_filter='B')
    print(f"  Balneological section packets: {len(b_packets)}")

    # ── Token counts in ZL ────────────────────────────────────────────────
    print("\nToken raw counts in ZL:")
    for tok in ['qokain', 'laiin', 'ai!n', 'aiin', 'daiin']:
        count = sum(1 for r in records if r['token'] == tok)
        print(f"  {tok}: {count}")

    # ── Test 1: qokain EARLY in Stars ────────────────────────────────────
    print("\n── Test 1: qokain EARLY in Stars ──")
    n, mean, pval = test_positional_bias(stars_packets, 'qokain')
    direction = direction_label(mean, pval)
    ref = TAKAHASHI_REF['qokain_stars']
    mean_str = f"{mean:.3f}" if mean is not None else "N/A"
    pval_str = f"{pval:.3f}" if pval is not None else "N/A"
    print(f"  ZL:  n={n}, mean={mean_str}, p={pval_str}, direction={direction}")
    print(f"  EVA: n={ref['n']}, mean={ref['mean']}, p={ref['p']}, direction={ref['direction']}")
    if pval is not None and n >= 5:
        delta_n = n - ref['n']
        delta_mean = mean - ref['mean']
        print(f"  Δn={delta_n:+d}, Δmean={delta_mean:+.3f}")
        if pval < 0.05 and direction == ref['direction']:
            verdict_q = 'REPLICATED'
        elif direction == ref['direction']:
            verdict_q = 'WEAKENED_DIRECTION_PRESERVED'
        elif pval >= 0.05:
            verdict_q = 'FAILED_REPLICATION'
        else:
            verdict_q = 'DIRECTION_REVERSED'
    else:
        verdict_q = 'INSUFFICIENT_N'
    print(f"  Verdict: {verdict_q}")

    qokain_result = {
        'token': 'qokain', 'scope': 'Stars', 'claim_id': 'P2-CLAIM-010',
        'zl_n': n, 'zl_mean': mean, 'zl_p': pval, 'zl_direction': direction,
        'eva_n': ref['n'], 'eva_mean': ref['mean'], 'eva_p': ref['p'], 'eva_direction': ref['direction'],
        'verdict': verdict_q,
    }

    # ── Test 2: laiin LATE in Stars ───────────────────────────────────────
    print("\n── Test 2: laiin LATE in Stars ──")
    n2, mean2, pval2 = test_positional_bias(stars_packets, 'laiin')
    direction2 = direction_label(mean2, pval2)
    ref2 = TAKAHASHI_REF['laiin_stars']
    mean2_str = f"{mean2:.3f}" if mean2 is not None else "N/A"
    pval2_str = f"{pval2:.3f}" if pval2 is not None else "N/A"
    print(f"  ZL:  n={n2}, mean={mean2_str}, p={pval2_str}, direction={direction2}")
    print(f"  EVA: n={ref2['n']}, mean={ref2['mean']}, p={ref2['p']}, direction={ref2['direction']}")
    if pval2 is not None and n2 >= 5:
        delta_n2 = n2 - ref2['n']
        delta_mean2 = mean2 - ref2['mean']
        print(f"  Δn={delta_n2:+d}, Δmean={delta_mean2:+.3f}")
        if pval2 < 0.05 and direction2 == ref2['direction']:
            verdict_l = 'REPLICATED'
        elif direction2 == ref2['direction']:
            verdict_l = 'WEAKENED_DIRECTION_PRESERVED'
        elif pval2 >= 0.05:
            verdict_l = 'FAILED_REPLICATION'
        else:
            verdict_l = 'DIRECTION_REVERSED'
    else:
        verdict_l = 'INSUFFICIENT_N'
    print(f"  Verdict: {verdict_l}")

    laiin_result = {
        'token': 'laiin', 'scope': 'Stars', 'claim_id': 'P2-CLAIM-011',
        'zl_n': n2, 'zl_mean': mean2, 'zl_p': pval2, 'zl_direction': direction2,
        'eva_n': ref2['n'], 'eva_mean': ref2['mean'], 'eva_p': ref2['p'], 'eva_direction': ref2['direction'],
        'verdict': verdict_l,
    }

    # ── Test 3: ai!n corpus-wide ──────────────────────────────────────────
    print("\n── Test 3: ai!n LATE corpus-wide ──")
    ain_zl_count = sum(1 for r in records if r['token'] == 'ai!n')
    print(f"  ZL count of 'ai!n': {ain_zl_count}")
    print("  VERDICT: TRANSCRIPTION_MISMATCH")
    print("  Reason: 'ai!n' uses '!' (Takahashi H glyph marker); ZL uses Eva-")
    print("  alphabet which does not encode this distinction. The token does")
    print("  not appear in ZL. P2-CLAIM-012 cannot be cross-checked via ZL.")
    print("  Closest ZL token: 'aiin' (n=" + str(sum(1 for r in records if r['token'] == 'aiin')) + ") — but this is a")
    print("  different token (not the !-marked variant). No substitution valid.")

    ain_result = {
        'token': 'ai!n', 'scope': 'corpus-wide', 'claim_id': 'P2-CLAIM-012',
        'zl_n': ain_zl_count,
        'verdict': 'TRANSCRIPTION_MISMATCH',
        'reason': 'The ! marker in Takahashi H IVTFF notation has no equivalent in ZL Eva- alphabet. aiin (n!=) is a different token.',
        'eva_n': 23, 'eva_mean': 0.686, 'eva_p': 0.005, 'eva_direction': 'LATE',
    }

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("REPLICATION SUMMARY")
    print("=" * 65)
    print(f"{'Claim':<20} {'ZL n':>6} {'ZL mean':>9} {'ZL p':>8} {'Verdict'}")
    print("-" * 65)
    qm = f"{qokain_result['zl_mean']:.3f}" if qokain_result['zl_mean'] is not None else "N/A"
    qp = f"{qokain_result['zl_p']:.3f}" if qokain_result['zl_p'] is not None else "N/A"
    lm = f"{laiin_result['zl_mean']:.3f}" if laiin_result['zl_mean'] is not None else "N/A"
    lp = f"{laiin_result['zl_p']:.3f}" if laiin_result['zl_p'] is not None else "N/A"
    print(f"{'P2-CLAIM-010':<20} {qokain_result['zl_n']:>6} {qm:>9} {qp:>8} {qokain_result['verdict']}")
    print(f"{'P2-CLAIM-011':<20} {laiin_result['zl_n']:>6} {lm:>9} {lp:>8} {laiin_result['verdict']}")
    print(f"{'P2-CLAIM-012':<20} {'0':>6} {'N/A':>9} {'N/A':>8} TRANSCRIPTION_MISMATCH")

    # ── Save results ──────────────────────────────────────────────────────
    output = {
        'metadata': {
            'zl_file': ZL_FILE,
            'total_records': len(records),
            'total_packets': len(all_packets),
            'stars_packets': len(stars_packets),
        },
        'qokain_stars': qokain_result,
        'laiin_stars': laiin_result,
        'ain_corpus': ain_result,
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
