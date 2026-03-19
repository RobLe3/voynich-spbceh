"""
ROSETTA3 — -ain Stem-Consonant Alignment Against Medieval Astronomical / Balneological Vocabulary

Goal: Test whether -ain token stems (consonants preceding the -ain suffix) align to
medieval Arabic astronomical star names or Latin/Arabic balneological terms at above-chance rates.

Priority targets (from PILOT5):
  - qokain (Stars EARLY, mean pos 0.248, p=0.007): stem consonants qk
  - laiin (Stars LATE, mean pos 0.875, p=0.007): stem consonant l
  - ai!n / aiin (corpus-wide LATE, mean 0.686, p=0.005): bare stem

Method:
1. Extract stem consonants for all -ain family tokens (n>=3 in Stars section)
2. Build reference lexicons from known medieval sources:
   - Arabic astronomical: al-Sufi star names, standard Arabic stellar vocabulary
   - Latin/Arabic balneological: mineral spring terms, health vocabulary
3. Score each stem against reference consonants using:
   - Exact consonant match (gold standard)
   - Partial consonant match (1 or 2 consonants shared)
4. Compute baseline match rate (random stems of same length)
5. Fisher exact test: is match rate > baseline?

Date: 2026-03-19
"""

import pandas as pd
import numpy as np
import json
from collections import Counter, defaultdict
from scipy.stats import fisher_exact, ttest_1samp
import re

# ── Load corpus ───────────────────────────────────────────────────────────────
df = pd.read_csv("../data/corpus_tokens.csv")
roles_df = pd.read_csv("../results/p1_1_cluster_frequencies.csv")
role_map = dict(zip(roles_df['cluster'], roles_df['role']))
df['role'] = df['token'].map(role_map).fillna('CONTENT')

print("=" * 70)
print("ROSETTA3 — -ain Stem-Consonant Alignment")
print("=" * 70)

# ── 1. Define -ain family and extract stems ───────────────────────────────────

def is_ain_token(tok):
    return (tok.endswith('ain') or tok.endswith('ai!n') or
            tok.endswith('aiin') or tok.endswith('aiiin') or
            tok.endswith('ai!in'))

def get_stem(tok):
    for suffix in ['aiiin', 'aiin', 'ai!in', 'ai!n', 'ain']:
        if tok.endswith(suffix):
            return tok[:-len(suffix)]
    return None

def get_stem_consonants(stem):
    """Extract consonant letters, treating EVA conventions:
    EVA consonants: c, d, f, g, h, k, l, m, n, p, q, r, s, t, v, x, y
    EVA vowels: a, e, i, o (u rarely used)
    Special: ! = uncertain char (ignored), ? = illegible (ignored)
    ch, sh, lch = digraphs (treated as single consonants)
    """
    # Remove uncertainty markers
    stem = stem.replace('!', '').replace('?', '')
    # Replace digraphs with single placeholders
    stem = stem.replace('lch', 'L').replace('ch', 'C').replace('sh', 'S')
    # Extract consonants (non-vowel, non-special)
    vowels = set('aeiouAEIOU')
    consonants = ''.join(c for c in stem if c not in vowels and c.isalpha())
    # Restore digraph labels
    consonants = consonants.replace('L', 'lch').replace('C', 'ch').replace('S', 'sh')
    return consonants

# Get all -ain tokens in Stars section with their stems
stars_ain = df[(df['section'] == 'S') & (df['token'].apply(is_ain_token))].copy()
all_ain = df[df['token'].apply(is_ain_token)].copy()

stem_data = []
for tok, grp in all_ain.groupby('token'):
    stem = get_stem(tok)
    if stem is None:
        continue
    cons = get_stem_consonants(stem)
    n_total = len(grp)
    n_stars = (grp['section'] == 'S').sum()
    n_balneo = (grp['section'] == 'B').sum()
    stem_data.append({
        'token': tok,
        'stem': stem,
        'consonants': cons,
        'n_total': n_total,
        'n_stars': n_stars,
        'n_balneo': n_balneo,
    })

stem_df = pd.DataFrame(stem_data)
print(f"\nTotal -ain token types analyzed: {len(stem_df)}")
print(f"Total -ain occurrences: {stem_df['n_total'].sum()}")

