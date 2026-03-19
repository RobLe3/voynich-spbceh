#!/usr/bin/env python3
"""
D1 Corpus Parser: IVTFF format parser for Voynich Manuscript analysis (SPBCEH project).
Primary source: Lsi_ivtff_0d_v4j_fixed.txt
Output: structured CSV with per-token fields for SPBCEH role analysis.
"""

import re
import csv
import json
from collections import defaultdict
from pathlib import Path

# ──────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
CORPUS_FILE = BASE_DIR / "data" / "Lsi_ivtff_0d_v4j_fixed.txt"
OUT_DIR = BASE_DIR / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Use the Takahashi transcription (;H in this file = Stolfi/Landini harmonized baseline)
# After checking, ;H is the primary Stolfi transcription.
# We'll extract ALL transcribers but flag which is primary.
PRIMARY_TRANSCRIBER = "H"

# ──────────────────────────────────────────────────────────
# Regex patterns
# ──────────────────────────────────────────────────────────

# Page header: <fXXX>   <! $I=T $Q=A $P=A $L=A $H=1 ...>
PAGE_HEADER_RE = re.compile(
    r'^<(f\w+)>\s+<!([^>]*)>',
)

# Data line locator: <f1r.1,@P0;H> — para markers: @,+,*,=,&,~,/
DATA_LINE_RE = re.compile(
    r'^<(f[\w.]+)\.([\w.]+),([@+*=&~\/])([\w]+);(\w+)>\s+(.*)',
)

# Attribute parser for page headers
ATTR_RE = re.compile(r'\$(\w+)=(\S+)')

# ──────────────────────────────────────────────────────────
# Parser
# ──────────────────────────────────────────────────────────

