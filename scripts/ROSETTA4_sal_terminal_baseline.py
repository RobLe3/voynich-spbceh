"""
ROSETTA4 — sal terminal-entity pattern: baseline test
Tests whether sal's 24% pre-R2 rate in Balneological packets is above baseline.

Method:
  1. Reconstruct all Balneological packets (R1 → payload → R2)
  2. For each content token appearing in B packets, measure its rate of
     appearing immediately before the R2 CLOSE token
  3. Compare sal's rate to the distribution across all tokens
  4. If sal is in the top 5% → terminal-entity hypothesis strengthened
  5. Analyze the 1–3 tokens PRECEDING sal in terminal position:
     are they ingredient/action clusters?
  6. Full listing of all packets containing sal
"""

import json
import csv
from pathlib import Path
from collections import defaultdict, Counter
import statistics

DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results"

# Role assignments (R1 = INIT, R2 = CLOSE)
R1_TOKENS = {'qokeedy','qokeey','qokedy','qokeedy','qokedy','qokal','qokar',
             'qokain','qokaiin','qokchey','qokol','qokchy','qokedy',
             'qokeody','qokeeody','qokeey','qoky','qoke','qoked'}

R2_TOKENS = {'chedy','shedy','lchedy','cheody','sheody','lcheody',
             'chey','shey','lchey','cheey','sheey','lcheey',
             'chdaiin','shdaiin','lchdaiin','cheol','sheol','lcheol',
             'chol','shol','lchol','chy','shy','lchy',
             'chd','shd','lchd','cheedy','sheedy','lcheedy',
             'ched','shed','lched','cheo','sheo','lcheo',
             'cheeol','sheeol','lcheeol','chkal','shkal','lchkal',
             'chor','shor','lchor'}