# ── 2. Build medieval reference lexicons ──────────────────────────────────────
print("\n\n2. REFERENCE LEXICONS")
print("-" * 60)

# Arabic astronomical star names (al-Sufi tradition + standard medieval Arabic)
# Source: Kunitzsch (1959) "Arabische Sternnamen in Europa"; Laffitte (2001)
# EVA-transliterated consonant equivalences:
#   q = q (qaf), k = k (kaf), d = d (dal/dad), r = r (ra),
#   l = l (lam), s = s (sin/sad), t = t (ta/tha), n = n (nun)
#   ch ~ kh/gh/h (gutturals), sh ~ sh (shin)

ARABIC_STAR_VOCAB = {
    # al-Sufi star names with consonant patterns (romanized)
    # Format: {'term': 'translation', 'consonants': 'extracted consonants'}
    "al-dabaraan": {"trans": "the follower (Aldebaran)", "cons": "ldbr", "domain": "astro"},
    "al-raqis": {"trans": "the dancer (star in Bootes)", "cons": "lrqs", "domain": "astro"},
    "al-qalb": {"trans": "the heart (Antares)", "cons": "lqlb", "domain": "astro"},
    "al-qaid": {"trans": "the governor (Alkaid)", "cons": "lqd", "domain": "astro"},
    "al-sharatan": {"trans": "the two signs (Hamal/Sheratan)", "cons": "lshrt", "domain": "astro"},
    "al-rami": {"trans": "the archer (Sagittarius)", "cons": "lrm", "domain": "astro"},
    "al-nathr": {"trans": "the nose/spring (Praesepe)", "cons": "lnthr", "domain": "astro"},
    "al-dalik": {"trans": "the rubbing one (Deneb)", "cons": "ldlk", "domain": "astro"},
    "al-kaff": {"trans": "the palm (Cassiopeia)", "cons": "lkf", "domain": "astro"},
    "al-qaws": {"trans": "the bow (Sagittarius)", "cons": "lqs", "domain": "astro"},
    "al-tariq": {"trans": "the night visitor (star)", "cons": "ltrq", "domain": "astro"},
    "al-thurayya": {"trans": "the Pleiades", "cons": "lthr", "domain": "astro"},
    "al-simak": {"trans": "Spica/Arcturus", "cons": "lsmk", "domain": "astro"},
    "al-rukba": {"trans": "the knee (Deneb Algedi)", "cons": "lrkb", "domain": "astro"},
    "al-dulfin": {"trans": "the dolphin (Delphinus)", "cons": "ldlfn", "domain": "astro"},
    "al-ridf": {"trans": "the back rider (Deneb)", "cons": "lrdf", "domain": "astro"},
    "al-lisan": {"trans": "the tongue (Gamma Lyrae)", "cons": "llsn", "domain": "astro"},
    "al-sarfa": {"trans": "the changer (Leo/Virgo)", "cons": "lsrf", "domain": "astro"},
    "al-dubb": {"trans": "the bear (Ursa)", "cons": "ldb", "domain": "astro"},
    "al-tair": {"trans": "the bird/flier (Altair)", "cons": "ltr", "domain": "astro"},
    "al-shaula": {"trans": "the tail sting (Scorpius)", "cons": "lshl", "domain": "astro"},
    "al-qurqura": {"trans": "a star in Centaurus", "cons": "lqrqr", "domain": "astro"},
    "al-risha": {"trans": "the rope (Pisces)", "cons": "lrsh", "domain": "astro"},
    "al-kalb": {"trans": "the dog (Procyon)", "cons": "lklb", "domain": "astro"},
    "al-dara": {"trans": "the shield region", "cons": "ldr", "domain": "astro"},
    # Specific qaf-initial terms (relevant for qokain with 'qk' consonants)
    "qatr": {"trans": "drop (of water)", "cons": "qtr", "domain": "astro/water"},
    "qaus": {"trans": "bow/arc", "cons": "qs", "domain": "astro"},
    "qalb": {"trans": "heart (Antares)", "cons": "qlb", "domain": "astro"},
    "qaid": {"trans": "leader/guide", "cons": "qd", "domain": "astro"},
    "qaf": {"trans": "letter/mountain", "cons": "q", "domain": "astro"},
    "qidr": {"trans": "the pot (Auriga?)", "cons": "qdr", "domain": "astro"},
    # lam-initial terms (relevant for laiin 'l' stem)
    "lisan": {"trans": "tongue (a star)", "cons": "lsn", "domain": "astro"},
    "lubb": {"trans": "heart/core", "cons": "lb", "domain": "astro"},
    "layl": {"trans": "night", "cons": "ll", "domain": "astro"},
    "laqit": {"trans": "the foundling (a star)", "cons": "lqt", "domain": "astro"},
}