def parse_ivtff(corpus_path: Path, primary_transcriber: str = "H"):
    """
    Parse IVTFF interlinear file.
    Returns:
      - tokens_rows: list of dicts, one per token
      - folio_meta: dict folio_id -> {section, currier, hand, quire, panel}
      - stats: summary stats dict
    """
    folio_meta = {}  # folio_id -> metadata dict
    current_folio_meta = {}
    current_folio = None

    tokens_rows = []
    line_rows = []

    # Paragraph tracking
    paragraph_id = 0
    in_paragraph = False

    total_lines_parsed = 0
    total_tokens = 0
    skipped_lines = 0

    transcriber_counts = defaultdict(int)

    with open(corpus_path, encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            line = raw_line.rstrip("\n")

            # Skip comments
            if line.startswith("#"):
                continue
            if not line.strip():
                continue

            # Page header line: <fXXX>  <! $I=... ...>
            ph_match = PAGE_HEADER_RE.match(line)
            if ph_match:
                current_folio = ph_match.group(1)
                attrs_str = ph_match.group(2)
                attrs = dict(ATTR_RE.findall(attrs_str))
                current_folio_meta = {
                    "folio_id": current_folio,
                    "section": attrs.get("I", "?"),
                    "currier": attrs.get("L", "?"),
                    "hand": attrs.get("H", "?"),
                    "quire": attrs.get("Q", "?"),
                    "panel": attrs.get("P", "?"),
                }
                folio_meta[current_folio] = current_folio_meta
                continue

            # Data line
            dl_match = DATA_LINE_RE.match(line)
            if not dl_match:
                skipped_lines += 1
                continue

            folio_id_raw = dl_match.group(1)
            line_num = dl_match.group(2)
            para_marker = dl_match.group(3)  # @, +, *, =
            unit_code = dl_match.group(4)    # P0, Pt, etc.
            transcriber = dl_match.group(5)  # H, C, F, N, U, etc.
            eva_raw = dl_match.group(6).strip()

            transcriber_counts[transcriber] += 1

            # Only process primary transcriber for analysis
            if transcriber != primary_transcriber:
                continue

            total_lines_parsed += 1

            # Get folio metadata (may need to look up parent folio)
            # e.g. folio_id_raw = "f1r" (for data lines, matches the page header)
            base_folio = re.match(r"(f\w+)", folio_id_raw).group(1)
            meta = folio_meta.get(base_folio, {
                "folio_id": base_folio,
                "section": "?",
                "currier": "?",
                "hand": "?",
                "quire": "?",
                "panel": "?",
            })

            # Paragraph tracking
            if para_marker in ("@", "*"):
                paragraph_id += 1
                in_paragraph = True

            # Determine line type from para_marker and unit_code terminal character
            is_paragraph_start = para_marker in ("@", "*")
            is_paragraph_end = (para_marker == "=") or eva_raw.endswith("=")
            is_continuation = para_marker == "+"

            # Strip terminal line markers from EVA text
            eva_clean = eva_raw.rstrip("=-")
            # Strip trailing <$> (end-of-text marker)
            eva_clean = eva_clean.replace("<$>", "").strip()
            # Remove {comment} blocks
            eva_clean = re.sub(r'\{[^}]*\}', '', eva_clean)
            # Remove <...> special markers (illegible, etc.)
            eva_clean = re.sub(r'<[^>]*>', '!', eva_clean)
            # Normalize multiple ! to single
            eva_clean = re.sub(r'!+', '!', eva_clean)

            # Tokenize: split on '.' (word boundary)
            # ',' is an in-line pause — treat as word boundary too
            raw_tokens = re.split(r'[.,]', eva_clean)
            # Filter empty tokens
            tokens = [t.strip() for t in raw_tokens if t.strip()]

            n_tokens = len(tokens)
            total_tokens += n_tokens

            # Assign positional labels
            for i, token in enumerate(tokens):
                if n_tokens == 1:
                    position = "only"
                elif i == 0:
                    position = "initial"
                elif i == n_tokens - 1:
                    position = "final"
                else:
                    position = "medial"

                tokens_rows.append({
                    "folio_id": base_folio,
                    "line_id": f"{base_folio}.{line_num}",
                    "unit_code": unit_code,
                    "transcriber": transcriber,
                    "section": meta.get("section", "?"),
                    "currier": meta.get("currier", "?"),
                    "hand": meta.get("hand", "?"),
                    "quire": meta.get("quire", "?"),
                    "paragraph_id": paragraph_id,
                    "is_para_start": is_paragraph_start,
                    "is_para_end": is_paragraph_end,
                    "token": token,
                    "position": position,
                    "token_index": i,
                    "line_length": n_tokens,
                })

            line_rows.append({
                "folio_id": base_folio,
                "line_id": f"{base_folio}.{line_num}",
                "unit_code": unit_code,
                "transcriber": transcriber,
                "section": meta.get("section", "?"),
                "currier": meta.get("currier", "?"),
                "hand": meta.get("hand", "?"),
                "paragraph_id": paragraph_id,
                "is_para_start": is_paragraph_start,
                "is_para_end": is_paragraph_end,
                "n_tokens": n_tokens,
                "eva_raw": eva_raw,
                "tokens": " ".join(tokens),
            })

    stats = {
        "total_lines_parsed": total_lines_parsed,
        "total_tokens": total_tokens,
        "total_paragraphs": paragraph_id,
        "total_folios": len(folio_meta),
        "skipped_lines": skipped_lines,
        "transcriber_counts": dict(sorted(transcriber_counts.items())),
    }

    return tokens_rows, line_rows, folio_meta, stats


def main():
    print(f"Parsing {CORPUS_FILE}...")
    tokens_rows, line_rows, folio_meta, stats = parse_ivtff(CORPUS_FILE, PRIMARY_TRANSCRIBER)

    print(f"\n=== PARSE STATS ===")
    print(f"Total folios with metadata: {stats['total_folios']}")
    print(f"Total lines parsed ({PRIMARY_TRANSCRIBER}): {stats['total_lines_parsed']}")
    print(f"Total tokens ({PRIMARY_TRANSCRIBER}): {stats['total_tokens']}")
    print(f"Total paragraphs: {stats['total_paragraphs']}")
    print(f"Skipped lines (no match): {stats['skipped_lines']}")
    print(f"\nLines per transcriber:")
    for k, v in sorted(stats['transcriber_counts'].items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")

    # Section distribution
    from collections import Counter
    section_counts = Counter(r["section"] for r in tokens_rows)
    print(f"\nTokens by section (primary transcriber {PRIMARY_TRANSCRIBER}):")
    for sec, cnt in sorted(section_counts.items()):
        print(f"  $I={sec}: {cnt} tokens")

    currier_counts = Counter(r["currier"] for r in tokens_rows)
    print(f"\nTokens by Currier language:")
    for cur, cnt in sorted(currier_counts.items()):
        print(f"  $L={cur}: {cnt} tokens")

    # Top 20 tokens
    token_freq = Counter(r["token"] for r in tokens_rows)
    print(f"\nTop 20 most frequent tokens:")
    for token, cnt in token_freq.most_common(20):
        print(f"  {token}: {cnt}")

    # Unique types
    unique_types = len(token_freq)
    print(f"\nUnique token types: {unique_types}")

    # Save outputs
    # 1. Token-level CSV
    token_csv = OUT_DIR / "corpus_tokens.csv"
    with open(token_csv, "w", newline="", encoding="utf-8") as f:
        if tokens_rows:
            writer = csv.DictWriter(f, fieldnames=tokens_rows[0].keys())
            writer.writeheader()
            writer.writerows(tokens_rows)
    print(f"\nSaved: {token_csv}")

    # 2. Line-level CSV
    line_csv = OUT_DIR / "corpus_lines.csv"
    with open(line_csv, "w", newline="", encoding="utf-8") as f:
        if line_rows:
            writer = csv.DictWriter(f, fieldnames=line_rows[0].keys())
            writer.writeheader()
            writer.writerows(line_rows)
    print(f"Saved: {line_csv}")

    # 3. Folio metadata JSON
    meta_json = OUT_DIR / "folio_metadata.json"
    with open(meta_json, "w", encoding="utf-8") as f:
        json.dump(folio_meta, f, indent=2)
    print(f"Saved: {meta_json}")

    # 4. Stats JSON
    stats_json = OUT_DIR / "parse_stats.json"
    stats_out = {
        **stats,
        "section_token_counts": dict(section_counts),
        "currier_token_counts": dict(currier_counts),
        "top_50_tokens": token_freq.most_common(50),
        "unique_token_types": unique_types,
    }
    with open(stats_json, "w", encoding="utf-8") as f:
        json.dump(stats_out, f, indent=2)
    print(f"Saved: {stats_json}")

    print("\nD1 parse complete.")
    return stats, token_freq, section_counts, currier_counts


if __name__ == "__main__":
    main()
