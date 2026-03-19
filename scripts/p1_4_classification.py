#!/usr/bin/env python3
"""
P1.4: Predictive Section Classification.

Tests whether SPBCEH role frequencies predict section identity better than:
  (a) chance
  (b) raw token frequency features alone

Setup:
  - 5 seeds, stratified 80/20 split
  - Features: (A) SPBCEH role freqs (7), (B) top-100 token freqs, (C) combined (107)
  - Classifiers: logistic regression + KNN (k=5)
  - Targets: section (8-class), Currier (2-class control)

Red flags:
  RF3:  best section accuracy <30% → SPBCEH roles do not predict section
  RF3b: combined accuracy < SPBCEH-only + 2% → SPBCEH adds nothing over raw tokens
"""

import csv
import json
import math
import random
from collections import defaultdict, Counter
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
D1_DIR  = BASE_DIR / "data"
P1_DIR  = BASE_DIR / "results"

SPBCEH_CLUSTERS = {
    "INIT":  ["qokeedy","qokeey","qokedy","qokaiin","qokai!n","qokar","qokol","qoky","qokal","qokey","fachys"],
    "CLOSE": ["chedy","shedy","chey","shey","cfhaiin","ykchdy","cheey","sheey","chdy","lchedy"],
    "LINK":  ["okaiin","okeey","otar","otedy","oteey","okar","okal"],
    "ACT":   ["daiin","dain","dai!n","dar","dal","dol"],
    "MODE":  ["shol","chol","shor","chor","cheol","sheol"],
    "TIME":  ["aiin","aiiin","saiin","otaiin"],
    "REF":   ["ol","or","al"],
}
ROLES = ["INIT","CLOSE","LINK","ACT","MODE","TIME","REF"]
ROLE_MAP = {c: r for r, cs in SPBCEH_CLUSTERS.items() for c in cs}

SECTIONS = ["H","S","B","P","C","Z","A","T"]
CURRIER_LABELS = ["A","B"]