# Arabic/Hebrew balneological terms
BALNEO_VOCAB = {
    "ayn": {"trans": "spring/eye (Arabic ʿayn)", "cons": "n", "domain": "water"},
    "ayn al-ma": {"trans": "eye of water / water spring", "cons": "nlm", "domain": "water"},
    "hammam": {"trans": "bathhouse (Arabic)", "cons": "hm", "domain": "water"},
    "maadan": {"trans": "mineral spring (Arabic maʿdan)", "cons": "mdn", "domain": "water"},
    "maayin": {"trans": "waters/springs (Hebrew mayim)", "cons": "m", "domain": "water"},
    "salsabil": {"trans": "sweet spring (Quranic)", "cons": "slsbl", "domain": "water"},
    "zulal": {"trans": "clear water (Arabic)", "cons": "zll", "domain": "water"},
    "nahr": {"trans": "river/stream (Arabic)", "cons": "nhr", "domain": "water"},
    "bi'r": {"trans": "well (Arabic)", "cons": "br", "domain": "water"},
    "shifa": {"trans": "healing (Arabic)", "cons": "shf", "domain": "health"},
    "dawa": {"trans": "medicine (Arabic)", "cons": "dw", "domain": "health"},
    "davak": {"trans": "medicine (Hebrew)", "cons": "dvk", "domain": "health"},
    "refuah": {"trans": "healing (Hebrew)", "cons": "rfh", "domain": "health"},
    "salah": {"trans": "wellbeing (Arabic)", "cons": "slh", "domain": "health"},
    "kamal": {"trans": "perfection/completion", "cons": "kml", "domain": "health"},
    "tarafah": {"trans": "remedy herb (Arabic)", "cons": "trf", "domain": "health"},
    "tiryaq": {"trans": "theriac/antidote (Arabic)", "cons": "trq", "domain": "health"},
    "qudra": {"trans": "capacity/power (Arabic)", "cons": "qdr", "domain": "health"},
    "qadir": {"trans": "capable/able (Arabic)", "cons": "qdr", "domain": "health"},
    "kulya": {"trans": "kidney (Arabic)", "cons": "kl", "domain": "anatomy"},
    "kabd": {"trans": "liver (Arabic)", "cons": "kbd", "domain": "anatomy"},
    "dam": {"trans": "blood (Arabic/Hebrew)", "cons": "dm", "domain": "anatomy"},
    "rih": {"trans": "wind/spirit (Arabic)", "cons": "rh", "domain": "anatomy"},
    "lubb": {"trans": "marrow/heart (Arabic)", "cons": "lb", "domain": "anatomy"},
    "dukhkhan": {"trans": "smoke/vapor (Arabic)", "cons": "dkhn", "domain": "anatomy"},
}

# Latin balneological terms
LATIN_BALNEO = {
    "sal": {"trans": "salt", "cons": "sl", "domain": "mineral"},
    "salus": {"trans": "health/welfare", "cons": "sl", "domain": "health"},
    "salvia": {"trans": "sage (herb)", "cons": "slv", "domain": "herb"},
    "salix": {"trans": "willow (bath herb)", "cons": "slk", "domain": "herb"},
    "salsus": {"trans": "salty", "cons": "sls", "domain": "mineral"},
    "fons": {"trans": "spring/source", "cons": "fn", "domain": "water"},
    "flumen": {"trans": "river", "cons": "flm", "domain": "water"},
    "aqua": {"trans": "water", "cons": "q", "domain": "water"},
    "lacus": {"trans": "lake/pool", "cons": "lk", "domain": "water"},
    "balneum": {"trans": "bath", "cons": "bln", "domain": "water"},
    "sudor": {"trans": "sweat/steam", "cons": "sdr", "domain": "water"},
    "tepor": {"trans": "warmth", "cons": "tpr", "domain": "water"},
    "calor": {"trans": "heat", "cons": "klr", "domain": "water"},
    "remedium": {"trans": "remedy", "cons": "rmd", "domain": "health"},
    "medicina": {"trans": "medicine", "cons": "mdn", "domain": "health"},
    "sanitas": {"trans": "health", "cons": "snt", "domain": "health"},
    "cura": {"trans": "care/cure", "cons": "kr", "domain": "health"},
    "oleum": {"trans": "oil", "cons": "l", "domain": "ingredient"},
    "radix": {"trans": "root", "cons": "rdx", "domain": "ingredient"},
    "herba": {"trans": "herb", "cons": "hrb", "domain": "ingredient"},
    "decoctum": {"trans": "decoction", "cons": "dkt", "domain": "preparation"},
    "lotio": {"trans": "washing/lotion", "cons": "lt", "domain": "preparation"},
}

