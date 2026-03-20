#!/usr/bin/env bash
# reproduce.sh — run full SPBCEH analysis pipeline from repo root
# Requires: data/Lsi_ivtff_0d_v4j_fixed.txt (download from voynich.nu/transcr.html)
# Usage: cd <repo-root> && bash scripts/reproduce.sh
# Runtime: ~5-10 min total (step 4 ~2 min, step 6 ~3 min)

set -e
cd "$(dirname "$0")"   # scripts/

echo "[1/6] Parsing corpus..."
python parse_corpus.py

echo "[2/6] Cluster frequency + role classification..."
python p1_cluster_analysis.py

echo "[3/6] Falsification test..."
python p1_3_falsification.py

echo "[4/6] Section classification (slow: ~2 min)..."
python p1_4_classification.py

echo "[5/6] FSA conformance + entropy (Paper 2)..."
python p2_analysis.py

echo "[6/6] 6-role anti-projection test — Paper 2 primary accuracy (slow: ~3 min)..."
python p2_5_6role_rerun.py

echo "Done. Key outputs:"
echo "  data/corpus_tokens.csv"
echo "  results/p1_1_cluster_frequencies.csv"
echo "  results/p1_3_falsification_v1.1_results.json"
echo "  results/p1_4_classification_results.json"
echo "  results/p1_6_transition_matrix.json"
echo "  results/p2_all_results.json       (FSA conformance = 61.3%)"
echo "  results/p2_5_v2_6role_results.json (6-role accuracy = 64.7%)"
