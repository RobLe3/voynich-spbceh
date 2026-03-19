"""
PILOT1 — Five-Folio Three-Layer Analysis
Phase 2 Step 4: f75r (Balneo), f88r (Pharma), f103r (Recipe), f111v & f114v (Stars)

For each folio:
- Parse paragraphs with FSA → INIT / PAYLOAD / CLOSE sequences
- Label Layer 1 frame tokens (R1/R2/R6)
- Flag Layer 2 inner-function-word candidates (qol, kal, kol)
- List Layer 3 Rosetta tokens with enrichment context
- Output Markdown table per folio

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import defaultdict

# ── Load data ──────────────────────────────────────────────────────────────
df = pd.read_csv("D1_corpus/corpus_tokens.csv")
struct_df = pd.read_csv("P1_structural/p1_1_cluster_frequencies.csv")
STRUCT = set(struct_df['cluster'].tolist())

# Role assignments from cluster freq table
role_map = dict(zip(struct_df['cluster'], struct_df['role']))

# Layer definitions
LAYER1_R1 = {t for t in STRUCT if role_map.get(t) == 'INIT'}
LAYER1_R2 = {t for t in STRUCT if role_map.get(t) == 'CLOSE'}
LAYER1_R6 = {t for t in STRUCT if role_map.get(t) == 'REF'}
LAYER1_R3 = {t for t in STRUCT if role_map.get(t) == 'LINK'}

LAYER2_CANDIDATES = {'qol', 'kal', 'kol', 'okol', 'qokeol', 'al', 'sal'}
# sal included as ambiguous — may be Layer 2 or 3

# Layer 3: top Rosetta candidates from ILLUS1
LAYER3_ROSETTA = {
    'qokain': ('Balneological', 9.6), 'qoteedy': ('Balneological', 6.9),
    'cheedy': ('Balneological', 5.9), 'oly': ('Balneological', 5.3),
    'qol': ('Balneological', 5.1), 'sal': ('Balneological', 3.54),
    'okai!n': ('Stars', 4.2), 'qotaiin': ('Stars', 3.8),
    'ain': ('All', 1.0), 'ar': ('All', 1.0),
}

TARGET_FOLIOS = ['f75r', 'f88r', 'f103r', 'f111v', 'f114v']

def classify_token(tok):
    """Return (layer, role_or_label) for a token."""
    if tok in LAYER1_R1:
        return (1, 'R1-INIT')
    elif tok in LAYER1_R2:
        return (1, 'R2-CLOSE')
    elif tok in LAYER1_R6:
        return (1, 'R6-REF')
    elif tok in LAYER1_R3:
        return (1, 'R3-LINK')
    elif tok in STRUCT:
        return (1, 'R4/R5')
    elif tok in LAYER2_CANDIDATES:
        return (2, 'fn-word')
    elif tok in LAYER3_ROSETTA:
        return (3, f'Rosetta({LAYER3_ROSETTA[tok][0]}×{LAYER3_ROSETTA[tok][1]})')
    else:
        return (4, 'content')

def fsa_parse_paragraph(tokens):
    """
    Simple FSA: IDLE → OPEN (on R1) → PAYLOAD (R3/R4/R5/R6) → CLOSED (on R2) → OPEN...
    Returns list of (state, token) and packet count.
    """
    state = 'IDLE'
    sequence = []
    packets = []
    current_packet = []
    violations = 0

    for tok in tokens:
        layer, label = classify_token(tok)
        if label == 'R1-INIT':
            if state == 'IDLE' or state == 'CLOSED':
                state = 'OPEN'
                current_packet = [tok]
            else:  # R1 while OPEN or PAYLOAD — violation / nested
                violations += 1
                current_packet.append(tok)
            sequence.append(('OPEN', tok))
        elif label == 'R2-CLOSE':
            if state in ('OPEN', 'PAYLOAD'):
                current_packet.append(tok)
                packets.append(current_packet)
                current_packet = []
                state = 'CLOSED'
            else:
                violations += 1
                sequence.append(('VIOLATION', tok))
                continue
            sequence.append(('CLOSE', tok))
        else:
            if state == 'OPEN':
                state = 'PAYLOAD'
            current_packet.append(tok)
            sequence.append((state if state in ('PAYLOAD','IDLE','CLOSED') else 'PAYLOAD', tok))

    return sequence, packets, violations

def format_token(tok):
    layer, label = classify_token(tok)
    if layer == 1 and 'R1' in label:
        return f'**[R1]{tok}**'
    elif layer == 1 and 'R2' in label:
        return f'**[R2]{tok}**'
    elif layer == 1 and 'R6' in label:
        return f'**[R6]{tok}**'
    elif layer == 1:
        return f'[{tok}]'
    elif layer == 2:
        return f'_{tok}_'
    elif layer == 3:
        return f'***{tok}***'
    else:
        return tok

lines_df = df.groupby(['folio_id', 'line_id'])['token'].apply(list).reset_index()
lines_df.columns = ['folio_id', 'line_id', 'tokens']
lines_df['section'] = df.groupby(['folio_id', 'line_id'])['section'].first().values

para_df = df.groupby(['folio_id', 'paragraph_id'])['token'].apply(list).reset_index()
para_df.columns = ['folio_id', 'paragraph_id', 'tokens']
para_df['section'] = df.groupby(['folio_id', 'paragraph_id'])['section'].first().values

output_sections = []

for folio in TARGET_FOLIOS:
    folio_df = para_df[para_df['folio_id'] == folio].copy()
    if len(folio_df) == 0:
        # Try line-level
        folio_df = lines_df[lines_df['folio_id'] == folio].copy()
        folio_df.columns = ['folio_id', 'paragraph_id', 'tokens', 'section']

    section = folio_df['section'].iloc[0] if len(folio_df) > 0 else '?'
    total_tokens = sum(len(r) for r in folio_df['tokens'])

    # Token layer counts
    layer_counts = defaultdict(int)
    token_list_all = [t for row in folio_df['tokens'] for t in row]
    for tok in token_list_all:
        layer, _ = classify_token(tok)
        layer_counts[layer] += 1

    # FSA analysis
    all_packets = []
    all_violations = 0
    para_results = []

    for _, row in folio_df.iterrows():
        toks = row['tokens']
        seq, packets, violations = fsa_parse_paragraph(toks)
        all_packets.extend(packets)
        all_violations += violations

        # Build annotated line
        annotated = ' '.join(format_token(t) for t in toks)
        l1 = [t for t in toks if classify_token(t)[0] == 1]
        l2 = [t for t in toks if classify_token(t)[0] == 2]
        l3 = [t for t in toks if classify_token(t)[0] == 3]

        # Role sequence (just the structural tokens)
        role_seq = ' → '.join(classify_token(t)[1] for t in toks if classify_token(t)[0] == 1)
        if not role_seq:
            role_seq = '(no frame tokens)'

        para_results.append({
            'para': row['paragraph_id'],
            'n_tokens': len(toks),
            'annotated': annotated,
            'role_seq': role_seq,
            'l1': ', '.join(l1) if l1 else '—',
            'l2': ', '.join(l2) if l2 else '—',
            'l3': ', '.join(set(l3)) if l3 else '—',
            'n_packets': len(packets),
            'violations': violations,
        })

    # Rosetta tokens on this folio
    folio_tokens = [t for row in folio_df['tokens'] for t in row]
    rosetta_on_folio = {t: folio_tokens.count(t) for t in LAYER3_ROSETTA if t in folio_tokens}
    layer2_on_folio = {t: folio_tokens.count(t) for t in LAYER2_CANDIDATES if t in folio_tokens}

    # Build markdown section
    md = [f"\n## Folio {folio} (Section: {section})\n"]
    md.append(f"**Tokens**: {total_tokens} | **Paragraphs/lines**: {len(folio_df)} | "
              f"**Complete packets**: {len(all_packets)} | **FSA violations**: {all_violations}\n")
    md.append(f"**Layer distribution**: L1-frame={layer_counts[1]} ({layer_counts[1]/max(total_tokens,1)*100:.1f}%), "
              f"L2-fnword={layer_counts[2]} ({layer_counts[2]/max(total_tokens,1)*100:.1f}%), "
              f"L3-rosetta={layer_counts[3]} ({layer_counts[3]/max(total_tokens,1)*100:.1f}%), "
              f"L4-content={layer_counts[4]} ({layer_counts[4]/max(total_tokens,1)*100:.1f}%)\n")

    if rosetta_on_folio:
        md.append("**Layer 3 Rosetta tokens present**: " +
                  ", ".join(f"`{t}`×{n}" for t,n in sorted(rosetta_on_folio.items(), key=lambda x:-x[1])) + "\n")
    if layer2_on_folio:
        md.append("**Layer 2 function-word candidates**: " +
                  ", ".join(f"`{t}`×{n}" for t,n in sorted(layer2_on_folio.items(), key=lambda x:-x[1])) + "\n")

    md.append("\n### Paragraph-level three-layer breakdown\n")
    md.append("| Para | Tokens | Role sequence (L1 frame) | L2 fn-words | L3 Rosetta | Packets |\n")
    md.append("|------|--------|--------------------------|-------------|------------|--------|\n")
    for pr in para_results[:15]:  # limit to first 15 paragraphs
        md.append(f"| {pr['para']} | {pr['n_tokens']} | {pr['role_seq'][:60]} | {pr['l2'][:30]} | {pr['l3'][:30]} | {pr['n_packets']} |\n")

    if all_packets:
        md.append(f"\n### Complete packets on this folio ({len(all_packets)} total)\n")
        for i, pkt in enumerate(all_packets[:5]):
            annotated_pkt = ' '.join(format_token(t) for t in pkt)
            md.append(f"- Packet {i+1}: {annotated_pkt}\n")

    output_sections.append(''.join(md))

# Write output
header = """# Five-Folio Three-Layer Pilot Analysis
**Phase 2 Step 4 — SPBCEH v2.0**
**Date**: 2026-03-19