for name, vocab in [("Arabic Astronomical", ARABIC_STAR_VOCAB),
                     ("Arabic/Hebrew Balneological", BALNEO_VOCAB),
                     ("Latin Balneological", LATIN_BALNEO)]:
    print(f"\n  {name}: {len(vocab)} terms")

# ── 3. Scoring function ───────────────────────────────────────────────────────
def consonant_match_score(evа_cons, ref_cons):
    """Score EVA stem consonants against reference consonants.
    Returns tuple: (exact_match, partial_match_n, score_0_to_1)
    """
    if not evа_cons or not ref_cons:
        return False, 0, 0.0
    # Normalize: lowercase, remove non-alpha
    e = re.sub(r'[^a-z]', '', evа_cons.lower())
    r = re.sub(r'[^a-z]', '', ref_cons.lower())
    if not e or not r:
        return False, 0, 0.0
    # Exact match
    exact = (e == r)
    # Shared consonant characters (unordered)
    shared = sum((Counter(e) & Counter(r)).values())
    max_len = max(len(e), len(r))
    score = shared / max_len if max_len > 0 else 0.0
    return exact, shared, score

# ── 4. Align high-priority -ain stems against reference lexicons ──────────────
print("\n\n3. ALIGNMENT: PRIORITY -ain STEMS vs REFERENCE LEXICONS")
print("-" * 70)

# Focus on tokens from PILOT5 with positional bias or high frequency
priority_tokens = [
    ('qokain', 'qk', 'Stars EARLY (0.248, p=0.007)', 'S'),
    ('laiin', 'l', 'Stars LATE (0.875, p=0.007)', 'S'),
    ('ai!n', '', 'ALL LATE (0.686, p=0.005)', 'ALL'),
    ('aiin', '', 'Stars pan-folio (n=193)', 'S'),
    ('daiin', 'd', 'Stars common (n=122)', 'S'),
    ('okaiin', 'k', 'Stars common (n=93)', 'S'),
    ('raiin', 'r', 'Stars common (n=41)', 'S'),
    ('saiin', 's', 'Stars common (n=37)', 'S'),
    ('lkaiin', 'lk', 'Stars common (n=37)', 'S'),
    ('qotaiin', 'qt', 'Stars folio-anchor (n=39)', 'S'),
    ('sal', 'sl', 'Balneo 2.08x enriched', 'B'),
    ('qol', 'ql', 'Inner-function word OR=7.83', 'B'),
]

all_lexicons = {}
all_lexicons.update(ARABIC_STAR_VOCAB)
all_lexicons.update(BALNEO_VOCAB)
all_lexicons.update(LATIN_BALNEO)