# ──────────────────────────────────────────────────────────
# Load folio-level features
# ──────────────────────────────────────────────────────────
def load_folio_data():
    """
    Returns: folio_records list of dicts with:
      folio_id, section, currier, token_counts (Counter), role_counts (Counter)
    """
    folio_tokens = defaultdict(lambda: {"section": None, "currier": None,
                                         "tokens": Counter(), "roles": Counter()})
    with open(D1_DIR / "corpus_tokens.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fid = row["folio_id"]
            tok = row["token"]
            folio_tokens[fid]["section"]  = row["section"]
            folio_tokens[fid]["currier"]  = row["currier"]
            folio_tokens[fid]["tokens"][tok] += 1
            role = ROLE_MAP.get(tok)
            if role:
                folio_tokens[fid]["roles"][role] += 1

    records = []
    for fid, d in folio_tokens.items():
        # Only include folios with known section and currier
        if d["section"] and d["currier"] and d["section"] in SECTIONS:
            records.append({
                "folio_id": fid,
                "section":  d["section"],
                "currier":  d["currier"],
                "tokens":   d["tokens"],
                "roles":    d["roles"],
            })
    return records


def get_top_tokens(records, n=100):
    """Return the n most frequent tokens across all folios."""
    total = Counter()
    for r in records:
        total.update(r["tokens"])
    return [tok for tok, _ in total.most_common(n)]


def make_feature_vectors(records, top_tokens):
    """
    Build feature vectors A, B, C for each folio record.
    A = normalized SPBCEH role frequencies (7 dims)
    B = normalized top-100 token frequencies (100 dims)
    C = A + B combined (107 dims)
    """
    feats = []
    for r in records:
        total_toks = sum(r["tokens"].values())
        total_roles = sum(r["roles"].values())

        # Feature A: SPBCEH role freqs
        if total_roles > 0:
            A = [r["roles"].get(role, 0) / total_roles for role in ROLES]
        else:
            A = [0.0] * 7

        # Feature B: top-100 token freqs
        if total_toks > 0:
            B = [r["tokens"].get(tok, 0) / total_toks for tok in top_tokens]
        else:
            B = [0.0] * len(top_tokens)

        C = A + B
        feats.append({"folio_id": r["folio_id"], "section": r["section"],
                       "currier": r["currier"], "A": A, "B": B, "C": C})
    return feats


# ──────────────────────────────────────────────────────────
# Stratified split
# ──────────────────────────────────────────────────────────
def stratified_split(records, label_key, test_frac=0.2, seed=0):
    """80/20 stratified split by label_key."""
    rng = random.Random(seed)
    by_label = defaultdict(list)
    for r in records:
        by_label[r[label_key]].append(r)

    train, test = [], []
    for label, items in by_label.items():
        items_s = list(items)
        rng.shuffle(items_s)
        n_test = max(1, round(len(items_s) * test_frac))
        test.extend(items_s[:n_test])
        train.extend(items_s[n_test:])
    return train, test


# ──────────────────────────────────────────────────────────
# Classifiers (no external libraries)
# ──────────────────────────────────────────────────────────
def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def vec_add(a, b):
    return [x+y for x, y in zip(a, b)]

def vec_scale(a, s):
    return [x*s for x in a]

def softmax(z):
    m = max(z)
    exps = [math.exp(x - m) for x in z]
    s = sum(exps)
    return [e/s for e in exps]


class LogisticRegression:
    """One-vs-rest multinomial logistic regression with L2 regularization."""
    def __init__(self, labels, lr=0.1, epochs=500, reg=0.01):
        self.labels = sorted(set(labels))
        self.lr = lr
        self.epochs = epochs
        self.reg = reg
        self.weights = None

    def fit(self, X, y):
        n_feat = len(X[0])
        n_cls = len(self.labels)
        label_idx = {l: i for i, l in enumerate(self.labels)}
        # Initialize weights [n_cls × n_feat]
        W = [[0.0]*n_feat for _ in range(n_cls)]
        b = [0.0]*n_cls

        for epoch in range(self.epochs):
            for xi, yi in zip(X, y):
                # Forward
                logits = [dot(W[c], xi) + b[c] for c in range(n_cls)]
                probs = softmax(logits)
                # Gradient
                true_c = label_idx[yi]
                for c in range(n_cls):
                    err = probs[c] - (1.0 if c == true_c else 0.0)
                    for j in range(n_feat):
                        W[c][j] -= self.lr * (err * xi[j] + self.reg * W[c][j])
                    b[c] -= self.lr * err

        self.weights = W
        self.bias = b
        self.label_idx = label_idx

    def predict(self, X):
        preds = []
        n_cls = len(self.labels)
        for xi in X:
            logits = [dot(self.weights[c], xi) + self.bias[c] for c in range(n_cls)]
            preds.append(self.labels[logits.index(max(logits))])
        return preds

    def score(self, X, y):
        preds = self.predict(X)
        return sum(p == t for p, t in zip(preds, y)) / len(y)


class KNN:
    """K-Nearest Neighbors classifier (Euclidean distance)."""
    def __init__(self, k=5):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        preds = []
        for xi in X:
            dists = []
            for xj, yj in zip(self.X_train, self.y_train):
                d = math.sqrt(sum((a-b)**2 for a, b in zip(xi, xj)))
                dists.append((d, yj))
            dists.sort(key=lambda x: x[0])
            neighbors = [yj for _, yj in dists[:self.k]]
            preds.append(Counter(neighbors).most_common(1)[0][0])
        return preds

    def score(self, X, y):
        preds = self.predict(X)
        return sum(p == t for p, t in zip(preds, y)) / len(y)


# ──────────────────────────────────────────────────────────
# Baseline: majority class
# ──────────────────────────────────────────────────────────
def majority_baseline(train_labels, test_labels):
    majority = Counter(train_labels).most_common(1)[0][0]
    return sum(l == majority for l in test_labels) / len(test_labels)


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
def run_classification(feats, label_key, feat_key, seeds, clf_class, clf_kwargs, label_name,
                       valid_labels=None):
    """Run n-seed classification and return mean accuracy.
    valid_labels: if set, filter records to those with label in valid_labels.
    """
    if valid_labels:
        feats = [r for r in feats if r[label_key] in valid_labels]
    accs = []
    for seed in seeds:
        train, test = stratified_split(feats, label_key, test_frac=0.2, seed=seed)
        X_train = [r[feat_key] for r in train]
        y_train = [r[label_key] for r in train]
        X_test  = [r[feat_key] for r in test]
        y_test  = [r[label_key] for r in test]

        if len(set(y_train)) < 2:
            continue

        # For LogReg, derive labels from training data
        kw = dict(clf_kwargs)
        if clf_class is LogisticRegression:
            kw["labels"] = sorted(set(y_train))

        clf = clf_class(**kw)
        clf.fit(X_train, y_train)
        acc = clf.score(X_test, y_test)
        accs.append(acc)
    mean_acc = sum(accs) / len(accs) if accs else 0.0
    return mean_acc, accs


def main():
    print("P1.4 — Predictive Section Classification")
    print("Loading folio data...")
    records = load_folio_data()
    print(f"Folios with known section: {len(records)}")

    # Section distribution
    sec_counts = Counter(r["section"] for r in records)
    print(f"Section distribution: {dict(sorted(sec_counts.items()))}")

    top_tokens = get_top_tokens(records, n=100)
    feats = make_feature_vectors(records, top_tokens)
    print(f"Feature vectors built: {len(feats)}")

    SEEDS = [0, 1, 2, 3, 4]

    # ── Section classification ──
    print("\n=== SECTION CLASSIFICATION (8-class) ===")

    results = {}

    for feat_key, feat_name in [("A","SPBCEH roles (7)"), ("B","Top-100 tokens"), ("C","Combined (107)")]:
        for clf_name, clf_class, clf_kwargs in [
            ("LogReg", LogisticRegression, {"labels": SECTIONS, "lr": 0.05, "epochs": 300, "reg": 0.01}),
            ("KNN-5",  KNN,               {"k": 5}),
        ]:
            mean_acc, seed_accs = run_classification(feats, "section", feat_key, SEEDS, clf_class, clf_kwargs,
                                                     feat_name, valid_labels=set(SECTIONS))
            key = f"{feat_key}_{clf_name}_section"
            results[key] = {"feat": feat_name, "clf": clf_name, "target": "section",
                            "mean_acc": mean_acc, "seed_accs": seed_accs}
            print(f"  {feat_name} | {clf_name}: {mean_acc:.3f} ({', '.join(f'{a:.3f}' for a in seed_accs)})")

    # ── Currier (2-class control) ──
    print("\n=== CURRIER CLASSIFICATION (2-class control) ===")
    for feat_key, feat_name in [("A","SPBCEH roles (7)"), ("B","Top-100 tokens"), ("C","Combined (107)")]:
        for clf_name, clf_class, clf_kwargs in [
            ("LogReg", LogisticRegression, {"labels": CURRIER_LABELS, "lr": 0.05, "epochs": 300, "reg": 0.01}),
            ("KNN-5",  KNN,               {"k": 5}),
        ]:
            mean_acc, seed_accs = run_classification(feats, "currier", feat_key, SEEDS, clf_class, clf_kwargs,
                                                     feat_name, valid_labels={"A","B"})
            key = f"{feat_key}_{clf_name}_currier"
            results[key] = {"feat": feat_name, "clf": clf_name, "target": "currier",
                            "mean_acc": mean_acc, "seed_accs": seed_accs}
            print(f"  {feat_name} | {clf_name}: {mean_acc:.3f} ({', '.join(f'{a:.3f}' for a in seed_accs)})")

    # ── Majority baseline ──
    print("\n=== BASELINES ===")
    all_sections = [r["section"] for r in feats]
    all_currier  = [r["currier"]  for r in feats]
    train0, test0 = stratified_split(feats, "section", seed=0)
    maj_sec = majority_baseline([r["section"] for r in train0], [r["section"] for r in test0])
    train0c, test0c = stratified_split(feats, "currier", seed=0)
    maj_cur = majority_baseline([r["currier"] for r in train0c], [r["currier"] for r in test0c])
    print(f"  Section majority baseline: {maj_sec:.3f}")
    print(f"  Currier majority baseline: {maj_cur:.3f}")

    # ── Red flag checks ──
    print("\n=== RED FLAG CHECKS ===")
    best_section_spbceh = max(results[k]["mean_acc"] for k in results if "_section" in k and k.startswith("A_"))
    best_section_raw    = max(results[k]["mean_acc"] for k in results if "_section" in k and k.startswith("B_"))
    best_section_combo  = max(results[k]["mean_acc"] for k in results if "_section" in k and k.startswith("C_"))

    print(f"  Best SPBCEH-only section acc: {best_section_spbceh:.3f}")
    print(f"  Best raw-token section acc:   {best_section_raw:.3f}")
    print(f"  Best combined section acc:    {best_section_combo:.3f}")

    rf3   = best_section_spbceh < 0.30
    rf3b  = best_section_combo < best_section_spbceh + 0.02

    print(f"\n  RF3  (SPBCEH section acc <30%): {'TRIGGERED' if rf3 else 'NOT triggered'}")
    print(f"  RF3b (combined < SPBCEH + 2%): {'TRIGGERED' if rf3b else 'NOT triggered'}")

    # ── Save ──
    output = {
        "n_folios": len(records),
        "section_distribution": dict(sec_counts),
        "majority_baseline_section": maj_sec,
        "majority_baseline_currier": maj_cur,
        "results": results,
        "best_section_spbceh": best_section_spbceh,
        "best_section_raw": best_section_raw,
        "best_section_combo": best_section_combo,
        "rf3_triggered": rf3,
        "rf3b_triggered": rf3b,
    }
    out_path = P1_DIR / "p1_4_classification_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved: {out_path}")

    return output


if __name__ == "__main__":
    main()
