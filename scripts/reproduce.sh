#!/usr/bin/env bash
# reproduce.sh — run full SPBCEH analysis pipeline from repo root
# Requires: data/Lsi_ivtff_0d_v4j_fixed.txt (download from voynich.nu/transcr.html)
# Usage: cd <repo-root> && bash scripts/reproduce.sh

set -e
cd "$(dirname "$0")"   # scripts/

echo "[1/5] Parsing corpus..."
python parse_corpus.py

echo "[2/5] Cluster frequency + role classification..."
python p1_cluster_analysis.py

echo "[3/5] Falsification test..."
python p1_3_falsification.py

echo "[4/5] Section classification..."
python p1_4_classification.py

echo "[5/5] FSA conformance + entropy (Paper 2)..."
python p2_analysis.py

echo "Done. Key outputs:"
echo "  data/corpus_tokens.csv"
echo "  results/p1_1_cluster_frequencies.csv"
echo "  results/p1_3_falsification_v1.1_results.json"
echo "  results/p1_4_classification_results.json"
echo "  results/p1_6_transition_matrix.json"
echo "  results/p2_all_results.json (p2_1.para_level.pct_conformant_trans = 61.3)"