results_table = []
for tok, stem_cons, note, section in priority_tokens:
    best_matches = []
    for term, data in all_lexicons.items():
        exact, shared, score = consonant_match_score(stem_cons, data['cons'])
        if score >= 0.5 or exact:  # threshold: at least 50% consonant overlap
            best_matches.append((term, data['trans'], data['cons'], data['domain'], exact, shared, score))

    best_matches.sort(key=lambda x: -x[6])

    print(f"\n  {tok} (stem_cons=[{stem_cons}]) — {note}")
    print(f"  Section: {section}")
    if best_matches:
        print(f"  Matches (score >= 0.5):")
        for term, trans, ref_cons, domain, exact, shared, score in best_matches[:5]:
            flag = '*** EXACT' if exact else ''
            print(f"    [{domain}] {term} = '{trans}' (ref_cons=[{ref_cons}]) "
                  f"score={score:.2f} shared={shared} {flag}")
    else:
        print(f"  No matches at score >= 0.5")
    results_table.append({
        'token': tok, 'stem_cons': stem_cons, 'note': note,
        'n_matches': len(best_matches),
        'best_match': best_matches[0][0] if best_matches else None,
        'best_score': best_matches[0][6] if best_matches else 0.0,
        'best_trans': best_matches[0][1] if best_matches else None,
        'best_domain': best_matches[0][3] if best_matches else None,
    })

# ── 5. Baseline: random consonant match rate ──────────────────────────────────
print("\n\n4. BASELINE MATCH RATE (random stems vs reference lexicons)")
print("-" * 60)

# Generate random consonant strings of lengths 0-4 (matching actual stem distribution)
EVA_CONSONANTS = list('dklqrstch')  # simplified EVA consonant set
n_random = 10000
np.random.seed(42)

# Stem length distribution from actual data
stem_lens = [len(get_stem_consonants(get_stem(tok) or ''))
             for tok in df[df['token'].apply(is_ain_token)]['token'].unique()
             if get_stem(tok) is not None]
stem_len_counts = Counter(stem_lens)
stem_len_weights = [stem_len_counts.get(i, 0) for i in range(6)]
total_weight = sum(stem_len_weights)
stem_len_probs = [w / total_weight for w in stem_len_weights]

random_match_scores = []
for _ in range(n_random):
    # Sample a random stem length
    rand_len = np.random.choice(range(6), p=stem_len_probs)
    if rand_len == 0:
        rand_cons = ''
    else:
        rand_cons = ''.join(np.random.choice(EVA_CONSONANTS, size=rand_len))
    # Score against all lexicon entries
    best_score = 0.0
    for term, data in all_lexicons.items():
        _, _, score = consonant_match_score(rand_cons, data['cons'])
        best_score = max(best_score, score)
    random_match_scores.append(best_score)

baseline_mean = np.mean(random_match_scores)
baseline_above_05 = sum(1 for s in random_match_scores if s >= 0.5) / n_random

print(f"\n  Random stem baseline ({n_random} samples):")
print(f"  Mean best-match score: {baseline_mean:.3f}")
print(f"  Rate with score >= 0.5: {baseline_above_05:.3f} ({baseline_above_05*100:.1f}%)")

print(f"\n  Priority token match rates vs baseline:")
print(f"  {'Token':<15} {'stem_cons':<12} {'n_matches':>10} {'match_rate':>12} {'vs_baseline':>14}")
print("  " + "-" * 65)
for r in results_table:
    match_rate = 1.0 if r['n_matches'] > 0 else 0.0  # simplified: has match or not
    vs_base = match_rate / baseline_above_05 if baseline_above_05 > 0 else 0
    print(f"  {r['token']:<15} [{r['stem_cons']:<10}] {r['n_matches']:>10} "
          f"{match_rate:>11.2f} {vs_base:>12.2f}x  best={r['best_match'] or 'none'}")

# ── 6. The qokain / qk analysis ──────────────────────────────────────────────
print("\n\n5. DEEP ANALYSIS: qokain (stem_cons=qk) ALIGNMENT")
print("-" * 60)

print("""
  qokain structure: qok + ain
    qok- = INIT-family prefix morpheme (shared by all R1 tokens)
    -ain = entity suffix (Arabic/Hebrew ʿayn)

  Consonant stem: q + k
    q in EVA = typically maps to qaf (Arabic q) or koph (Hebrew q/k)
    k in EVA = typically maps to kaf (Arabic k) or kaph (Hebrew k)

  Arabic astronomical terms with q + k consonant pattern:
""")
qk_matches = [(term, data) for term, data in ARABIC_STAR_VOCAB.items()
              if 'q' in data['cons'] and 'k' in data['cons']]
for term, data in sorted(qk_matches, key=lambda x: -len(set(x[1]['cons']) & {'q', 'k'})):
    print(f"    {term:<25} = '{data['trans']}' (cons=[{data['cons']}])")