# Load corpus
token_records = []
with open(DATA_DIR / "corpus_tokens.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        token_records.append(row)

print(f"Corpus: {len(token_records)} tokens")

# ============================================================
# 1. RECONSTRUCT BALNEOLOGICAL PACKETS
# ============================================================

balneo_records = [r for r in token_records if r['section'] == 'B']
print(f"Balneological tokens: {len(balneo_records)}")

# Group by paragraph_id (packets span lines within a paragraph)
para_groups = defaultdict(list)
for r in balneo_records:
    para_key = (r['folio_id'], r['paragraph_id'])
    para_groups[para_key].append(r)

# Reconstruct packets within each paragraph
def reconstruct_packets(records):
    """Find R1→payload→R2 sequences."""
    packets = []
    i = 0
    while i < len(records):
        tok = records[i]['token']
        if tok in R1_TOKENS:
            # Find next R2
            j = i + 1
            while j < len(records) and records[j]['token'] not in R2_TOKENS:
                j += 1
            if j < len(records):
                init_tok = tok
                close_tok = records[j]['token']
                payload = records[i+1:j]
                packets.append({
                    'folio_id': records[i]['folio_id'],
                    'init': init_tok,
                    'payload': [r['token'] for r in payload],
                    'close': close_tok,
                    'payload_records': payload
                })
                i = j + 1
            else:
                i += 1
        else:
            i += 1
    return packets

all_B_packets = []
for para_key, records in para_groups.items():
    all_B_packets.extend(reconstruct_packets(records))

print(f"Reconstructed {len(all_B_packets)} Balneological packets")

# ============================================================
# 2. PRE-R2 RATE FOR ALL TOKENS (baseline computation)
# ============================================================

print("\n2. PRE-R2 RATE — ALL TOKENS IN B PACKETS")
print("-" * 60)

# For each packet, record which token immediately precedes R2
pre_r2_tokens = []
all_payload_tokens = []

for pkt in all_B_packets:
    payload = pkt['payload']
    if payload:
        pre_r2_tokens.append(payload[-1])  # last payload token = immediately before R2
    all_payload_tokens.extend(payload)

pre_r2_count = Counter(pre_r2_tokens)
payload_total = Counter(all_payload_tokens)

# Rate = times in pre-R2 position / times in any payload position
token_pre_r2_rates = {}
for tok, count_in_pre_r2 in pre_r2_count.items():
    total_in_payload = payload_total.get(tok, 0)
    if total_in_payload >= 3:  # minimum frequency threshold
        rate = count_in_pre_r2 / total_in_payload
        token_pre_r2_rates[tok] = {
            'token': tok,
            'count_pre_r2': count_in_pre_r2,
            'count_in_payload': total_in_payload,
            'pre_r2_rate': rate
        }

# Sort by rate
sorted_rates = sorted(token_pre_r2_rates.items(), key=lambda x: -x[1]['pre_r2_rate'])

print(f"  Tokens in any B-packet payload (freq >= 3): {len(token_pre_r2_rates)}")
print(f"  Total payload slots analyzed: {len(all_payload_tokens)}")
print(f"  Total pre-R2 slots: {len(pre_r2_tokens)}")

# Overall baseline
all_rates = [v['pre_r2_rate'] for v in token_pre_r2_rates.values()]
baseline_mean = statistics.mean(all_rates)
baseline_median = statistics.median(all_rates)
baseline_p95 = sorted(all_rates)[int(len(all_rates) * 0.95)]
baseline_p90 = sorted(all_rates)[int(len(all_rates) * 0.90)]
baseline_p80 = sorted(all_rates)[int(len(all_rates) * 0.80)]

print(f"\n  Baseline pre-R2 rate distribution:")
print(f"    Mean:   {baseline_mean:.3f}")
print(f"    Median: {baseline_median:.3f}")
print(f"    p80:    {baseline_p80:.3f}")
print(f"    p90:    {baseline_p90:.3f}")
print(f"    p95:    {baseline_p95:.3f}")

# sal's rate
sal_data = token_pre_r2_rates.get('sal', None)
if sal_data:
    sal_rate = sal_data['pre_r2_rate']
    sal_rank = sum(1 for r in all_rates if r > sal_rate)
    sal_percentile = sal_rank / len(all_rates)
    print(f"\n  sal specifically:")
    print(f"    pre-R2 count: {sal_data['count_pre_r2']}")
    print(f"    payload count: {sal_data['count_in_payload']}")
    print(f"    pre-R2 rate: {sal_rate:.3f} ({sal_rate*100:.1f}%)")
    print(f"    rank: top {sal_percentile*100:.1f}% of all tokens")
    print(f"    vs baseline mean: {sal_rate / baseline_mean:.2f}×")
    print(f"    vs baseline p90: {'ABOVE' if sal_rate > baseline_p90 else 'BELOW'}")
    print(f"    vs baseline p95: {'ABOVE' if sal_rate > baseline_p95 else 'BELOW'}")
else:
    sal_rate = None
    print(f"\n  sal: not found in payload tokens with freq >= 3")

print(f"\n  Top 20 tokens by pre-R2 rate (freq >= 3 in payload):")
print(f"  {'Token':15s} {'pre-R2':6s} {'total':6s} {'rate':8s}")
for tok, data in sorted_rates[:20]:
    marker = " <-- SAL" if tok == 'sal' else ""
    print(f"  {tok:15s} {data['count_pre_r2']:6d} {data['count_in_payload']:6d} "
          f"{data['pre_r2_rate']:8.3f}{marker}")

# ============================================================
# 3. PACKETS CONTAINING SAL — FULL LISTING
# ============================================================

print("\n\n3. ALL BALNEOLOGICAL PACKETS CONTAINING sal")
print("-" * 60)

sal_packets = [p for p in all_B_packets if 'sal' in p['payload']]
print(f"  Packets containing sal: {len(sal_packets)} / {len(all_B_packets)} total")

terminal_sal = 0
non_terminal_sal = 0

for i, pkt in enumerate(sal_packets):
    payload = pkt['payload']
    sal_positions = [j for j, t in enumerate(payload) if t == 'sal']
    is_terminal = payload[-1] == 'sal' if payload else False
    if is_terminal:
        terminal_sal += 1
    else:
        non_terminal_sal += 1

    print(f"\n  Packet {i+1} [{pkt['folio_id']}]:")
    print(f"    {pkt['init']} | {' '.join(payload)} | {pkt['close']}")
    for pos in sal_positions:
        rel_pos = pos / (len(payload) - 1) if len(payload) > 1 else 0.5
        pre_context = payload[max(0, pos-3):pos]
        post_context = payload[pos+1:min(len(payload), pos+4)]
        terminal_flag = " *** TERMINAL (pre-R2)" if pos == len(payload) - 1 else ""
        print(f"    sal at index {pos}/{len(payload)-1} (rel={rel_pos:.2f}){terminal_flag}")
        print(f"    context: ...{' '.join(pre_context)} [SAL] {' '.join(post_context)}...")

print(f"\n  Terminal sal (immediately before R2): {terminal_sal}/{len(sal_packets)} ({terminal_sal/max(len(sal_packets),1)*100:.1f}%)")
print(f"  Non-terminal sal: {non_terminal_sal}/{len(sal_packets)}")

# ============================================================
# 4. PRE-SAL CONTEXT (tokens preceding sal in terminal position)
# ============================================================

print("\n\n4. CONTEXT ANALYSIS — TOKENS PRECEDING TERMINAL sal")
print("-" * 60)

pre_sal_1 = []  # token immediately before terminal sal
pre_sal_2 = []  # token 2 before terminal sal
pre_sal_3 = []  # token 3 before terminal sal

for pkt in sal_packets:
    payload = pkt['payload']
    if payload and payload[-1] == 'sal':
        # sal is terminal
        if len(payload) >= 2:
            pre_sal_1.append(payload[-2])
        if len(payload) >= 3:
            pre_sal_2.append(payload[-3])
        if len(payload) >= 4:
            pre_sal_3.append(payload[-4])

if pre_sal_1:
    print(f"  Token immediately before terminal sal (n={len(pre_sal_1)}):")
    for tok, cnt in Counter(pre_sal_1).most_common(10):
        print(f"    {tok}: {cnt}")

if pre_sal_2:
    print(f"  Token 2 before terminal sal (n={len(pre_sal_2)}):")
    for tok, cnt in Counter(pre_sal_2).most_common(10):
        print(f"    {tok}: {cnt}")

# Compare to overall pre-R2 context (what precedes the R2 token in general)
print(f"\n  Overall most common tokens in payload (B section, all packets):")
for tok, cnt in payload_total.most_common(15):
    print(f"    {tok}: {cnt}")

# ============================================================
# 5. SAL VS STRUCTURAL TOKENS: POSITION DISTRIBUTION
# ============================================================

print("\n\n5. SAL POSITION DISTRIBUTION IN B PACKETS")
print("-" * 60)

sal_positions_in_payload = []
for pkt in sal_packets:
    payload = pkt['payload']
    for j, t in enumerate(payload):
        if t == 'sal':
            rel = j / (len(payload) - 1) if len(payload) > 1 else 0.5
            sal_positions_in_payload.append(rel)

if sal_positions_in_payload:
    mean_pos = statistics.mean(sal_positions_in_payload)
    print(f"  sal mean position in B-packet payloads: {mean_pos:.3f}")
    print(f"  (0.0=first token, 1.0=immediately before R2)")
    print(f"  N positions: {len(sal_positions_in_payload)}")

    # t-test against 0.5
    from scipy import stats
    t_stat, p_val = stats.ttest_1samp(sal_positions_in_payload, 0.5)
    print(f"  t-test vs 0.5: t={t_stat:.3f}, p={p_val:.3f}")
    if p_val < 0.05:
        bias = "LATE" if mean_pos > 0.5 else "EARLY"
        print(f"  → {bias}-biased (p<0.05)")
    else:
        print(f"  → No significant positional bias vs. 0.5")

# ============================================================
# 6. MORPHOLOGICAL FAMILY OF sal IN B PACKETS
# ============================================================

print("\n\n6. sal MORPHOLOGICAL FAMILY IN B PACKETS")
print("-" * 60)

# Find all sl-initial tokens in B payload
sl_family_B = Counter()
for pkt in all_B_packets:
    for t in pkt['payload']:
        if t.startswith('s') and 'l' in t[:4]:
            sl_family_B[t] += 1

print(f"  sl-consonant tokens in B packet payloads (top 20):")
for tok, cnt in sl_family_B.most_common(20):
    is_sal = " <-- sal" if tok == 'sal' else ""
    print(f"    {tok}: {cnt}{is_sal}")

# ============================================================
# 7. FALSIFICATION CHECK: is sal's pre-R2 rate significantly above chance?
# ============================================================

print("\n\n7. FALSIFICATION CHECK")
print("-" * 60)

if sal_data:
    # How many tokens have rate >= sal's rate?
    n_at_or_above = sum(1 for r in all_rates if r >= sal_rate)
    print(f"  sal pre-R2 rate: {sal_rate:.3f}")
    print(f"  Tokens with rate >= sal: {n_at_or_above} / {len(all_rates)}")
    print(f"  Fraction: {n_at_or_above/len(all_rates):.3f}")
    print()
    if n_at_or_above / len(all_rates) < 0.20:
        print("  → sal is in the TOP 20% of all tokens by pre-R2 rate.")
        print("    Terminal-entity pattern is ABOVE baseline.")
    elif n_at_or_above / len(all_rates) < 0.40:
        print("  → sal is above median but not clearly above baseline.")
    else:
        print("  → sal's pre-R2 rate is NOT exceptional — many tokens match or exceed it.")
        print("    Terminal-entity hypothesis is NOT supported by this test.")

    # Show tokens with similarly high or higher rates
    print(f"\n  Tokens with pre-R2 rate >= {sal_rate:.3f}:")
    for tok, data in sorted_rates:
        if data['pre_r2_rate'] >= sal_rate:
            marker = " <-- sal" if tok == 'sal' else ""
            print(f"    {tok:15s} rate={data['pre_r2_rate']:.3f} "
                  f"({data['count_pre_r2']}/{data['count_in_payload']}){marker}")

# ============================================================
# SAVE RESULTS
# ============================================================

output = {
    'n_B_packets': len(all_B_packets),
    'sal_packets_found': len(sal_packets),
    'terminal_sal_count': terminal_sal,
    'terminal_sal_rate': terminal_sal / max(len(sal_packets), 1),
    'baseline_mean_pre_r2_rate': baseline_mean,
    'baseline_p90': baseline_p90,
    'baseline_p95': baseline_p95,
    'sal_pre_r2_rate': sal_rate,
    'sal_count_pre_r2': sal_data['count_pre_r2'] if sal_data else None,
    'sal_count_in_payload': sal_data['count_in_payload'] if sal_data else None,
    'top_20_pre_r2_tokens': [{'token': tok, **data} for tok, data in sorted_rates[:20]],
    'sal_mean_position': mean_pos if sal_positions_in_payload else None,
    'pre_sal_terminal_context': {
        'n1': Counter(pre_sal_1).most_common(5),
        'n2': Counter(pre_sal_2).most_common(5),
    }
}

with open(RESULTS_DIR / "ROSETTA4_sal_terminal_results.json", 'w') as f:
    json.dump(output, f, indent=2, default=str)

print("\n\nSaved: ROSETTA4_sal_terminal_results.json")
print("=" * 60)
print("ROSETTA4 COMPLETE")
print("=" * 60)