## Notation

- `**[R1]token**` — Layer 1, R1 Initiator-like (frame)
- `**[R2]token**` — Layer 1, R2 Closure-like (frame)
- `**[R6]token**` — Layer 1, R6 Reference-like (frame)
- `[token]` — Layer 1, other structural role
- `_token_` — Layer 2, inner-packet function word candidate
- `***token***` — Layer 3, Rosetta lexical entity
- `token` — Layer 4, unclassified content

## Folios Analyzed

- **f75r** — Biological/Balneological (B)
- **f88r** — Pharmaceutical (P)
- **f103r** — Stars/Recipes (S)
- **f111v** — Stars/Recipes (S)
- **f114v** — Stars/Recipes (S)

---
"""

full_output = header + '\n'.join(output_sections)
with open('PILOT1_five_folio_results.md', 'w') as f:
    f.write(full_output)

print("PILOT1 complete. Output: PILOT1_five_folio_results.md")
print(f"\nSummary by folio:")
for folio in TARGET_FOLIOS:
    folio_rows = para_df[para_df['folio_id'] == folio]
    if len(folio_rows) == 0:
        folio_rows = lines_df[lines_df['folio_id'] == folio]
    n_tok = sum(len(r) for r in folio_rows['tokens']) if len(folio_rows) > 0 else 0
    section = folio_rows['section'].iloc[0] if len(folio_rows) > 0 else '?'
    print(f"  {folio} ({section}): {n_tok} tokens, {len(folio_rows)} units")