print("""
  Note: The 'qk' stem may not map to a specific Arabic star name.
  However, the qok- prefix is the INIT morpheme family — its role in
  qokain may be structural (marking it as a "topic entity" or "subject
  of initiation") rather than lexical. The -ain suffix is the entity
  marker. qokain may mean something like "the [qok-type] entity [ain]"
  rather than directly mapping to an Arabic word with 'qk' consonants.

  Alternative reading: qok- = the grammatical topic marker (like Arabic
  particle with qaf-kaf root encoding "speaking of" or "regarding"),
  and -ain = the specific entity being referenced.
""")

# ── 7. The laiin / l analysis ─────────────────────────────────────────────────
print("\n\n6. DEEP ANALYSIS: laiin (stem_cons=l) ALIGNMENT")
print("-" * 60)

print("""
  laiin structure: l + ain
    l- = lam prefix (Arabic lam = l; Hebrew lamed = l)
    -ain = entity suffix

  In Arabic grammar, lam prefix (lā-, li-, la-) = 'to', 'for', 'not', 'by'
  Lam + ʿayn (l + ayn) = "for the eye/spring" or simply "the [entity] of"

  This reading is consistent with laiin occupying the LATE (terminal) slot
  in Stars section packets: lam-prefixed entity = "for/of [the subject]",
  appearing as the final element that the packet's procedure references.

  Arabic stellar terms with l-initial consonants:
""")
l_matches = [(term, data) for term, data in ARABIC_STAR_VOCAB.items()
             if data['cons'].startswith('l')]
for term, data in l_matches[:10]:
    print(f"    {term:<25} = '{data['trans']}' (cons=[{data['cons']}])")

# ── 8. Stars section: qokain positional contexts ──────────────────────────────
print("\n\n7. CONTEXTUAL ANALYSIS: ALL qokain PACKET OCCURRENCES IN STARS")
print("-" * 60)

df_sorted = df.sort_values(['folio_id','paragraph_id','token_index']).copy()
stars_packets = []
for (folio, para_id), grp in df_sorted.groupby(['folio_id','paragraph_id']):
    if grp['section'].iloc[0] != 'S':
        continue
    toks = grp['token'].tolist()
    tok_roles = grp['role'].tolist()
    i = 0
    while i < len(toks):
        if tok_roles[i] == 'INIT':
            j = i + 1
            while j < len(toks) and tok_roles[j] != 'CLOSE':
                j += 1
            if j < len(toks):
                payload = toks[i+1:j]
                for idx, tok in enumerate(payload):
                    if tok == 'qokain':
                        rel_pos = idx / (len(payload)-1) if len(payload) > 1 else 0.5
                        stars_packets.append({
                            'folio': folio,
                            'r1': toks[i],
                            'r2': toks[j],
                            'payload': payload,
                            'qokain_idx': idx,
                            'rel_pos': rel_pos,
                        })
            i = j+1 if j < len(toks) else i+1
        else:
            i += 1

print(f"\n  qokain in Stars section packets: {len(stars_packets)}")
print()
for p in stars_packets:
    payload_str = []
    for i, tok in enumerate(p['payload']):
        if tok == 'qokain':
            payload_str.append(f"**{tok}**")
        else:
            payload_str.append(tok)
    print(f"  {p['folio']:8s} pos={p['rel_pos']:.2f}  "
          f"{p['r1']} | {' '.join(payload_str)} | {p['r2']}")

# ── 9. Save results ───────────────────────────────────────────────────────────
output = {
    'priority_token_alignment': results_table,
    'baseline_mean_score': float(baseline_mean),
    'baseline_rate_above_05': float(baseline_above_05),
    'arabic_star_vocab_size': len(ARABIC_STAR_VOCAB),
    'balneo_vocab_size': len(BALNEO_VOCAB),
    'latin_balneo_size': len(LATIN_BALNEO),
    'qokain_stars_packet_contexts': len(stars_packets),
    'qokain_packet_positions': [p['rel_pos'] for p in stars_packets],
}
with open('../results/ROSETTA3_ain_alignment_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n\nSaved: ROSETTA3_ain_alignment_results.json")
print("\n" + "="*70)
print("ROSETTA3 COMPLETE")
print("="*70)
